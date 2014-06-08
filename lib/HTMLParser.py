# import bs4
# from bs4 import BeautifulSoup

class HTMLParser:

	def __init__(self):

		pass

	@staticmethod
	def initSoup(HTMLDataFile):
		return None
		# return BeautifulSoup(open(HTMLDataFile))

	@staticmethod
	def GetDataFromTag(TagName, soup):
		return soup.find_all(TagName)