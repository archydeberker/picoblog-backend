"""
Graph SQL API to expose our data for Gatsby.
"""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
import models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User


class Post(SQLAlchemyObjectType):
    class Meta:
        model = models.Post


class Message(SQLAlchemyObjectType):
    class Meta:
        model = models.Message


class Tag(SQLAlchemyObjectType):
    class Meta:
        model = models.Tag


class Query(graphene.ObjectType):
    users = graphene.List(User)
    messages = graphene.List(Message)
    posts = graphene.List(Post)
    tags = graphene.List(Tag)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_posts(self, info):
        query = Post.get_query(info)
        return query.all()

    def resolve_messages(self, info):
        query = Message.get_query(info)
        return query.all()

    def resolve_tags(self, info):
        query = Tag.get_query(info)
        return query.all()


schema = graphene.Schema(query=Query)

if __name__ == "__main__":
    query = "{hello}"
    result = schema.execute(query)
    print(result)
    query = '{hello(name: "GraphQL")}'
    result = schema.execute(query)
    print(result)
