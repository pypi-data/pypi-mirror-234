import time
from typing import Literal

import rlp
from hexbytes import HexBytes
from loguru import logger
from bubble.inner_contract import InnerContractEvent
from bubble.main import get_default_modules
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_utils import to_checksum_address, combomethod

from bubble_aide.restricting import Restricting
from bubble_aide.statics.economic import Economic
from bubble_aide.statics.calculator import Calculator
from bubble_aide.statics.contract import Contract
from bubble_aide.staking import Staking
from bubble_aide.stakingL2 import StakingL2
from bubble_aide.bubble import Bubble
from bubble_aide.bubbleL2 import BubbleL2
from bubble_aide.delegate import Delegate
from bubble_aide.slashing import Slashing
from bubble_aide.reward import Reward
from bubble_aide.govern import Govern
from bubble_aide.statics.graphqls import Graphql
from bubble_aide.statics.constant import Constant
from bubble_aide.utils.utils import get_web3, get_economic, precompile_contracts
from eth_account._utils.signing import to_standard_signature_bytes
from eth_hash.auto import keccak
from eth_keys.datatypes import Signature
from eth_typing import HexStr
from eth_utils import remove_0x_prefix, to_canonical_address


class Aide:

    def __init__(self,
                 uri: str,
                 account: LocalAccount = None,
                 economic: Economic = None
                 ):
        """
        Args:
            uri: 节点开放的RPC链接
            account: 发送签名交易时适用的默认地址
            economic: 链上经济模型数据，会自动获取（需要debug接口开放），缺少经济模型数据会导致部分功能不可用。
        """
        self.uri = uri
        self.account = account
        self.economic = economic
        self.result_type = 'auto'  # 交易返回的结果类型，通过self.set_result_type()设置
        # 设置模块
        self.__init_web3__()
        self.__init_modules__()

    def __init_web3__(self):
        """ 设置web相关模块
        """
        self.web3 = get_web3(self.uri)
        self.bub = self.web3.bub
        self.txpool = self.web3.node.txpool
        self.personal = self.web3.node.personal
        self.admin = self.web3.node.admin
        self.debug = self.web3.debug

    def __init_modules__(self):
        """ 设置bubble内置合约相关模块
        """
        self.economic = get_economic(self)
        self.constant = Constant(self)
        self.graphql = Graphql(f'{self.uri}/bubble/graphql')
        self.calculator = Calculator(self)
        self.restricting = Restricting(self)
        self.staking = Staking(self)
        self.stakingL2 = StakingL2(self)
        self.bubble = Bubble(self)
        self.bubbleL2 = BubbleL2(self)
        self.delegate = Delegate(self)
        self.slashing = Slashing(self)
        self.reward = Reward(self)
        self.govern = Govern(self)

    def set_account(self, account: LocalAccount):
        """ 设置发送交易的默认账户
        """
        self.account = account

    def set_result_type(self,
                        result_type: Literal['auto', 'txn', 'hash', 'receipt', 'event']
                        ):
        """ 设置返回结果类型，包括：auto, txn, hash, receipt, event（仅适用于内置合约，其他合约必须要手动解析），建议设置为auto
        """
        self.result_type = result_type

    @combomethod
    def create_account(self):
        """ 创建账户
        """
        return Account.create()

    @combomethod
    def create_hd_account(self):
        """ 创建HD账户
        """
        pass

    @combomethod
    def create_keystore(self, passphrase, key=None):
        """ 创建钱包文件
        """
        pass

    @combomethod
    def to_checksum_address(self, address):
        """ 任意地址转换为checksum地址
        """
        return to_checksum_address(address)

    def transfer(self, to_address, amount, txn=None, private_key=None):
        """ 发送转账交易
        """
        transfer_txn = {
            "chainId": self.bub.chain_id,
            "to": to_address,
            "gas": 21000,
            "gasPrice": self.bub.gas_price,
            "value": amount,
            "data": '',
        }

        if txn:
            transfer_txn.update(txn)

        return self.send_transaction(transfer_txn, private_key=private_key)

    def get_balance(self, address, block_identifier=None):
        """ 查询自由金额的余额
        """
        return self.bub.get_balance(address, block_identifier)

    def init_contract(self,
                      abi,
                      bytecode=None,
                      address=None
                      ):
        return Contract(self, abi, bytecode, address)

    def deploy_contract(self,
                        abi,
                        bytecode,
                        txn=None,
                        private_key=None,
                        *init_args,
                        **init_kwargs):
        contract = self.bub.contract(abi=abi, bytecode=bytecode)
        txn = contract.constructor(*init_args, **init_kwargs).build_transaction(txn)
        receipt = self.send_transaction(txn, result_type='receipt', private_key=private_key)
        address = receipt.get('contractAddress')

        if not address:
            raise Exception(f'deploy contract failed, transaction receipt: {receipt}.')

        return self.init_contract(abi, bytecode, address)

    def wait_block(self, to_block, time_out=None):
        """ 等待块高
        """
        current_block = self.bub.block_number
        time_out = time_out or (to_block - current_block) * 3

        for i in range(time_out):
            time.sleep(1)
            current_block = self.bub.block_number

            if i % 10 == 0:
                logger.info(f'waiting block: {current_block} -> {to_block}')

            # 等待确定落链
            if current_block > to_block:
                logger.info(f'waiting block: {current_block} -> {to_block}')
                return

        raise TimeoutError('wait block timeout!')

    def wait_period(self,
                    period_type: Literal['round', 'consensus', 'epoch', 'increasing'] = 'epoch',
                    wait_count: int = 1,
                    ):
        """ 基于当前块高，等待n个指定周期
        """
        current_period, _, _ = self.calculator.get_period_info(period_type=period_type)
        dest_period = current_period + wait_count - 1  # 去掉当前的指定周期
        _, end_block = self.calculator.get_period_ends(dest_period, period_type=period_type)
        self.wait_block(end_block)

    def send_transaction(self, txn: dict, fid=None, result_type=None, private_key=None):
        """ 签名交易并发送，返回交易hash
        """
        result_type = result_type or self.result_type

        account = self.bub.account.from_key(private_key) if private_key else self.account
        if not account:
            raise ValueError('no private key for signature')

        if not txn.get('from'):
            txn['from'] = account.address
            txn.pop('gas')

        txn['gas'] = txn.get('gas') or self.bub.estimate_gas(txn)
        txn['gasPrice'] = txn.get('gasPrice') or self.bub.gas_price
        txn['nonce'] = txn.get('nonce') or self.bub.get_transaction_count(account.address)
        txn['chainId'] = txn.get('chainId') or self.bub.chain_id

        # 返回交易体
        if result_type == "txn":
            return txn

        signed_txn = self.bub.account.sign_transaction(txn, account.key)
        tx_hash = self.bub.send_raw_transaction(signed_txn.rawTransaction)

        # 返回交易hash
        if result_type == 'hash':
            return tx_hash

        receipt = self.get_transaction_receipt(tx_hash)

        # 返回交易回执
        if result_type == 'receipt':
            return receipt

        # 返回预编译合约事件
        if receipt.get('to') in precompile_contracts:
            return self.decode_data(receipt, fid=fid)

        # 设置错误返回交易回执
        return receipt

    def get_transaction_receipt(self, tx_hash, timeout=20):
        """ 发送签名交易，并根据结果类型获取交易结果
        """
        receipt = self.bub.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        if type(receipt) is bytes:
            receipt = receipt.decode('utf-8')

        return receipt

    @staticmethod
    def decode_data(receipt, fid=None):
        return InnerContractEvent(fid).process_receipt(receipt)

    def ec_recover(self, block_identifier):
        """ 使用keccak方式，解出区块的签名节点公钥
        """
        block = self.web3.bub.get_block(block_identifier)

        sign = block.extraData[32:]
        extra = block.extraData[:32]
        raw_data = [bytes.fromhex(remove_0x_prefix(block.parentHash.hex())),
                    to_canonical_address(block.miner),
                    bytes.fromhex(remove_0x_prefix(block.stateRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.transactionsRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.receiptsRoot.hex())),
                    bytes.fromhex(remove_0x_prefix(block.logsBloom.hex())),
                    block.number,
                    block.gasLimit,
                    block.gasUsed,
                    block.timestamp,
                    extra,
                    bytes.fromhex(remove_0x_prefix(block.nonce.hex()))
                    ]
        hash_bytes = HexBytes(keccak(rlp.encode(raw_data)))
        signature_bytes = HexBytes(sign)
        signature_bytes_standard = to_standard_signature_bytes(signature_bytes)
        signature = Signature(signature_bytes=signature_bytes_standard)
        return remove_0x_prefix(HexStr(signature.recover_public_key_from_msg_hash(hash_bytes).to_hex()))
