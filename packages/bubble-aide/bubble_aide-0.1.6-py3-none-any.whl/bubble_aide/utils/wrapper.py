import functools


def contract_transaction(fid=None, default_txn=None):
    """ 内置合约交易装饰器，接受额外参数
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(self, *args, txn: dict = None, private_key=None, **kwargs):
            txn = txn or {}
            if default_txn:
                txn.update(default_txn)

            # 填充from地址，以免合约交易在预估gas时检验地址失败
            if not txn.get('from'):
                account = self.aide.bub.account.from_key(private_key) if private_key else self.aide.account
                if account:
                    txn['from'] = account.address

            contract_function = func(self, *args, private_key=private_key, **kwargs)
            txn = contract_function.build_transaction(txn)

            return self.aide.send_transaction(txn, fid=fid, private_key=private_key)

        return wrapper

    return decorator
