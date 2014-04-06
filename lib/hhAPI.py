from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from urllib.parse import quote
from lib.DocParser import Document

class hhAPI:

	SpecializationDict = None

	#parameters
	education = ""
	gender = 0 #пол 0-М 1-Ж
	employment = 0 #тип занятости
	experience = 0 #опыт работы
	schedule = 0 #график работы
	city = ""
	specializationId = 0
	freetext = ""
	tmptext = ""


	def __init__(self, user):
		self.city = user.city
		self.freetext = "программирование"
		self.tmptext = Document(user.resumeField._get_path())
		self.SpecializationDict = self.getDictionary("https://api.hh.ru/specializations")
		self.getSpecializationUserList()



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

	def RetrieveInfoFromText(self):
		for zone in self.tmptext:
			pass

	def CreateQuery(self, buildData=None):
		if buildData is not None:
			data = hhAPI.getCityCode(buildData.city, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
			link = "https://api.hh.ru/vacancies?text=" + quote("программирование") + "&area=" + str(data)
			print (link)
		else:
			data = hhAPI.getCityCode(self.city, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
			print("city code = " + str(data))
			link = "https://api.hh.ru/vacancies?text=" + quote("программирование") + "&area=" + str(data)
			print (link)
		#data = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		return res

	def getPossibleEdulevels(self):
		edudata = JSONParser.Parse(HTMLData.getStringHTMLData("https://api.hh.ru/dictionaries", 'utf-8'))['education_level']
		result = []
		for val in edudata:
			result.append(val['name'])
		return result

	def getDictionary(self, link):
		return JSONParser.Parse(HTMLData.getStringHTMLData(link, "utf-8"))

	def getSpecialization(self, name=None):
		data = self.SpecializationDict
		for val in data:
			for val2 in val['specializations']:
				clearvalue = Document.ParseWord(val2['name'])
				if name is not None and name in clearvalue:
					return val2['id']
				else: continue
		return None

	def getSpecializationUserList(self):
		for zone in self.tmptext.zone_list:
			for word in zone.zone_raw_text.split(" "):
				res = self.getSpecialization(word)
				if res is not None:
					self.specializationId = res
					print("spec id = " + self.specializationId)
