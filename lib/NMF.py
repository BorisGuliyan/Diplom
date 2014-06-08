from lib.tfidf import tfidf
from suggesting_system.models import VacancyCache
import numpy as np
from numpy import *
from lib.tfidf import WordCount

class NMF:

	WeightMatrix = []
	HeightMatrix = []

	@staticmethod
	def calcldiff(matrixA, matrixB):

		dif = 0
		for i in range(shape(matrixA)[0]):
			for j in range(shape(matrixA)[1]):
				if matrixB[i, j] < 0.004:
					dif +=pow(matrixA[i][j] - 0.01, 2)
					continue
				dif +=pow(matrixA[i][j] - matrixB[i, j], 2)
		return dif

	@staticmethod
	def ConvertData(RowData, allwords):
		documentWords = []
		ec = 0

		documentTitles = RowData.keys()
		for key in RowData.keys():
			documentWords.append({})
			for word in WordCount.Tokenaizer(RowData[key]):
				parsedWord = tfidf.ParseWord(word)
				documentWords[ec].setdefault(parsedWord, 0)
				documentWords[ec][parsedWord] += 1
			ec += 1
		return documentWords, documentTitles, allwords

	@staticmethod
	def CreateMatrix(allwords, documentWords):
		wordvec = []
		# print(allwords)
		for word in allwords.items():
			wordvec.append(word[0])
		print("wordvec = ")
		print(wordvec)
		print("documentWords = ")
		print(documentWords)
		# for val in documentWords:
			# print("docwords val = ")
			# print(val)

		l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in documentWords]

		# print(len(l1))
		# print(wordvec[0:10])
		# print(l1[0][0:10])
		print("l1 = ")
		print(matrix(l1))
		print(shape(l1))
		# for i in range(100):
		# 	print(l1[i])
		bads = 0
		goods = 0
		cols = shape(l1)[1]
		rows = shape(l1)[0]
		for i in range(int(cols)):   #TODO проверить передаваемые в функцию параметры, форматы данных не соотвествуют друг другу
			# if l1[0][i] == 0 and l1[1][i] == 0:
			# 	pass
			summary = 0
			for j in range(int(rows)):
				summary += l1[j][i]
			if summary != 0:
				# l1[1][0] = 1
				# print("Hit!")
				# print(wordvec[i])
				goods += 1
			if summary == 0:
				l1[int(random.random())][i] = 1
				# print("bad = " + wordvec[i])
				bads += 1

				# print("ALL BAD")
				# print(i)
				# print(wordvec[i])
				# l1[0][i] = 1    #TODO этот фикс искажает результат и не является решением проблемы, но позволяет работать дальше
		print("goods = " + str(goods) + " bads = " + str(bads))
		return l1, wordvec

	@staticmethod
	def calculate(v, pc=15, lim=4):
		ic = shape(v)[0]
		fc = shape(v)[1]

		WeightMatrix = matrix([[random.random() + 0.001 for j in range(pc)] for i in range(ic)])
		HeightMatrix = matrix([[random.random() + 0.001 for i in range(fc)] for i in range(pc)])

		print(shape(WeightMatrix))
		print(shape(HeightMatrix))

		for i in range(lim):
			wh = WeightMatrix * HeightMatrix
			cost = NMF.calcldiff(v, wh)

			print("cost = " + str(cost))
			WeightMatrixTransposed = transpose(WeightMatrix)

			hn = (WeightMatrixTransposed * v)

			hd = (WeightMatrixTransposed * WeightMatrix * HeightMatrix)

			HeightMatrix = matrix(array(HeightMatrix) * array(hn) / array(hd))

			HeightMatrixTransposed = transpose(HeightMatrix)
			wn = (v * HeightMatrixTransposed)
			wd = (WeightMatrix * HeightMatrix * HeightMatrixTransposed)
			WeightMatrix = matrix(array(WeightMatrix) * array(wn) / array(wd))
		return WeightMatrix, HeightMatrix

	@staticmethod
	def prepareToVis(WeightMatrix, HeightMatrix, docs, wordvec):
		pc, wc = shape(HeightMatrix)
		docslist = list(docs)
		toppatterns = [[] for i in range(len(docslist))]
		patternnames = []
		result = []
		for i in range(pc):
			slist = []
			for j in range(wc):
				slist.append((HeightMatrix[i, j], wordvec[j]))
			slist.sort()
			slist.reverse()
			n = [s[1] for s in slist[0:8]]
			# print("pattern = " + str(n))
			patternnames.append(n)

			flist = []
			for j in range(len(docslist)):
				flist.append((WeightMatrix[j, i], docslist[j]))
				toppatterns[j].append((WeightMatrix[j, i],i ,docslist[j]))
			flist.sort()
			flist.reverse()
			for f in flist[0:5]:
				# print("res = " + str(f))
				result.append(f)

		return toppatterns, patternnames, result


	# def vesualise(self, ):
