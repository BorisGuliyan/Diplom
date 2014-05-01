from lib.DocReader import DocReader
from lib.tfidf import tfidf
from Diplom import morph

class Document:

	keywords_list = ["city", "education", "expirience", "город", "гор.", "email", "e-mail", "опыт", "опыт работы",
		                 "образование", "квалификация", "образование и квалификация", "стаж", "квалификация и образование", "навыки", "технические навыки"]
	zone_list = []

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

	def __init__(self, DocPath):
		self.DocPath = DocPath
		self.DocText = DocReader.Reader(self.DocPath)
		self.DocTermList = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(self.DocText))
		self.ParseResume()
		for val in self.zone_list:
			pass
			print("start zone=========")
			if val.zone_type is not None:
				pass
				#print ("zone name = " + val.zone_type)
			print(val.zone_raw_text)
			print("end zone===========")

	def ParseResume(self):
		once = 0
		i = 0
		self.zone_list = []
		for val in self.DocText.split('\n'):
			changed_val = val.strip().lower().replace(",", '').replace(".", '')
			if once == 0:
				self.zone_list.append(self.DocumentZone(self.ParseWord(changed_val)))
				once = 1
			if changed_val in self.keywords_list:
				self.zone_list.append(self.DocumentZone(changed_val, changed_val))
				i += 1
				continue
			self.zone_list[i].zone_raw_text += self.ParseWord(changed_val)

	@staticmethod
	def ParseWord(word):
		splitted = word.split(' ')
		word_str_norm = ""
		for val in splitted:
			w = morph.parse(val)
			if len(w) > 0:
				result = w[0]
				if ("NOUN" or "ADJF" or "VERB" in result.tag) and len(result.normal_form) > 2:
					word_str_norm += result.normal_form + ' '
		return word_str_norm

	@staticmethod
	def CompareStrings(word, string):
		for val in string:
			if word == val:
				return True
		return False

#должен этой функцией корректно разделить резюме на составные части