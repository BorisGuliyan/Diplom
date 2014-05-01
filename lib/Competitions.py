from Diplom import SpecializationDict
from lib.hhAPI import hhAPI

class Competition:

#предметы из стандарта нужно добавить в компетенцию. вес легко определить по тематике и часам, распарсив стандарт
#проблема это определить нужный список стандартов
#нужно сравнить что упоминается в резюме, с тем что есть в компетенции.
#далее нужно как-то использовать профессии из хедхантера. КАК?? они плохо маппятся на стандарт образования
#из полученной инфы нужно получить запрос к hh
	#парсим резюме, получаем различные данные о знаниях, пихаем в разные компетенции по диапазонам.
	#проблема это создать кучу компетенций

	name = ""
	courseList = []
	description = ""
	progLanguages = []
	software = []
	technology = []
	professions = []

	class Profession:
		name = ""
		courses = [] #стандарты образования!!11

		def __init__(self, name, courses=None):
			self.name = name
			self.courses = courses

	class Course:
		name = ""
		gradValue = 0
		weight = 0

		def __init__(self, name, gradValue=0, weight=0):
			self.name = name
			self.gradValue = gradValue
			self.weight = weight

	def __init__(self, name, coursesList, progList, softList, techList):
		self.name = name
		self.coursesList = coursesList
		if progList is not None:
			self.setProgLanguages(progList)
		self.software = softList
		self.technology = techList
		self.professions = self.getProfessions()

	def addCourses(self, courses):
		for course in courses:
			self.coursesList.append(course)


	def setProgLanguages(self, progList):
		for progName in progList:
			self.progLanguages.append(progName)

	def courseListToProfessions(self): #TODO возможно это самая важная функция из всех вообще
		pass

	def getProfessions(self):
		ProfessionsList = []
		keys = hhAPI.ProceedSpecList(SpecializationDict).keys()
		for key in keys:
			ProfessionsList.append(self.Profession(key))
		return ProfessionsList


	def ResumeToCompetition(self):
		self.progLanguages
		pass

