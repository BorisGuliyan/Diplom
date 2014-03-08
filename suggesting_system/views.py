from django.forms import Form, ModelForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from lib.DocReader import DocReader
from lib.tfidf import tfidf
from lib.hhAPI import hhAPI
from lib.HTMLData import HTMLData
from lib.JSONParser import JSONParser

# Create your views here.
from suggesting_system.models import User, UserForm, UploadFileForm
from lib.DocParser import Document

def index(request):
	return render(request, "suggesting_system/index.html")

def info(request):
	template = loader.get_template('suggesting_system/info.html')

	all = User.objects.all()
	#info = hhAPI.CreateQuery(hhAPI.getCityCode(something.city))
	context = RequestContext(request, {'all': all, 'info': info})

	return HttpResponse(template.render(context))

def user(request, _id):
	template = loader.get_template('suggesting_system/user.html')
	FindedUser = User.objects.get(id = _id)
	#tfresult = tfidf.tf('интеграл', DocReader.Reader(FindedUser.resumeField._get_path()))
	info = Document(FindedUser.resumeField._get_path())
	#parm = hhAPI.get_data_from_user_model(FindedUser)
	context = RequestContext(request, {'FindedUser': FindedUser, "info": info.DocTermList[0][1]})
	return HttpResponse(template.render(context))

def form(request):
	if request.method == 'POST':
		sform = UserForm(request.POST, request.FILES)
		fform = UploadFileForm(request.POST, request.FILES)
		if sform.is_valid() and fform.is_valid():
			st = sform.save()
			f = fform.save()
			return HttpResponseRedirect('/info/')
	else:
		sform = UserForm()
		fform = UploadFileForm()
	return render(request, 'suggesting_system/form.html', {'sform': sform, 'fform': fform})