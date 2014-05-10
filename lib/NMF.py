from lib.tfidf import tfidf
from suggesting_system.models import VacancyCache
import numpy as np
from numpy import *
from lib.tfidf import tfidf

class NMF:

	WeightMatrix = []
	HeightMatrix = []

	@staticmethod
	def calcldiff(matrixA, matrixB):
		dif = 0
		for i in range(shape(matrixA)[0]):
			for j in range(shape(matrixA)[1]):
				dif +=pow(matrixA[i, j] - matrixB[i, j], 2)

		return dif


	@staticmethod
	def ConvertData(RowData, allwords):
		documentWords = []
		documentTitles = []
		ec = 0

		documentTitles = RowData.keys()
		for key in RowData.keys():
			documentWords.append({})
			for word in tfidf.WordCount.Tokenaizer(RowData[key]):
				parsedWord = tfidf.ParseWord(word)
				documentWords[ec].setdefault(parsedWord, 0)
				documentWords[ec][parsedWord] += 1
			ec += 1

		print(documentWords)
		print(documentTitles)
		print(allwords)
		return documentWords, documentTitles, allwords

	def CreateMatrix(self, documentWords, allwords):
		wordvec = documentWords
		l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in allwords]

	@staticmethod
	def calculate(v, pc=3, lim=100):
		ic = shape(v)[0]
		fc = shape(v)[1]

		WeightMatrix = matrix([[random.random() for j in range(pc)] for i in range(ic)])
		HeightMatrix = matrix([[random.random() for i in range(fc)] for i in range(pc)])

		print(WeightMatrix)
		print(HeightMatrix)

		for i in range(lim):
			wh = WeightMatrix * HeightMatrix

			cost = NMF.calcldiff(v, wh)

			if cost == 0: break

			WeightMatrixTransposed = transpose(WeightMatrix)
			hn = WeightMatrixTransposed * v
			hd = WeightMatrixTransposed * WeightMatrix * HeightMatrix

			HeightMatrix = matrix(array(HeightMatrix) * array(hn) / array(hd))

			HeightMatrixTransposed = transpose(HeightMatrix)
			wn = v * HeightMatrixTransposed
			wd = WeightMatrix * HeightMatrix * HeightMatrixTransposed

			WeightMatrix = matrix(array(WeightMatrix) * array(wn) / array(wd))
		return WeightMatrix, HeightMatrix

