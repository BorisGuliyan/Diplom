from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from lib.DocParser import Document
from lib.tfidf import tfidf
from Diplom import SpecializationDict
from lib.DocReader import DocReader
from suggesting_system.models import VacancyCache
from lib.tfidf import WordCount

class hhAPI:

	SpecializationDict = None

	#parameters
	education = ""
	schedule = 0 #график работы
	city = ""
	specializationIdList = []
	importantSpecializations = []
	progLangs = set([])
	freetext = ""
	tmptext = ""
	documents = None
	docdict = None

	def __init__(self, user):
		self.city = user.city
		self.freetext = "программирование"
		self.tmptext = None
		#self.tmptext = Document(None, DocReader.ReadManyFiles(["C://Boris//Учеба//Курсовая.doc", "C://Boris//Учеба//Diplom//mess.doc", user.resumeField._get_path()]))
		text = DocReader.ReadManyFiles([user.resumeField._get_path(), "D://Boris//Учеба//Diplom//mess.doc"])
		self.documents = Document(None, text[0])
		self.docdict = text[1]
		# print(self.docdict)
		self.tmptext = self.documents.ParsedText
		self.SpecializationDict = SpecializationDict
		self.getSpecializationUserListByText()
		self.importantSpecializations = self.GetImportantSpecializations(self.specializationIdList)

