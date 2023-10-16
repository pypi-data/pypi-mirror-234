from __future__ import annotations
from elasticsearch import Elasticsearch
from settings import *

EsClient = Elasticsearch(ELASTICSEARCH_URL)


def register_events():
    from . import events
    activity_events = events.ActivityEvent()
    activity_events.initialise_events()


register_events()
