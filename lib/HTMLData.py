# -*- coding: utf-8 -*-
import urllib
from urllib import request

class HTMLData:
    bdata = ''
    sdata = ''

    @staticmethod
    def getByteHTMLData(url):
        bdata = urllib.request.urlopen(url)
        return bdata

    @staticmethod
    def getStringHTMLData(url, encoding):
        sdata = HTMLData.getByteHTMLData(url).read().decode(encoding)
        return sdata