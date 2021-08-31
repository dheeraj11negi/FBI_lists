from scrapinghelp import htmlhelper
import csv
import re
from csv import writer
import requests
import json
from multiprocessing import Pool
from datetime import datetime
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapinghelp import htmlhelper
from    finalExtractData   import  getAllData
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

class ExtractData:
    def Crawlallurl(newele,source,findcount,apilink,getname,sanction_list):
        finddata = htmlhelper.returnvalue(source,"castle-grid-block-xs-2 castle-grid-block-sm-2 castle-grid-block-md-3","</ul>")
        if finddata=="":
            finddata = htmlhelper.returnvalue(source,
                                              "<ul class=\"full-grid wanted-grid-natural infinity",
                                              "</ul>")

        getalllinks = htmlhelper.collecturl(finddata, "<p class=\"name\">", "</p>")
        count=0
        while count<findcount:
            newurl = apilink
            newres = requests.get(newurl)
            newsource = htmlhelper.returnformatedhtml(newres.text)
            findnewdata = htmlhelper.returnvalue(source,"castle-grid-block-xs-2 castle-grid-block-sm-2 castle-grid-block-md-3","</ul>")
            getnewalllinks = htmlhelper.collecturl(finddata, "<p class=\"name\">", "</p>")
            for go in getnewalllinks:
                getalllinks.append(go)
            apilink=htmlhelper.returnvalue(newsource,"<button href=\"","\" class=")
            count+=1
        mycount=0
        length = len(getalllinks)
        mapcountry = {'Afghanistan':"Afghanistan",'Pakistan':"Pakistan",'Japan':"Japan",'Syrian': "Syria", 'Russian': "Russia", 'Mexican': "Mexico", 'Polish': "poland",
                      'Canadian': "Canada", 'American': "America", 'Haitian': "Haiti", 'Laotian': "Laos",
                      'Cuban': "Cuba", 'Brazilian': "Brazil", 'South African': "South Africa", 'Ecuadoran': "Eucador"}
        for ele in getalllinks:
            geturl = htmlhelper.returnvalue(ele, "<a href=\"", "\">")
            getAllData.getResults(newele,ele, geturl, length, mapcountry,mycount,getname,sanction_list)
            mycount+=1
    def findlessData(newele,source,getname,sanction_list):
        finddata = htmlhelper.returnvalue(source,
                                          "castle-grid-block-xs-2 castle-grid-block-sm-2 castle-grid-block-md-3",
                                          "</ul>")
        if finddata == "":
            finddata = htmlhelper.returnvalue(source,
                                              "<ul class=\"full-grid wanted-grid-natural infinity",
                                              "</ul>")

        getalllinks = htmlhelper.collecturl(finddata, "<p class=\"name\">", "</p>")
        if  len(getalllinks)<=0:
            getalllinks=htmlhelper.collecturl(finddata, "<h3 class=\"title\">", "</h3>")

        myfirstcount = 0
        mylength = len(getalllinks)
        mapcountry = {'Syrian': "Syria", 'Russian': "Russia", 'Mexican': "Mexico", 'Polish': "poland",
                      'Canadian': "Canada", 'American': "America", 'Haitian': "Haiti", 'Laotian': "Laos",
                      'Cuban': "Cuba", 'Brazilian': "Brazil", 'South African': "South Africa", 'Ecuadoran': "Eucador"}
        for ele in getalllinks:
            getnewurl = htmlhelper.returnvalue(ele, "<a href=\"", "\">")
            getAllData.getResults(newele, ele, getnewurl, mylength, mapcountry, myfirstcount, getname,sanction_list)
            myfirstcount += 1
        print("kjhgf")


