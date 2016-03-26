from __future__ import unicode_literals

from django.db import models

class Ebayitem(models.Model):
    item_id       = models.BigIntegerField(primary_key=True)
    item_url      = models.URLField()
    item_weight   = models.FloatField()
    item_timeleft = models.CharField(max_length=50)
    item_price    = models.FloatField()
    
    def id(self):
        return self.item_id