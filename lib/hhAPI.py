from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from urllib.parse import quote
from lib.DocParser import Document
from lib.tfidf import tfidf
from Diplom import SpecializationDict

class hhAPI:

	SpecializationDict = None

	#parameters
	education = ""
	gender = 0 #пол 0-М 1-Ж
	employment = 0 #тип занятости
	experience = 0 #опыт работы
	schedule = 0 #график работы
	city = ""
	specializationIdList = []
	importantSpecializations = []
	freetext = ""
	tmptext = ""

	def __init__(self, user):
		self.city = user.city
		self.freetext = "программирование"
		self.tmptext = None
		self.tmptext = Document(user.resumeField._get_path())
		self.SpecializationDict = SpecializationDict
		self.getSpecializationUserList()
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

	def CreateQuery(self, buildData=None):
		if buildData is not None:
			data = hhAPI.getCityCode(buildData.city, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
			link = "https://api.hh.ru/vacancies?text=" + quote("программирование") + "&area=" + str(data)
			print (link)
		else:
			data = hhAPI.getCityCode(self.city, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
			print("city code = " + str(data))
			link = "https://api.hh.ru/vacancies?specialization="
			for spec in self.specializationIdList[:-1]:
				if spec.split(".")[0] in self.importantSpecializations:
					link += spec + "&specialization="
			link += self.specializationIdList[-1]
			link += "&area=" + str(data)
		#data = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		print(link)
		res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		self.printVacancy(self.ParseVacancyResponce(res['items']))
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
				print(key)
				#return key
				return key
		return None

	class Vacancy:
		name = ""
		company_name = ""
		vacancy_url = ""
		salary = 0

		def __init__(self, name, company_name, vacancy_url, salary=0):
			self.name = name
			self.company_name = company_name
			self.vacancy_url = vacancy_url
			self.salary = salary


	def ParseVacancyResponce(self, JSONAllVacancyData):
		result = []
		for item in JSONAllVacancyData:
			result.append(self.Vacancy(item['name'], item['employer']['name'], item['url']))
		return result

	def printVacancy(self, vacancyList):
		for item in vacancyList:
			# print("название вакансии: " + item.name)
			# print("название компании: " + item.company_name)
			# print("ссылка: " + item.vacancy_url)
			# print("зарплата: " + str(item.salary))
			pass

	@staticmethod
	def ProceedSpecList(SpecDict=None): #возвращает словарь специализаций
		names = []
		ids = []
		for val in SpecDict:
			for val2 in val['specializations']:
				names.append(Document.ParseWord(val2['name']))
				ids.append(val2['id'])
		return dict(zip(ids, names))

	def getSpecializationUserList(self):    #сопоставляет специализацию и резюме
		i = 0
		self.specializationIdList = []
		specdict = self.ProceedSpecList(self.SpecializationDict)
		for zone in self.tmptext.zone_list:
			tfrestmp = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(zone.zone_raw_text))
			for val in tfrestmp:
				res = self.getSpecialization(specdict, val[0])
				if res is not None:
					i += 1
					#print("res = " + specdict[res])
					self.specializationIdList.append(res)
					if i > 20: break
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
		print(sortedList)
		maxVal = sortedList[0][1]
		result.append(sortedList[0][0])
		if maxVal > 7:      #коэффициенты приоритетности остальных специальностей, относительно наиболее приоритетной
			priorityVal = 3
		else:
			if 4 > maxVal <= 7:
				priorityVal = 2
			else:
				priorityVal = 1
		print (maxVal)
		print("priority val = " + str(priorityVal))
		for sortedVal in sortedList[1:]:
			checkPriorityResult = maxVal / priorityVal
			if checkPriorityResult == 0:
				return result
			if sortedVal[1] >= checkPriorityResult:
				result.append(sortedVal[0])
		print(result)
		return result