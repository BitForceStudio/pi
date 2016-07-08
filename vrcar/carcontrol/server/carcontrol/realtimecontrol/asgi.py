import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carcontrol.settings")
channel_layer = channels.asgi.get_channel_layer()
