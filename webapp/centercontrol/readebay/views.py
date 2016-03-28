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
    #jsonResult = simplejson.dumps(listInfo)
    return HttpResponse(httpResponse) #jsonResult,content_type="application/json")

def getpagesource(url):
    
    httpReport = ""
    httpReport = httpHeader(httpReport)
    # Try to trick the server using header
    header = fakeHttpHeader()
    
    pattern_url   = "<h3 class=\"lvtitle\"><a href=(.*?)</h3>"
    pattern_title = "class=\"vip\" title=\"(.*?)\">"
    pattern_link = "\"(.*?)\"  class=\"vip\" title=\""
    pattern_grams = "Amber (.*?) Grams"
    pattern_necklace_gram = "Necklace (.*?) Grams"
    pattern_brooch_gram = "Brooch (.*?) Grams"
    pattern_id = "-/(.*?)\?hash=item"
    
    pattern_price = "<li class=\"lvprice prc\">(.*?)</span>"
    pattern_money = "<span  class=\"bold\">(.*?)"

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
            item_price = float(item_price_line[27:])
            i=i+1
            for str1 in p_title:
                weight = -10.0
                p_gram = re.findall(pattern_grams,str1)
                item_id = re.findall(pattern_id,str)
                try:
                    x = float(p_gram[0])
                except:
                    weight=-10.0
                else:
                    weight = x;

                p_gram = re.findall(pattern_necklace_gram,str1)
                try:
                    x = float(p_gram[0])
                except:
                    weight=-10.0
                else:
                    weight = x

                p_gram = re.findall(pattern_brooch_gram,str1)
                try:
                    x=float(p_gram[0])
                except:
                    weight=-10.0
                else:
                    weight = x
            
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
                            createItem(int(item_id[0]),p_link[0],itemReport['ITEMWEIGHT'],itemReport['ITEMTIMEL'],item_price)
                            httpReport = httpFormer(httpReport,p_link[0],itemReport,1)

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

    pattern_timeleft   = "<span id=\"vi-cdown_timeLeft\" class=\"tml tmlHt\">(.*?)</span>"
    pattern_imgurl     = "bigImage.src = '(.*?)';"
    pattern_title      = "<span id=\"vi-lkhdr-itmTitl\" class=\"u-dspn\">(.*?)</span>"
    pattern_weight   = "Weight (.*?) Grams"

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
    else:
        the_page = response.read()
        p_timeleft = re.findall(pattern_timeleft,the_page, re.DOTALL)
        p_imgurl = re.findall(pattern_imgurl,the_page, re.DOTALL)
        p_title = re.findall(pattern_title,the_page,re.DOTALL)
        p_weight = re.findall(pattern_weight,the_page)
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
    return

def patternFileReader(filename):
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