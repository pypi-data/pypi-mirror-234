from gql import gql

from bubble_aide.utils.utils import get_gql


class Graphql:

    def __init__(self, uri: str):
        self.client = get_gql(uri)

    def execute(self, content):
        """ 执行GQL语句，并获取返回结果
        """
        return self.client.execute(gql(content))
