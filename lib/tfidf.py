from Diplom import morph

class WordCount:



	@staticmethod
	def wordFilter(word):
		#word = re.sub("[?.!/;:|/\\,*()&^%$#@{}[]'<>]?", '', word)
		if len(word) < 2 or word.isdigit():
			return False
		else: return True

	@staticmethod
	def Tokenaizer(text):
		stopWords = ["это", "дать", "или", "ясно", "над", "будут", "определённый", "тип", "для", "при",
		             "наш", "как", "так", "работа", "являться", "and", "the", "for", "вакансия", "также",
		             "даже", "они", "весь", "что", "если", "хороший"]
		res = []
		for line in text.split('\n'):
			for wordParsed in line.split(' '):
				#TODO перписать на регулярки как можно РАНЬШЕ
				wordReplaced = wordParsed.replace("\r", '').replace("«", '').replace("»", '').replace(".", '')\
					.replace(",", '').replace("</li>", '').replace(')', '').replace("\xa0", '')\
					.replace("<li>", '').replace("<strong>", '').replace("</strong>", '').replace("(", '')\
					.replace("<p>", '').replace("</p>", '').replace("<ul>", '').replace("</ul>", '').replace("<br", '')\
					.replace("/><br", '').replace("●", '').replace("/>•", '')
				wordParsed2 = tfidf.ParseWord(wordReplaced)
				if wordParsed2 != '' and len(wordParsed2) > 2 and WordCount.wordFilter(wordParsed2) and wordParsed2 not in stopWords:
					res.append(wordParsed2)
		# tfidf.doc_lenght = len(res)
		return res

	@staticmethod
	def map(text):
		collection = []
		tokened_text = WordCount.Tokenaizer(text)
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
		return sorted(d.items(), key=lambda x: x[1]), dict(zip(res, count)),

class tfidf: #TODO упростить использование

	doc_lenght = 0

	@classmethod
	def tf(self, word, text):   #TODO may be error and very SLOW
		all_list = WordCount.get_term_one_list(WordCount.map(text))[0]
		for value in all_list:
			pass
		try:
			return WordCount.get_term_one_list(WordCount.map(text))[0][word] / self.doc_lenght
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
				if ("NOUN" or "VERB" in result.tag) and len(result.normal_form) > 2:
					# print ("word = " + result.normal_form)
					return result.normal_form
		return ''
