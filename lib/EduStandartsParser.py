from lib.HTMLData import HTMLData
from lib.HTMLParser import HTMLParser
import bs4
from bs4 import BeautifulSoup

class EduStandartsParser:

	def __init__(self):
		pass

	@classmethod
	def GetHTML(cls):
		HTMLData.SaveHTML("http://www.edu.ru/db/cgi-bin/portal/spe/prog_list_new.plx?substr=&rasd=all&st=all&kod=all",
			"cp1251", "output.html")

	@staticmethod
	def GetOneStandart(link):
		HTMLData.SaveHTML(link, "cp1251", "out.html")
		return HTMLData.getStringHTMLData(link, "cp1251")

	@staticmethod
	def GetLinksFromAllStandarts():
		#EduStandartsParser.GetHTML()
		Links = []
		TableRows = HTMLParser.GetDataFromTag("tr", HTMLParser.initSoup("output.html"))
		i = 14
		while i < len(TableRows) - 1:
			if TableRows is not None:
				print(i)
				try:
					tmp = TableRows[i].find_all("th")[3]
				except IndexError:
					break
				if tmp is not None:
					Links.append(tmp.find("a", href=True)['href'])
			i += 1
		return Links

	class EduEntity:

		name = ""
		EduTime = 0
		weight = 0

		def __init__(self, name, EduTime, weight=0):
			self.name = name
			self.EduTime = EduTime
			self.weight = weight

	@staticmethod
	def GetTextData():
		TableRows = HTMLParser.GetDataFromTag("td", HTMLParser.initSoup("out.html"))
		i = 0
		result = []
		names = []
		hours = []
		for row in TableRows: #TODO за такой код я буду гореть в аду на 666 лет дольше
			try:
				tdlist = row.find_all("p")
				if tdlist is not []:
					if tdlist[0].contents[0].split(".")[0] == "СД":
						i = 1
						continue
					if i == 1:   #TODO Ловите наркомана!
						names.append(tdlist[0].contents[0])
						i += 1
						continue
					if i == 2:
						hours.append(tdlist[0].contents[0])
						i = 0
			except IndexError or AttributeError:
				print("ERROR")
		for item in names:
			result.append(EduStandartsParser.EduEntity(item, hours[names.index(item)]))
		return result

	@staticmethod
	def printresult():
		res = EduStandartsParser.GetTextData()
		for item in res:
			print("название предмета = " + item.name)
			print("часы = " + item.EduTime)