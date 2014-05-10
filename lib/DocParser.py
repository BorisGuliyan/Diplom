from lib.DocReader import DocReader
from lib.tfidf import tfidf
from Diplom import commonLangs

class Document:

	keywords_list = ["city", "education", "expirience", "город", "гор.", "email", "e-mail", "опыт", "опыт работы",
		                 "образование", "квалификация", "образование и квалификация", "стаж", "квалификация и образование", "навыки", "технические навыки"]
	zone_list = []
	DocProgLangs = []
	DocText = ""
	ParsedText = ""
	DocTermList = None

	class DocumentZone: #разделять резюме по зонам по ключевым словам
						#зона заканчивается либо в конце документа, либо в начале другой зоны
		zone_raw_text = " "
		zone_keywords = ""
		zone_type = ""

		def __init__(self, text, zone_name=None):
			self.zone_raw_text = text
			self.zone_type = zone_name

		def SplitToZones(self, text):
			#зоны: контактная информация ключевые слова:(e-mail/email, город, гор, тел)
			#образование
			#квалификация(иногда совмещено с образованием)
			#навыки
			#старые места работы, опыт работы, стаж, должность
			pass

	def __init__(self, DocPath=None, text=None):
		if text is None:
			self.DocPath = DocPath
			self.DocText = DocReader.Reader(self.DocPath)
			self.DocTermList = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(self.DocText))
			self.ParseResume()
		else:
			self.DocText = text
			self.DocTermList = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(self.DocText))
			print(self.DocTermList)
			self.ParseText()
			self.ParseResume()

	@staticmethod
	def GetProgLangsFromText(text): #находит в тексте упоминания языков программирования
		LangsList = []              #возвращает список популярных языков из текста
		for word in text:
			if word[0].lower() in commonLangs:
				LangsList.append(word[0].lower())
		return set(LangsList)

	def ParseText(self):
		for word in self.DocText.split('\n'):
			changed_word = word.strip().lower().replace(",", '').replace(".", '')
			self.ParsedText += tfidf.ParseWord(changed_word) + " "
		# self.ParsedText = tfidf.WordCount.Tokenaizer(self.DocText)
		print(self.ParsedText)

	def ParseResume(self):
		once = 0
		i = 0
		self.zone_list = []
		for val in self.DocText.split('\n'):
			changed_val = val.strip().lower().replace(",", '').replace(".", '')
			if once == 0:
				self.zone_list.append(self.DocumentZone(tfidf.ParseWord(changed_val)))
				once = 1
			if changed_val in self.keywords_list:
				self.zone_list.append(self.DocumentZone(changed_val, changed_val))
				i += 1
				continue
			self.zone_list[i].zone_raw_text += tfidf.ParseWord(changed_val)
		self.DocProgLangs.append(Document.GetProgLangsFromText(self.DocTermList))

	@staticmethod
	def CompareStrings(word, string):
		for val in string:
			if word == val:
				return True
		return False


#должен этой функцией корректно разделить резюме на составные части