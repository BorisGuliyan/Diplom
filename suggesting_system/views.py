from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from lib.GitHubAPI import GitHubAPI
from suggesting_system.models import VacancyCache
from django.contrib import messages
from lib.HTMLData import HTMLData
from lib.Competitions import Competition


# Create your views here.
from lib.tfidf import WordCount
from suggesting_system.models import User, UserForm, UploadFileForm
from lib.hhAPI import hhAPI
from lib.NMF import NMF
import time
from numpy import *

def index(request):
	return render(request, "suggesting_system/form.html")

def info(request):
	template = loader.get_template('suggesting_system/info.html')

	allobj = User.objects.all()
	#info = hhAPI.CreateQuery(hhAPI.getCityCode(something.city))
	context = RequestContext(request, {'all': allobj, 'info': info})

	return HttpResponse(template.render(context))

def user(request, _id):

	template = loader.get_template('suggesting_system/user.html')
	FindedUser = User.objects.get(id = _id)
	t1 = time.time()
	hhapi = hhAPI(FindedUser)

	info = hhapi.CreateQuery(GitHubAPI.GetLanguages(FindedUser.gitHub))

	textList = []
	doctitleList = []
	for vac in info:
		textList.append(vac.description)
		doctitleList.append(vac.vacancy_Id)
		# print(vac.description + ' ' + vac.name)

	allDict = hhapi.docdict
	i = 0
	BIGTextData = ''
	for i in range(len(textList)):
		BIGTextData += textList[i]
		allDict.update(dict(zip([doctitleList[i]], [textList[i]])))
		i += 1

	# print(allDict)
	vacancyTerms = WordCount.get_term_one_list(WordCount.map(BIGTextData))
	print("vacancy terms = ")
	print(vacancyTerms[1])
	print("hhDATA = ")
	print(hhapi.documents.DocTermList[1])
	print("terms = ")
	test = dict(list(hhapi.documents.DocTermList[1].items()) +  list(vacancyTerms[1].items()))
	print("test = ")
	print (test)

	documentWords, documentTitles, allwords = NMF.ConvertData(allDict, test)
	print("doc worlds = ")
	print(documentWords)
	tmp = NMF.CreateMatrix(allwords, documentWords)
	# print(tmp[0])
	# print(tmp[1])
	test = NMF.calculate(tmp[0])

	print(documentTitles)
	WeightMatrix = test[0]
	HeightMatrix = test[1]
	topp, pn, res = NMF.prepareToVis(WeightMatrix, HeightMatrix, documentTitles, tmp[1])
	print("fin res" + str(res))
	finalres = []
	a = "ssss"
	for val in res:
		try:
			idVac = int(val[1])
		except:
			idVac = 0
		print("idvac = " + str(idVac))
		print(val[0])
		if idVac != 0 and int(val[0]) > 3:
			print("appending...")
			finalres.append(VacancyCache.objects.filter(vacancy_Id=idVac)[0])
	info = finalres

	# print(topp['kinect'])

	#info = Competition("test", ["course1", "course2"], ["c", "c++"], ["soft1", "soft2", "soft3"], None)
	#info = Document(FindedUser.resumeField._get_path())
	#tmp = EduStandartsParser.printresult()
	#parm = hhAPI.get_data_from_user_model(FindedUser)
	t2 = time.time()
	print("working time = " + str(t2 - t1))
	descrs = []
	context = RequestContext(request, {'FindedUser': FindedUser, "info": info, "descrs": descrs})
	return HttpResponse(template.render(context))

def form(request):
	if request.method == 'POST':
		sform = UserForm(request.POST, request.FILES)
		fform = UploadFileForm(request.POST, request.FILES)
		if sform.is_valid() and not fform.is_valid():
			st = sform.save()
			# f = fform.save()
			return HttpResponseRedirect('/user/' + str(st.id))
		if sform.is_valid() and fform.is_valid():
			st = sform.save()
			f = fform.save()
			return HttpResponseRedirect('/user/' + str(st.id))
		if not sform.is_valid() and not fform.is_valid():
			messages.add_message(request, messages.INFO, "Поля, помеченные * обязательны для заполнения")
	else:
		sform = UserForm()
		fform = UploadFileForm()
	return render(request, 'suggesting_system/form.html', {'sform': sform, 'fform': fform})