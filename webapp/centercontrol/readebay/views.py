from django.shortcuts import render
from django.http import HttpResponse
from readebay.models import Ebayitem
import json as simplejson
import string
import re
from urllib2 import Request,urlopen,URLError,HTTPError

def index(request):
    # This mainly for test
    header = fakeHttpHeader()
    url = "http://www.ebay.co.uk/itm/Antique-Old-Natural-Baltic-Egg-Yolk-Butterscotch-Amber-Unique-/162020228630?hash=item25b9287e16:g:a7MAAOSwGYVW-Avu"
    req = Request(url,None,header)
    # try to connect to the server
    try:
        response = urlopen(req,None,5)
    except HTTPError,e:
        if hasattr(e,'code'):
            return 'The server cannot fuifill the request Error Code:' + e.code
        elif hasattr(e,'reason'):
            return 'We failed to reach a server, Reason: ' + e.reason
    else:
        return HttpResponse(response) 

def readebay_goldriga(request):
    url = "http://www.ebay.co.uk/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=goldriga&_ipg=200&_sop=10"
    httpResponse = getpagesource(url);
    return HttpResponse(httpResponse)

def readebay_organicwear(request):
    url = "http://www.ebay.co.uk/sch/m.html?_nkw=&_armrs=1&_ipg=200&_from=&_ssn=organicwear&_sop=1"
    httpReport = getpagesource(url); #WEIGHT : 62.37gr.
    return HttpResponse(httpResponse)

def readebay_katren2002(request):
    url = "http://www.ebay.co.uk/sch/Amber-/10191/m.html?_nkw=&_armrs=1&_ipg=200&_from=&_ssn=katren2002&_sop=1"
    httpReport = getpagesource(url); #WEIGHT : 738 gr.
    return HttpResponse(httpResponse)
    

# ------------------------------------------------------------------------------------------------------------------------
#            Private Functions
#-------------------------------------------------------------------------------------------------------------------------

def getpagesource(url):
    
    httpReport = ""
    httpReport = httpHeader(httpReport)
    # Try to trick the server using header
    header = fakeHttpHeader()
    
    pattern_url   = "<h3 class=\"lvtitle\"><a href=(.*?)</h3>"
    pattern_title = "class=\"vip\" title=\"(.*?)\">"
    pattern_link = "\"(.*?)\"  class=\"vip\" title=\""
    pattern_id = "-/(.*?)\?hash=item"
    pattern_float = "[+-]?[0-9.]+"
    pattern_price = "<li class=\"lvprice prc\">(.*?)</span>"

    req = Request(url,None,header)
    # try to connect to the server
    try:
        response = urlopen(req,None,5)
    except HTTPError,e:
        if hasattr(e,'code'):
            return 'The server cannot fuifill the request Error Code:' + e.code
        elif hasattr(e,'reason'):
            return 'We failed to reach a server, Reason: ' + e.reason
    else:
        the_page = response.read()
        p_url = re.findall(pattern_url,the_page, re.DOTALL)
        p_price = re.findall(pattern_price,the_page,re.DOTALL)
        i=0
        weight=0.0
        for str in p_url:
            p_link  = re.findall(pattern_link,str,re.DOTALL)
            p_title = re.findall(pattern_title,str,re.DOTALL)
            item_price_line = p_price[i]

            try:
                tx = re.findall(pattern_float,item_price_line,re.DOTALL)
                x = float(tx[0])
            except:
                item_price = -10
            else:
                item_price = x

            weight = -10.0
            p_gram = re.findall(pattern_float,p_title[0])
            item_id = re.findall(pattern_id,str)
            try:
                x = float(p_gram[0])
            except:
                weight=-10.0
            else:
                weight = x;
        
            if weight>30.0 or weight<0.0:
                #save to the database:
                exist = Ebayitem.objects.filter(item_id__exact = int(item_id[0]))
                if exist:
                    exitem = Ebayitem.objects.get(item_id__exact = int(item_id[0]))
                    if exitem.item_price != item_price:
                        # record updated info
                        itemReport = analyzeItemPage(exitem.item_url,exitem.item_weight,exitem.item_price)
                        exitem.item_price = item_price
                        exitem.item_timeleft = itemReport['ITEMTIMEL']
                        exitem.save()
                        httpReport = httpFormer(httpReport,exitem.item_url,itemReport,0)
                else:
                    itemReport = analyzeItemPage(p_link[0],weight,item_price)
                    if itemReport['ITEMWEIGHT']>30.0:
                        createItem(int(item_id[0]),p_link[0],itemReport['ITEMWEIGHT'],itemReport['ITEMTIMEL'],itemReport['ITEMPRICE'])
                        httpReport = httpFormer(httpReport,p_link[0],itemReport,1)

            i=i+1

        httpReport = httpFooter(httpReport)
        return httpReport
    
