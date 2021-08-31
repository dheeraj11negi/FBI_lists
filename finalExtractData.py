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
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def transform_name(name):
  name=name.replace("  ","")
  name=name.replace("\r","")
  name=name.replace("\t","")
  name=name.replace('\n','')
  name = name.replace("_", "")
  name = name.replace("Shri ", "")
  name = name.replace("SRI ", "")
  name = name.replace("Smt. ", "")
  name = name.replace("Dr. ", "")
  name = name.replace("Dr ", "")
  name = name.replace("Capt. ", "")
  name = name.replace("Sh. ", "")
  name = name.split(',')
  name = name[0]
  name = name.strip()

  return name

def alias_name(name):
  alias_list=[]
  subname = name.split(' ')
  l = len(subname)
  if l>=3:
    name1 = subname[l-1] + " " + subname[0]
    name2 = subname[l-2] + " " + subname[0]
    alias_list.append(transform_name(name1))
    alias_list.append(transform_name(name2))
  if l==2:
    name1 = subname[1] + " " + subname[0]
    alias_list.append(transform_name(name1))

  return alias_list
global  mylist,nationalist
mylist=[]
nationalist=set()


class getAllData:
    def getResults(newele,ele,geturl,length,mapcountry,mycount,getname,sanction_list):
        getres=requests.get(geturl)
        print(getres)
        mysource=htmlhelper.returnformatedhtml(getres.text)
        findalisas=htmlhelper.returnvalue(mysource,"<div class=\"wanted-person-aliases\">","</div")
        findcomments=htmlhelper.returnvalue(mysource,"<div class=\"wanted-person-caution\">","</div")
        d = {
            "name": "",
            "uid": "",
            "alias_name": [],
            "comments": "",
            "address": [
                {
                    "complete_address": "",
                    "state": "",
                    "city": "",
                    "country": ""
                }
                ],
            "list_type": "individual",
            "nns_status": "False",
            "last_updated": last_updated_string,
            "individual_details": {
                "gender": "",
                "date_of_birth": [],
                "organisation": ""
            },
            "documents": {
                "passport": "",
                "ssn": ""
            }
        }


        d["sanction_list"]=sanction_list


        tabledata=htmlhelper.returnvalue(mysource,"<tbody>","</tbody")
        findname=htmlhelper.returnvalue(ele,"\">","</a>")
        if  findname!="":
            d["name"]=transform_name(findname)
            d["alias_name"]=alias_name(d["name"])
        getallalises=htmlhelper.returnvalue(findalisas,"<p>","</p>").replace("\"","").strip().split(",")
        if  len(getallalises)>0:
            for addname in  getallalises:
                addnewname=addname.strip()
                d["alias_name"].append(addnewname)
        findcomments=htmlhelper.returnvalue(findcomments,"<p>","</p>")
        if  findcomments!="":
            d["comments"]=findcomments
        findtd=htmlhelper.collecturl(tabledata,"<tr>","</tr>")
        if  len(findtd)>0:
            for detail  in  findtd:
                if  "Date(s) of Birth" in   detail:
                    getdob=htmlhelper.returnvalue(detail,"</td>","</td>").replace("<td>","").split(",")
                    if  len(getdob)>0:
                        for dob in  getdob:
                            d["individual_details"]["date_of_birth"].append(dob)
                if  "Sex" in  detail:
                    getgender=htmlhelper.returnvalue(detail,"</td>","</td>").replace("<td>","")
                    if  getgender!="":
                        d["individual_details"]["gender"]=getgender
                if  "Place of Birth" in detail:
                    getbirthplace=htmlhelper.returnvalue(detail,"</td>","</td>").replace("<td>","").split(",")
                    if  len(getbirthplace)>0:
                        for check in  getbirthplace:
                            if  check   not in  mapcountry:
                                 d["address"][0]["state"]=check
                            else:
                                d["address"][0]["country"]=check


                    if  "Nationality"   in  detail:
                        getcountry=htmlhelper.returnvalue(detail,"</td>","</td>").replace("<td>","")
                        if  getcountry  in  mapcountry:
                        #d["country"].append(mapcountry[getcountry])
                            d["address"][0]["country"]=mapcountry[getcountry]
                            d["sanction_list"]["sl_host_country"]=mapcountry[getcountry]

                            nationalist.add(getcountry)
        try:
            d["address"][0]["complete_address"]= d["address"][0]["state"]+d["address"][0]["country"]
        except:
            pass
        d["uid"] = hashlib.sha256(((d["name"] + d["sanction_list"]["sl_type"]).lower()).encode()).hexdigest()
        mylist.append(d)

        if  mycount>=length-1:
            with open(getname+'.json', 'w', encoding="utf-8") as file:
                json.dump(mylist, file, ensure_ascii=False, indent=4)
            print(nationalist,end="\n")






