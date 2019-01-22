import graphene
import movie.schema


class Query(movie.schema.Query, graphene.ObjectType):
    pass


class Mutation(movie.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
