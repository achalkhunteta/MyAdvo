from django.db import models
import jsonfield

class GoogleForm(models.Model):
	'''
	Model class for Form object like google form
	'''

	title = models.CharField('Form Title', max_length=256, unique=True)
	form_data = jsonfield.JSONField()

	def __unicode__(self):
		return self.title