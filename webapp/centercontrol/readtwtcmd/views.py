from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson

def index(request):
    return HttpResponse("Hello, world. You're at the readtwtcmd index.")

def readtwtmsg(request):
    respond = 'abcdef'
    body = simplejson.loads(request.body)
    try:
        respond = body
    except ValueError as e:
        respond = e.strerror
    return HttpResponse(respond,content_type="application/json")
    
# Create your views here.
