from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
import urllib2
import pdfkit

def index(request):
    return HttpResponse("Hello, world. You're at the readtwtcmd index.")

def readtwtmsg(request):
    respond = 'abcdef'
    location = "/media/pi/Doc/remotesaved/"
    fname = ""
    body = simplejson.loads(request.body)
    try:
        lc_url = body.find("url")
        lc_arr = body.find("->")
        twtlen = len(body)
        url = body[lc_url+3:lc_arr]
        fname = body[len_arr+2:twtlen]
        respond = savetolocal(url,location,fname)
    except ValueError as e:
        respond = e.strerror
    return HttpResponse(respond,content_type="application/json")

def savetolocal(url,location,name):
	if (url and name):
		urllen = len(url)
		if(url[urllen-3:urllen] == 'pdf'):
			return download_file(url,name,location)
		else:
			return download_html_to_pdf(url,name,location)
	else:
		return "please check the url and file name." 


def download_file(url,fname,location):
    if (url and fname):
        response = urllib2.urlopen(url)
        # detect image file : jpg, pnp, etc...
        file = open(location+fname, 'wb')
        file.write(response.read())
        file.close()
        return "Completed" + " Save "+fname+" from "+url+" to "+location
    else:
        return "undefined url or file name"

def download_html_to_pdf(url,fname,location):
    if(url and fname):
        
        pdfkit.from_url(url,location+fname)
        return " Save "+fname+" from "+url+" to "+location + "Completed"
    else:
        return "Undefined url or file name"

    
# Create your views here.
