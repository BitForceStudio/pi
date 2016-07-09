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

def dircontrol(request):
    label = "remotecarcontrol"

    newcontrol,created = Room.objects.get_or_create(label=label)
    if created or newcontrol.name=="" :
    	newcontrol.name=label
    	newcontrol.save()

    return redirect(control,label=label)

def control(request,label):
    args={}
    args['label']="remotecarcontrol"
    return render(request, "realtimecontrol/base.html",args)