def createItem(item_id,url,weight,timeleft,price):
    newitem = Ebayitem()
    newitem.item_id = item_id
    newitem.item_url = url
    newitem.item_weight = weight
    newitem.item_timeleft = timeleft
    newitem.item_price = price
    newitem.save()

def httpFormer(httpReport,url,itemReport,new):
    httpReport = httpBody(httpReport,url,itemReport['ITEMIMGURL'],
                                         itemReport['ITEMTITLE'],
                                         itemReport['ITEMTIMEL'],
                                         itemReport['ITEMWEIGHT'],
                                         itemReport['ITEMPRICE'])
    return httpReport

def analyzeItemPage(url,weight,price):
    header = fakeHttpHeader()

    pattern_timeleft = "<span id=\"vi-cdown_timeLeft\" class=\"tml tmlHt\">(.*?)</span>"
    pattern_imgurl   = "bigImage.src = '(.*?)';"
    pattern_title    = "<span id=\"vi-lkhdr-itmTitl\" class=\"u-dspn\">(.*?)</span>"
    pattern_weight   = "Weight (.*?) Grams"
    pattern_price    = "<span id=\"convbidPrice\" style=\"white-space: nowrap;font-weight:bold;\">(.*?)<span>(including postage)"

    req = Request(url,None,header)
    reportList={'ITEMIMGURL':'',
                'ITEMTITLE':'',
                'ITEMWEIGHT':'',
                'ITEMPRICE':'',
                'ITEMTIMEL':''}
    try:
        response = urlopen(req,None,5)
    except HTTPError,e:
        if hasattr(e,'code'):
            print 'The server cannot fuifill the request'
            print 'Error Code:', e.code
        elif hasattr(e,'reason'):
            print 'We failed to reach a server'
            print 'Reason',e.reason
        return reportList
    else:
        the_page   = response.read()
        p_timeleft = re.findall(pattern_timeleft,the_page, re.DOTALL)
        p_imgurl   = re.findall(pattern_imgurl,the_page, re.DOTALL)
        p_title    = re.findall(pattern_title,the_page,re.DOTALL)
        p_weight   = re.findall(pattern_weight,the_page)
        tprice = 0.0
        try: 
            x = float(price)
        except:
            p_price = re.findall(pattern_price,the_page)
            tp = p_price[0]
            try:
                x = float(tp[1:])
            except:
                tprice = -100
            else:
                tprice = x
        else:
            if price<0:
                p_price = re.findall(pattern_price,the_page)
                tp = p_price[0]
                try:
                    x = float(tp[1:])
                except:
                    tprice = -100
                else:
                    tprice = x
            else:
                tprice = price
        price = tprice

        if len(p_weight)>0 and weight <0.0:
            try:
                x = float(p_weight[0])
            except:
                weight = -10.0
            else:
                weight = x 
        timeleft="01234567890123NOTIME"
        if len(p_timeleft) != 0:
            timeleft = p_timeleft[0]
        
        reportList={'ITEMIMGURL':p_imgurl[0],
                    'ITEMTITLE':p_title[0],
                    'ITEMWEIGHT':weight,
                    'ITEMPRICE':price,
                    'ITEMTIMEL':timeleft[14:]}
    return reportList

