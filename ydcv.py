#!/usr/bin/env python2
from urllib import quote
import urllib2, sys, json

API="YouDaoCV"
API_KEY="659600698"

if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "<words>"
else:
    for word in sys.argv[1:]:
        word = quote(word)
        data = urllib2.urlopen("http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s" % (API, API_KEY, word)).read().decode("utf-8")
        data = json.loads(data)
        try:
            pronounce = "[" + data["basic"]["phonetic"] + "]"
        except KeyError:
            pronounce = ""
        print data["query"], pronounce
        try:
            print "Explains: " + ("\n" + " " * 10).join(data["basic"]["explains"])
        except KeyError:
            pass
        try:
            print "Web:", ("\n" + " " * 5).join([item["key"] + ": " + ", ".join(item["value"]) for item in data["web"]])
        except KeyError:
            pass
