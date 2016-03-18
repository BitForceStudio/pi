from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
import urllib2
import pdfkit
import httplib       # for unshorten url
import urlparse      # for unshorten url

def index(request):
    return HttpResponse("Hello, world. You're at the readtwtcmd index.")

def readtwtmsg(request):
    respond = 'abcdef'
    location = "/media/pi/Doc/remotesaved/"
    fname = ""
    body = request.body
    try:
        lc_url = body.find("url")
        if lc_url < 0:
            respond = "Regular tweeter. no command found!"
            return HttpResponse(respond,content_type="application/json")
        lc_arr = body.find("->")
        lcorr = 3
        if lc_arr <= 0:
            lc_arr = body.find("-&gt;")
            lcorr = 6
        twtlen = len(body)
        url = unshortenurl(body[lc_url+4:lc_arr-1])
        res = url
        HttpResponse(res,content_type="application/json")
        fname = body[lc_arr+lcorr:twtlen]
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
        #return url+"|  "+"|"+location+"|  "+"|"+fname+"|"       
        pdfkit.from_url(url,location+fname)
        return " Save "+fname+" from "+url+" to "+location + "Completed"
    else:
        return "Undefined url or file name"

def unshortenurl(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD',parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url    

# Create your views here.
