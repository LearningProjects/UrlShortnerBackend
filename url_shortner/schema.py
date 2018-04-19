import graphene
from graphene_django.types import DjangoObjectType
from . import models
from url_shortner.models import Url

class UrlType(DjangoObjectType):
     class Meta:
          model = Url

class Shortner():
	def complete_to_short_url(complete_url):
		return complete_url + "/qwerty123"

class UrlInput(graphene.InputObjectType):
	complete_url = graphene.String(required=True)
	short_url = None

class CreateShortUrl(graphene.Mutation):
	class Arguments:
		url_object = UrlInput(required=True)

	url_object = graphene.Field(UrlType)

	@staticmethod
	def mutate(root, info, url_object):
		url_object = UrlType(
			complete_url = url_object.complete_url,
			short_url = Shortner.complete_to_short_url(
				url_object.complete_url)
		)
		Url.objects.create(complete_url='url',short_url='sh')
		return CreateShortUrl(url_object)

class Mutation(graphene.AbstractType):
	CreateShortUrl = CreateShortUrl.Field()

class Query(graphene.AbstractType):
	all_urls = graphene.List(UrlType)

	def resolve_all_urls(self, info):
		return models.Url.objects.all()