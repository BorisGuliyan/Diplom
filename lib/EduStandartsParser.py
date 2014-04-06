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
	def GetLinks():
		EduStandartsParser.GetHTML()
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

	@staticmethod
	def GetTextData():
		Links = EduStandartsParser.GetLinks()
		for link in Links:
			pass
			#print("http://www.edu.ru/" + link)
