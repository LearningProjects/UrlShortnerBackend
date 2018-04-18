import graphene
import url_shortner.schema

class Query(url_shortner.schema.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query)