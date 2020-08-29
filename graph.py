"""
Graph SQL API to expose our data for Gatsby.
"""
from graphene import ObjectType, String, Schema


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    def resolve_hello(root, info, name):
        return f"Hello {name}"

    def resolve_goodbye(root, info):
        return 'See ya'


schema = Schema(query=Query)

if __name__ == '__main__':
    query = '{hello}'
    result = schema.execute(query)
    print(result)
    query = '{hello(name: "GraphQL")}'
    result = schema.execute(query)
    print(result)