import  requests
from  scrapinghelp import  htmlhelper
from    ExtractData import  ExtractData
class findData:
    def findmydata(urllist,ele):
        if  ele=="https://www.fbi.gov/wanted/capitol-violence":
            return
        res=requests.get(ele)
        print(res)
        source=htmlhelper.returnformatedhtml(res.text)
        getname=htmlhelper.returnvalue(source,"<h1 class=\"sr-only\">","</h1>")
        finditems=htmlhelper.returnvalue(source,"<p class=\"right\">","</p>")

        sanction_list = {
            "sl_authority": "Federal Bureau of Investigation of United States of America",
            "sl_url": "",
            "sl_host_country": "",
            "sl_type": "",
            "sl_source": "",
            "sl_description": "Fugitives declared by Federal Bureau of Investigation"
        }
        '''sanction_list["sl_url"] = ele
        sanction_list["sl_type"] = "Federal Bureau of Investigation" + getname
        sanction_list["sl_source"] = "Federal Bureau of Investigation" + getname'''
        totalitems=""

        for i in finditems:
            try:
                if  i=="0" or i=="1" or i=="2"  or i=="3" or i=="4" or  i=="5"  or  i=="6"  or  i=="7"  or  i=="8"  or  i=="9":
                    totalitems+=i
            except:
                pass
        totalitems=int(totalitems)
        if  totalitems>40:
            findcount=totalitems//40
            apilink=htmlhelper.returnvalue(source,"<button href=\"","\" class=")
            ExtractData.Crawlallurl(ele,source,findcount,apilink,getname,sanction_list)

        else:

            ExtractData.findlessData(ele,source,getname,sanction_list)