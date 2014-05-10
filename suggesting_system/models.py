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

class VacancyCache(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2048)
	url = models.CharField(max_length=100)
	company_name = models.CharField(max_length=100)
	salary_start = models.IntegerField()
	salary_end = models.IntegerField()
	vacancy_Id = models.IntegerField()

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

