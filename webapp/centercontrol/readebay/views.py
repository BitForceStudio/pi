from django.shortcuts import render
from django.http import HttpResponse
from readebay.models import Ebayitem
import json as simplejson
import string
import re
from urllib2 import Request,urlopen,URLError,HTTPError

def index(request):
    header = {
            'Connection':'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
            }
    url = "http://www.ebay.co.uk/itm/Antique-Natural-Baltic-Egg-Yolk-Butterscotch-Amber-74-3-Grams-/162016261125?hash=item25b8ebf405:g:BIQAAOSwQjNW8tOb"
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
    listInfo = getpagesource(url);
    jsonResult = simplejson.dumps(listInfo)
    return HttpResponse(jsonResult,content_type="application/json")

def getpagesource(url):
    # Try to trick the server using header
    header = {
            'Connection':'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
            }

    pattern_url   = "<h3 class=\"lvtitle\"><a href=(.*?)</h3>"
    pattern_title = "class=\"vip\" title=\"(.*?)\">"
    pattern_link = "\"(.*?)\"  class=\"vip\" title=\""
    pattern_grams = "Amber (.*?) Grams"
    pattern_necklace_gram = "Necklace (.*?) Grams"
    pattern_brooch_gram = "Brooch (.*?) Grams"
    #pattern_imglink = "src=\"(.*?)\""
    #pattern_img = "<img(.*?)class=\"img\" alt='Item image' />"
    pattern_id = "Grams-/(.*?)\?hash=item"
    
    pattern_price = "<li class=\"lvprice prc\">(.*?)</span>"
    pattern_money = "<span  class=\"bold\">(.*?)"
    pattern_time  = "<span aria-label=\"Ending time: \" class=\"red\">(.*?)</span>"
    
    # define the list
    #img_list=[]
    url_list=[]
    wgt_list=[]

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
#        p_img = re.findall(pattern_img,the_page, re.DOTALL)
        p_price = re.findall(pattern_price,the_page,re.DOTALL)
        p_time  = re.findall(pattern_time,the_page,re.DOTALL)
        i=0
        weight=0.0
        for str in p_url:
            p_link  = re.findall(pattern_link,str,re.DOTALL)
            p_title = re.findall(pattern_title,str,re.DOTALL)
#            str_img = p_img[i]
#            p_imglink = re.findall(pattern_imglink,str_img,re.DOTALL)
            item_price_line = p_price[i]
            item_price = float(item_price_line[27:])
            item_time = p_time[i]
            i=i+1
            for str1 in p_title:
                weight = 0.0
                p_gram = re.findall(pattern_grams,str1)
                item_id = re.findall(pattern_id,str)
                try:
                    x = float(p_gram[0])
                except:
                    x=0.0
                else:
                    weight = x;

                p_gram = re.findall(pattern_necklace_gram,str1)
                try:
                    x = float(p_gram[0])
                except:
                    x=0.0
                else:
                    weight = x

                p_gram = re.findall(pattern_brooch_gram,str1)
                try:
                    x=float(p_gram[0])
                except:
                    x=0.0
                else:
                    weight = x
            
                if weight>30.0:
                    #save to the database:
                    exist = Ebayitem.objects.filter(item_id__exact = int(item_id[0]))
                    if exist:
                        exitem = Ebayitem.objects.get(item_id__exact = int(item_id[0]))
                        if exitem.item_price != item_price:
                            exitem.item_price = item_price
                            exitem.save()
                    else:
                        createItem(int(item_id[0]),p_link[0],weight,item_time,item_price)
                        #img_list.append(p_imglink[1])
                        url_list.append(p_link[0])
                        wgt_list.append(weight)
        
        listall={#'IMGURL':img_list,
                 'ITMURL':url_list,
                 'WEIGHT':wgt_list}
        return listall
    
def createItem(item_id,url,weight,timeleft,price):
    newitem = Ebayitem()
    newitem.item_id = item_id
    newitem.item_url = url
    newitem.item_weight = weight
    newitem.item_timeleft = timeleft
    newitem.item_price = price
    newitem.save()