#тестовая задача: получить вакансии используя модельки

	@staticmethod
	def searchCode(city, data): #data[index]
		for value in data:
			if value['name'] == city:
				return value['id']
		return None

	@staticmethod
	def getCityCode(city, data):  #TODO переписать рекурсивно, либо просто переписать. НЕ РАБОТАЕТ
		# i = 0
		# res = hhAPI.searchCode(city, data)
		# while res is None:
		# 	#print ("test")
		# 	for val in data:
		# 		print (val['areas'])
		# 		i += 1
		# 		res = hhAPI.searchCode(city, val['areas'])
		# 	data = val['areas']
		# 	if i > 100: return "breaked!: " + str(i)
		#return res
		if city == "москва" or city == "Москва":
			#return data[4]['areas'][12]['areas'][0]['id']
			return 1
		return 1

	def CreateQuery(self, buildData=None):
		data = hhAPI.getCityCode(self.city, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
		link = "https://api.hh.ru/vacancies?specialization="
		for spec in self.specializationIdList[:-1]:
			if spec.split(".")[0] in self.importantSpecializations:
				link += spec + "&specialization="
		link += self.specializationIdList[-1]
		link += "&area=1"
		print(buildData)
		if buildData is not None:
			print("self.progLangs union = ")
			print(self.progLangs[0].union(buildData))
		else:
			print("self.progLangs = ")
			print(self.progLangs)
		if self.progLangs is not None:
			link += "&text="
			for lang in self.progLangs[0]:
				link += lang + "%20or%20"
			link = link[:-8]
		link += "&per_page=200"
		print(link)
		res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		#print(res)
		print("result len = " + str(res['found']))
		res = self.ReadManyVacancyes(res['items'])
		return res

	def getPossibleEdulevels(self):
		edudata = JSONParser.Parse(HTMLData.getStringHTMLData("https://api.hh.ru/dictionaries", 'utf-8'))['education_level']
		result = []
		for val in edudata:
			result.append(val['name'])
		return result

	@staticmethod
	def getDictionary(link):
		return JSONParser.Parse(HTMLData.getStringHTMLData(link, "utf-8"))

	def getSpecialization(self, specdict, name=None):
		keys = specdict.keys()
		for key in keys:
			if Document.CompareStrings(name, specdict[key].split(' ')):
				# print(specdict.get(key))
				# print(key)
				#return key
				return key
		return None

	def ReadManyVacancyes(self, JSONAllVacancyData):
		result = []
		count = 0
		for item in JSONAllVacancyData:
			# print(item)
			count += 1
			findedInCache = VacancyCache.objects.filter(vacancy_Id=item['url'].split("vacancies/")[1])
			if len(findedInCache) == 0:
				VacancyJson = JSONParser.Parse(HTMLData.getStringHTMLData(item['url'], 'utf-8'))
				if VacancyJson['salary'] is not None and VacancyJson['salary']['to'] != None and VacancyJson['salary']['from'] != None:
					vacancy = VacancyCache(name=VacancyJson['name'], description=VacancyJson['description'],
					                       url=VacancyJson['alternate_url'],
					                       company_name=VacancyJson['employer']['name'], salary_start=VacancyJson['salary']['from'],
					                       salary_end=VacancyJson['salary']['to'], vacancy_Id=VacancyJson['id'])
					self.SaveVacancyToDB(vacancy)
					result.append(vacancy)
				else:
					vacancy = VacancyCache(name=VacancyJson['name'], description=VacancyJson['description'],
					                       url=VacancyJson['alternate_url'],
					                       company_name=VacancyJson['employer']['name'], salary_start=0,
					                       salary_end=0, vacancy_Id=VacancyJson['id'])
					self.SaveVacancyToDB(vacancy)
					result.append(vacancy)
			else:
				result.append(findedInCache[0])
			if count > 100:
				break
		# print(len(result))
		return result

	def SaveVacancyToDB(self, vacancy):
		VacancyNew = vacancy
		VacancyNew.save()

	def PageWorking(self):
		pass

	def printVacancy(self, vacancyList):
		for item in vacancyList:
			# print("название вакансии: " + item.name)
			# print("название компании: " + item.company_name)
			# print("ссылка: " + item.vacancy_url)
			# print("зарплата: " + str(item.salary))
			# print("descr: " + item.description)
			pass

	@staticmethod
	def ProceedSpecList(SpecDict=None): #возвращает словарь специализаций
		names = []
		ids = []
		for val in SpecDict:
			for val2 in val['specializations']:
				names.append(tfidf.ParseWord(val2['name']))
				ids.append(val2['id'])
		return dict(zip(ids, names))

	# def getSpecializationUserList(self):    #сопоставляет специализацию и резюме
	# 	i = 0
	# 	self.specializationIdList = []
	# 	progLangs = []
	# 	specdict = self.ProceedSpecList(self.SpecializationDict)
	# 	for zone in self.tmptext.zone_list:
	# 		tfrestmp = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(zone.zone_raw_text))
	# 		for val in tfrestmp:
	# 			self.progLangs |= Document.GetProgLangsFromText(val[0])
	# 			print(val[0])
	# 			res = self.getSpecialization(specdict, val[0])
	# 			if res is not None:
	# 				i += 1
	# 				self.specializationIdList.append(res)
	# 				if i > 20: break
	# 	self.GetImportantSpecializations(self.specializationIdList)

	def getSpecializationUserListByText(self):    #сопоставляет специализацию и ЛЮБОЙ ТЕКСТ
		i = 0
		self.specializationIdList = []
		specdict = self.ProceedSpecList(self.SpecializationDict)

		tfrestmp = WordCount.get_term_one_list(WordCount.map(self.tmptext))[0]
		# langs = self.documents.DocProgLangs
		self.progLangs = self.documents.DocProgLangs
		for val in tfrestmp:
			#self.progLangs |= Document.GetProgLangsFromText(val[0])
			res = self.getSpecialization(specdict, val[0])
			if res is not None:
				i += 1
				self.specializationIdList.append(res)
				if i > 100: break
		self.GetImportantSpecializations(self.specializationIdList)

	def GetImportantSpecializations(self, keyList):     #считает количество каждой специализации и возвращает самые подходящие
		SingleSpecCount = [0] * len(keyList)
		SpecIdList = []
		result = []
		for i in range(len(keyList)):
			splittedVal = keyList[i].split(".")[0]
			if splittedVal in SpecIdList:
				SingleSpecCount[SpecIdList.index(splittedVal)] += 1
			else:
				SpecIdList.append(splittedVal)
		sortedList = sorted(dict(zip(SpecIdList, SingleSpecCount)).items(), key=lambda x: x[1], reverse=True)
		maxVal = sortedList[0][1]
		result.append(sortedList[0][0])
		if maxVal > 7:      #коэффициенты приоритетности остальных специальностей, относительно наиболее приоритетной
			priorityVal = 3
		else:
			if 4 > maxVal <= 7:
				priorityVal = 2
			else:
				priorityVal = 1
		for sortedVal in sortedList[1:]:
			checkPriorityResult = maxVal / priorityVal
			if checkPriorityResult == 0:
				return result
			if sortedVal[1] >= checkPriorityResult:
				result.append(sortedVal[0])
		return result
