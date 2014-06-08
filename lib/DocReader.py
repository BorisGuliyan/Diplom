import subprocess

class DocReader:

	@staticmethod
	def Reader(path):
		cmd = "antiword -m cp1251.txt " + path
		print(cmd)
		text = subprocess.check_output(cmd.split(" "), shell=True)
		return text.decode("cp1251")

	@staticmethod
	def ReadManyFiles(filesPath):
		BIGTextData = ""
		filename = ""
		filesDict = {}
		try:
			for filePath in filesPath:
				filename = filePath.split("//")[-1]
				print(filePath)
				TextData = DocReader.Reader(filePath) + "\n"
				BIGTextData += TextData
				filesDict.update(dict(zip([filename], [TextData])))
		except IOError:
			print("ERROR")
			pass
		return BIGTextData, filesDict

	def readLoadedText(self, textList, doctitleList):
		result = {}
		BIGTextData = ""
		i = 0
		for i in range(len(textList)):
			BIGTextData += textList[i]
			result.update(dict(zip([doctitleList[i]], [textList[i]])))
			i += 1
		return result
# a = DOCReader.Reader("C:\\Boris\\Учеба\\Diplom\\test.doc")
#print(a.decode("cp1251"))

