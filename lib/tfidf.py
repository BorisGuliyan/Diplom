from Diplom import morph

class tfidf: #TODO упростить использование

	doc_lenght = 0

	class WordCount:

		@staticmethod
		def wordFilter(word):
			#word = re.sub("[?.!/;:|/\\,*()&^%$#@{}[]'<>]?", '', word)
			if len(word) < 2 or word.isdigit():
				return False
			else: return True

		@staticmethod
		def Tokenaizer(text):
			res = []
			for line in text.split('\n'):
				for wordParsed in line.split(' '):
					#TODO перписать на регулярки
					wordParsed = tfidf.ParseWord(wordParsed.replace("\r", '').replace("«", '').replace("»", '').replace(".", '').replace(",", ''))
					if wordParsed != '' and len(wordParsed) > 0 and tfidf.WordCount.wordFilter(wordParsed):
						res.append(wordParsed)
			tfidf.doc_lenght = len(res)
			return res

		@staticmethod
		def map(text):
			collection = []
			tokened_text = tfidf.WordCount.Tokenaizer(text)
			for x in tokened_text:
				collection.append(x + ' 1')
			return collection

		@staticmethod
		def reduce(key, values):
			summary = 0
			for value in values:
				summary += value
			return {key :summary}

		@staticmethod
		def get_term_one_list(collection):    #костыль, не труЪ, но работает
			res = []
			count = []
			for value in collection:
				if value[:-2] in res:
					count[res.index(value[:-2])] += 1
					pass
				else:
					res.append(value[:-2])
					count.append(1)
			#return dict(zip(sorted(res), sorted(count)))
			d = dict(zip(res, count))
			#return dict(zip(res, count))
			return sorted(d.items(), key=lambda x: x[1])

	@classmethod
	def tf(self, word, text):   #TODO may be error
		all_list = tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(text))
		for value in all_list:
			pass
		try:
			return tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(text))[word] / self.doc_lenght
		except KeyError:
			return "Key not found"

	def idf(self, word, doc_count):
		pass

	@staticmethod
	def ParseWord(word):
		if len(word) > 2:
			w = morph.parse(word)
			if w != []:
				result = w[0]
				if ("NOUN" or "ADJF" or "VERB" in result.tag) and len(result.normal_form) > 2:
					return result.normal_form
		return ''

#f = open('text.txt', 'r')
#text = f.read()
#print (tfidf.WordCount.map(text))
#print (tfidf.WordCount.reduce("blablabla", [1, 1, 1, 1]))
#print (tfidf.WordCount.get_term_one_list(tfidf.WordCount.map(text)))
#print (tfidf.tf('y'))