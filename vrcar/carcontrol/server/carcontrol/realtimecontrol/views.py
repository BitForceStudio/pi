from django.shortcuts                   import render,redirect
from django.http                        import HttpResponseRedirect
from django.conf                        import settings
from django.db                          import transaction
from .models                            import Room

import json
import random
import string
import hashlib

def about(request):
    return render(request, "realtimecontrol/about.html")

def control(request,label):
    args={}
    args['label']=123123123123123
    return render(request, "realtimecontrol/base.html",args)

