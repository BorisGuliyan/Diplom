import subprocess

class DocReader:

	@staticmethod
	def Reader(path):
		cmd = "antiword -m cp1251.txt " + path
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
				BIGTextData += DocReader.Reader(filePath) + "\n"
				filesDict.update(dict(zip([filename], [BIGTextData])))
		except IOError:
			print("ERROR")
			pass
		return BIGTextData, filesDict


# a = DOCReader.Reader("C:\\Boris\\Учеба\\Diplom\\test.doc")
#print(a.decode("cp1251"))

