import graphene
from graphene_django.types import DjangoObjectType
from django.core.exceptions import ObjectDoesNotExist
from . import models
from url_shortner.models import Url
import math

BASE_62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MAIN_SHORT_URL = "sh.rt/"

class UrlShortner:
	def base_10_to_62(c):
		return BASE_62[c]
	def base_62_to_10(c):
		return BASE_62.find(c)

	def complete_to_short(url):
		url_value = int(url)
		complete = ''
		while url_value > 62:
			complete += UrlShortner.base_10_to_62(int(url_value%62))
			url_value=int(url_value/62)

		complete += UrlShortner.base_10_to_62(int(url_value))
		return complete[::-1]

	def short_to_complete(url):
		url = url[::-1]
		sum_base10 = 0
		exp = 0
		
		for c in url:
			sum_base10 += (math.pow(62,exp)* UrlShortner.base_62_to_10(c))
			exp = exp + 1

		return str(int(sum_base10))


def save_url_object(url):
	try:
		e = Url.objects.get(complete_url=url.complete_url)
		return False
	except ObjectDoesNotExist:
		Url.objects.create(complete_url=url.complete_url,
				short_url="")
		url_with_short = Url.objects.get(complete_url=url.complete_url)
		short = UrlShortner.complete_to_short(url_with_short.id)
		url_with_short.short_url = MAIN_SHORT_URL + short
		url_with_short.save()
		return url_with_short


class UrlType(DjangoObjectType):
	class Meta:
		model = Url

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
			short_url = "")
		new_obj = save_url_object(url_object)
		if not new_obj:
			raise Exception('Link já foi encurtado')
		else:
			return CreateShortUrl(new_obj)


class Mutation(graphene.AbstractType):
	CreateShortUrl = CreateShortUrl.Field()

class Query(graphene.AbstractType):
	all_urls = graphene.List(UrlType)

	def resolve_all_urls(self, info):
		return models.Url.objects.all()