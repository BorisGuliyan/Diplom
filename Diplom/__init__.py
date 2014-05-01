
import pymorphy2

from lib.JSONParser import JSONParser
from lib.HTMLData import HTMLData
from lib.EduStandartsParser import EduStandartsParser

morph = pymorphy2.MorphAnalyzer()
SpecializationDict = None
SpecializationDict = JSONParser.Parse(HTMLData.getStringHTMLData("https://api.hh.ru/specializations", "utf-8"))
#EduStandartsParser.GetHTML()