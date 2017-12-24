# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *
from django.db import models
from datetime import datetime
import json
from django.utils import timezone


class Page(Document):
    url = URLField(required=True)
    last_update = DateTimeField(required = True)


# Create your models here.
class WebSite(Document):
    domain = URLField(required=True)
    last_update = DateTimeField(default=datetime.now)
    pageList = ListField(EmbeddedDocumentField('Page'))


class ScrapyItem(Document):
    unique_id = StringField(max_length=100, null=True)
    data = StringField() # this stands for our crawled data
    date = DateTimeField(default=timezone.now)
    
    # This is for basic and custom serialisation to return it to client as a JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id
