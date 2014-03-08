from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from urllib.parse import quote
from suggesting_system.models import User

class hhAPI:
	APIrequest = ''
	limit = ''
	#parameters
	education = ""
	gender = 0 #пол 0-М 1-Ж
	employment = 0 #тип занятости
	experience = 0 #опыт работы
	schedule = 0 #график работы
	city = ""
	freetext = ""

#тестовая задача: получить вакансии используя модельки
	@classmethod
	def get_data_from_user_model(self, User):
		#self.city = user.city
		self.freetext = "программирование"
		return self

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
		if city == "Москва":
			return data[4]['areas'][12]['areas'][0]['id']

	@staticmethod
	def CreateQuery(buildData):
		data = hhAPI.getCityCode(buildData, JSONParser.Parse(HTMLData.getStringHTMLData('https://api.hh.ru/areas', 'utf-8')))
		a = hhAPI.get_data_from_user_model(buildData)
		link = "https://api.hh.ru/vacancies?text=" + quote("программирование") + "&areas=" + data
		#data = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		return res

