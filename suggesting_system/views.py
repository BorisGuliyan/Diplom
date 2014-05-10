import urllib
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from lib.HTMLData import HTMLData
from lib.Competitions import Competition


# Create your views here.
from suggesting_system.models import User, UserForm, UploadFileForm
from lib.DocParser import Document
from lib.EduStandartsParser import EduStandartsParser
from lib.HTMLParser import HTMLParser
from lib.hhAPI import hhAPI
from lib.DocReader import DocReader
from lib.GitHubAPI import GitHubAPI
from lib.NMF import NMF
import numpy as np
from numpy import *

def index(request):
	return render(request, "suggesting_system/index.html")

def info(request):
	template = loader.get_template('suggesting_system/info.html')

	allobj = User.objects.all()
	#info = hhAPI.CreateQuery(hhAPI.getCityCode(something.city))
	context = RequestContext(request, {'all': allobj, 'info': info})

	return HttpResponse(template.render(context))

def user(request, _id):
	template = loader.get_template('suggesting_system/user.html')
	FindedUser = User.objects.get(id = _id)
	hhapi = hhAPI(FindedUser)
	#info = DocReader.ReadManyFiles(["C://Boris//Учеба//Курсовая.doc", "C://Boris//Учеба//Diplom//mess.doc", ])
	#
	# l1 = [[1, 2], [1, 2], [1, 2]]
	# l2 = [[2, 2, 5], [2, 2, 7]]
	#
	# m1 = matrix(l1)
	# m2 = matrix(l2)
	#
	# #print(m1 * m2)
	# tmp = NMF.calculate(m1 * m2)
	#
	# print(tmp)
	info = hhapi.CreateQuery()
	tmp = NMF.ConvertData(hhapi.docdict, hhapi.tmptext)



	#info = Competition("test", ["course1", "course2"], ["c", "c++"], ["soft1", "soft2", "soft3"], None)
	#info = Document(FindedUser.resumeField._get_path())
	#tmp = EduStandartsParser.printresult()
	#parm = hhAPI.get_data_from_user_model(FindedUser)
	context = RequestContext(request, {'FindedUser': FindedUser, "info": info})
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