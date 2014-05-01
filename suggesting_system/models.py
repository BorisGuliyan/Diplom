from django.db import models
from django.core.files import File

# Create your models here.
from django.db.models.base import Model
from django.forms import ModelForm

class User(models.Model):
	name = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	resumeField = models.FileField(upload_to='resume')
	#files = models.ForeignKey(UploadedFiles, blank=True, null=True)
	#file = models.FileField(upload_to='folder')

class UploadedFiles(models.Model):
	file = models.FileField(upload_to='folder')
	St = models.ForeignKey(User, blank=True, null=True)

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name', 'city', 'resumeField']

class UploadFileForm(ModelForm):
	class Meta:
		model = UploadedFiles
		fields = ['file']

class Vacancy(models.Model):
	text = models.CharField(max_length=10000)

