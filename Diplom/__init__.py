
import pymorphy2

from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from lib.EduStandartsParser import EduStandartsParser
import urllib.error

morph = pymorphy2.MorphAnalyzer()
SpecializationDict = None
try:
	SpecializationDict = JSONParser.Parse(HTMLData.getStringHTMLData("https://api.hh.ru/specializations", "utf-8"))
except urllib.error.URLError:
	print("Connection error, I can not work")
	exit()
#EduStandartsParser.GetHTML()
commonLangs = ["c", "c++", "ruby", "python", "javascript", "java", "c#", "f#", "css", "objective-c", "go", "shell", "perl",
	               "php", "lisp", "haskell", "pascal", "assembly", "scala", "sql", "с++"]