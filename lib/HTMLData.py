# -*- coding: utf-8 -*-
import os.path
import urllib
from urllib import request

class HTMLData:

	@staticmethod
	def getByteHTMLData(url):
		bdata = urllib.request.urlopen(url)
		return bdata

	@staticmethod
	def getStringHTMLData(url, encoding):
		sdata = HTMLData.getByteHTMLData(url).read().decode(encoding)
		return sdata

	@staticmethod
	def SaveHTML(url, encoding, filename):
		sdata = HTMLData.getByteHTMLData(url).read().decode(encoding)
		if not os.path.isfile(filename):
			f = open(filename, 'w')
			f.writelines(sdata)
			f.close()