#-------------------------------------------------------------------------------------------------------------------------
#                                                    Pattern file reader
#-------------------------------------------------------------------------------------------------------------------------
def testFileReader(filename):
    try:
        with open(filename,"r") as urls:
            for line in urls:
                #remove \n
                i = line.find("\n")
                fname = "temp"
                if i>0:
                    line = line[0:i]
                else:
                    continue
                # read line and find out the command
                llen = len(line)
                url = ''
                pattern = ''

                # get url and specific pattern
                if llen>4 and line[0:3]=="URL":
                    url = line[4:llen]
                elif llen>8  and line[0:7] == "PATTERN":
                    # read pattern and save it to pattern with the key: PATTERN <h3 class=\"lvtitle\"><a href=(.*?)</h3> -----> URL
                    position = line.find("----->")
                    rex = line[8:position-1]
                    key = line[position+7:llen]
                    #pattern.append([key:rex])
    except IOError:
        print "Fail to read file "+ filename
        return
    return

def patternFileReader(filename):
    #pattern_url   = "<h3 class=\"lvtitle\"><a href=(.*?)</h3>"
    #pattern_title = "class=\"vip\" title=\"(.*?)\">"
    #pattern_link = "\"(.*?)\"  class=\"vip\" title=\""
    #pattern_id = "-/(.*?)\?hash=item"
    #pattern_float = "[+-]?[0-9.]+"
    #pattern_price = "<li class=\"lvprice prc\">(.*?)</span>"
    return

#-------------------------------------------------------------------------------------------------------------------------
#                                                    HTTP UTILITY
#-------------------------------------------------------------------------------------------------------------------------
def httpHeader(httpReport):
    header = "<!-- report header --> \n"
    header = header + "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\"> \n"
    header = header + "<html> \n"
    header = header + "    <head> \n"
    header = header + "        <meta charset=\"UTF-8\"> \n"
    header = header + "        <title>Report</title> \n"
    header = header + "        <link rel=\"stylesheet\" type=\"text/css\"> \n"
    header = header + "    </head> \n"
    header = header + "     \n"
    header = header + "    <body> \n"
    header = header + "        <main> \n"  
    return httpReport+header

def httpBody(httpReport,url,imgurl,title,tl,weight,price):
    pricepg = price/weight
    body = "<!-- report sections --> \n"
    body = body + "            <!-- in a loop --> \n"
    body = body + "            <div style=\"width:900px; height:220px; float:left; background-color: #e0e0e0;\"> \n"
    body = body + "                <section style=\"display:inline; margin-top: 10px;\"> \n"
    body = body + "                    <div style=\"width:auto; height:200px;float:left; margin-top: 10px;margin-left:10px;\"> \n"
    body = body + "                        <!-- parameter --> \n"
    body = body + "                        <img src=\""+imgurl+"\" style=\"height:200px;\"/> \n"
    body = body + "                    </div> \n"
    body = body + " \n"
    body = body + "                    <div style=\"float:left; margin-top: 10px;margin-left:10px;\"> \n"
    body = body + "                        <!-- parameter --> \n"
    body = body + "                         <a href=\""+url+"\"><span> Title: "+title+"</span> </a> \n"
    body = body + "                        <p> Weight: "+str(weight)+"</p> \n"
    body = body + "                        <p> Price: "+str(price)+" -- "+str(pricepg*9.5)+"/g </p> \n"
    body = body + "                        <p> Time left: " + tl + " </p> \n"
    body = body + "                    </div> \n"
    body = body + "                </section> \n"
    body = body + "            </div> \n"
    body = body + " \n"
    return httpReport+body
    
def httpFooter(httpReport):
    footer = "<!-- report footer --> \n"
    footer = footer + "        </main> \n"
    footer = footer + "    </body> \n"
    footer = footer + "</html> \n"
    return httpReport+footer

def fakeHttpHeader():
    fheader = {
            'Connection':'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
            }
    return fheader