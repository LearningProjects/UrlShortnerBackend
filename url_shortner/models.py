from django.db import models

class Url(models.Model):
	id = models.AutoField(primary_key=True)
	complete_url = models.CharField(max_length=2000)
	short_url = models.CharField(max_length=15)