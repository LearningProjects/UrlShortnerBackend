import graphene
from graphene_django.types import DjangoObjectType
from . import models

class UrlType(DjangoObjectType):
	class Meta:
		model = models.Url

class Query(graphene.AbstractType):
	all_urls = graphene.List(UrlType)

	def resolve_all_urls(self, info):
		return models.Url.objects.all()