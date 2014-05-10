from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from Diplom import commonLangs

class GitHubAPI:

	languages = []  # список всех языков
	languagesStat = {} #название языка: процент

	@staticmethod
	def GetJSONByUserName(UserName):
		link = "https://api.github.com/users/" + UserName + "/repos"
		res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		return res

	@staticmethod
	def GetLanguages(UserName):
		languagesLinks = []
		languagesNames = []
		ReposJSON = GitHubAPI.GetJSONByUserName(UserName)
		for val in ReposJSON:
			languagesLinks.append(val['languages_url'])
		for link in languagesLinks:     #TODO may be sloooowwwww
			keysList = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8')).keys()   #слишком медленно работает
			for lang in keysList:
				if lang in commonLangs:
					languagesNames.append(lang.lower())
		print(set(languagesNames))
			#languagesNames.append(JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8')))