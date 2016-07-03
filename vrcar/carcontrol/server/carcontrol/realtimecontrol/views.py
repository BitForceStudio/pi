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
    return render(request, "chatroom/about.html")

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)
