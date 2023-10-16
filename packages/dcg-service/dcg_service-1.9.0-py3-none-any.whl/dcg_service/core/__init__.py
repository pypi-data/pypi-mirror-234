from __future__ import annotations
from elasticsearch import Elasticsearch
from settings import *

try:
    EsClient = Elasticsearch(ELASTICSEARCH_URL)
except Exception:
    EsClient = None


def register_events():
    from . import events
    activity_events = events.ActivityEvent()
    activity_events.initialise_events()
