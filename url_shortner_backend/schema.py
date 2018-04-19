import graphene
import url_shortner.schema

class Mutation(url_shortner.schema.Mutation, graphene.ObjectType):
	pass

class Query(url_shortner.schema.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)