from lib.DocReader import DocReader
from lib.tfidf import tfidf

class Document:

	def __init__(self, DocPath):
		self.DocPath = DocPath
		self.DocText = DocReader.Reader(self.DocPath)
		self.DocTermList = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(self.DocText))
		print(self.DocTermList)

	def GetType(self):
		pass

	def ParseResume(self):
		def SplitToZones(self):
			#зоны: контактная информация ключевые слова:(e-mail/email, город, гор, тел)
			#образование
			#квалификация(иногда совмещено с образованием)
			#навыки
			#старые места работы, опыт работы, стаж, должность
			pass
		pass
