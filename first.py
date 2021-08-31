import  requests
from  scrapinghelp import  htmlhelper
from  Data_crawl   import   findData
from multiprocessing.pool import ThreadPool as Pool
if __name__ == '__main__':
    url="https://www.fbi.gov/wanted"
    res=requests.get(url)

    print(res)
    source=htmlhelper.returnformatedhtml(res.text)
    getdata=htmlhelper.collecturl(source,"<div class=\"col-md-12\"","</div>")
    myele=getdata[1]
    urlist=htmlhelper.collecturl(myele,"<a href=\"","\" title=")
    pool_size = 100
    pool = Pool(pool_size)
    for ele in  urlist:
        pool.apply_async(findData.findmydata,(urlist,ele,))
    pool.close()
    pool.join()


