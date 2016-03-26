from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
import string
import re
from urllib2 import Request,urlopen,URLError,HTTPError

def index(request):
    return HttpResponse("<h2>Welcome to ebay weight extractor<\h2>")

def readebay_goldriga(request):
    url = "http://www.ebay.ph/sch/m.html?_nkw=&_armrs=1&_ipg=200&_from=&_ssn=goldriga&_sop=10"
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
    pattern_imglink = "src=\"(.*?)\""
    pattern_img = "<img(.*?)class=\"img\" alt='Item image' />"
    
    # define the list
    img_list=[]
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

        i=0
        weight=0.0
        for str in p_url:
            p_link = re.findall(pattern_link,str,re.DOTALL)
            p_title = re.findall(pattern_title,str,re.DOTALL)
#            str_img = p_img[i]
#            p_imglink = re.findall(pattern_imglink,str_img,re.DOTALL)
            for str1 in p_title:
                weight = 0.0
                p_gram = re.findall(pattern_grams,str1)
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
 #                   img_list.append(p_imglink[1])
                    url_list.append(p_link[0])
                    wgt_list.append(weight)
        
        listall={#'IMGURL':img_list,
                 'ITMURL':url_list,
                 'WEIGHT':wgt_list}
        return listall
