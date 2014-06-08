from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from Diplom import commonLangs

class GitHubAPI:

	languages = []  # список всех языков
	languagesStat = {} #название языка: процент

	@staticmethod
	def GetJSONByUserName(UserName):
		res = None
		link = "https://api.github.com/users/" + UserName + "/repos"
		# print(link)
		try:
			res = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8'))
		except:
			print("wrong git hub url, ignoring")
		return res

	@staticmethod
	def GetLanguages(UserName):
		languagesLinks = []
		languagesNames = []
		ReposJSON = GitHubAPI.GetJSONByUserName(UserName)
		if ReposJSON is not None:
			for val in ReposJSON:
				languagesLinks.append(val['languages_url'])
			for link in languagesLinks:     #TODO may be sloooowwwww
				keysList = JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8')).keys()   #слишком медленно работает
				for lang in keysList:
					# print(lang)
					if lang.lower() in commonLangs:
						languagesNames.append(lang.lower())
			# print(set(languagesNames))
		return set(languagesNames)
			#languagesNames.append(JSONParser.Parse(HTMLData.getStringHTMLData(link, 'utf-8')))