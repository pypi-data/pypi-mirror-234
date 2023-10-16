"""
Contains:
SqlAlchemy model events before_create, after_create, before_update, after_update.
"""
import importlib
import json
import sys
from decimal import Decimal
import enum
import inspect as module_inspect
from datetime import datetime, date

from elasticsearch_dsl import Search
from flask import request
from flask_sqlalchemy.model import Model
from sqlalchemy import event as alchemy_event, inspect
from . import EsClient, exceptions, APP_MODELS

DEFAULT_ACTIVITY_INDEX = 'logs'
DEFAULT_EVENTS = ['after_insert', 'before_update']

try:
    from . import ACTIVITY_INDEX, EXCLUDE_MODEL_EVENTS, EVENTS
except:
    ACTIVITY_INDEX = DEFAULT_ACTIVITY_INDEX
    EXCLUDE_MODEL_EVENTS = []
    EVENTS = DEFAULT_EVENTS


class BaseEvents(object):
    """
    Base events class.
    """
    events = []

    def initialise_events(self):
        if not self.events:
            raise exceptions.NotImplementedException("Please register models events through EventRegistry")

        for event in self.events:
            alchemy_event.listen(event['model'], event['name'], getattr(self, event['name']))

    def before_update(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")

    def after_update(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")

    def after_insert(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")

    def before_insert(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")

    def before_delete(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")

    def after_delete(self, mapper, connection, target):
        raise exceptions.NotImplementedException("Not implimented")


class EventRegistry(BaseEvents):

    @classmethod
    def register(cls, model, events: list):
        for event in events:
            cls.events.append({'model': model, 'name': event})


class ActivityMixin:
    """
    Activity event class,
    register event class in __init__.py file

    e.g.
    from . import events
    activity_events = events.ActivityEvent()
    activity_events.initialise_events()
    """

    @classmethod
    def save_activity(cls, table_name, activity, new_data, old_data=None, **kwargs):
        """
        Push user activity logs to Elasticsearch.
        """

        if old_data is None:
            old_data = {}

        # Make sure `request` is available and headers contain "Request-Id".
        request_id = request.headers.get("Request-Id")

        activity_data = {
            "Table": table_name,
            "OldData": old_data,
            "NewData": new_data,
            "Activity": activity
        }

        # Assuming `EsClient` is properly imported and initialized.

        search = Search(using=EsClient, index=ACTIVITY_INDEX).query("match", RequestID=request_id)

        try:
            response = search.execute()
            hits = response.hits

            if hits:
                # Retrieve the first matching document and update the activity array
                hit = hits[0]
                index_id = hit.meta.id
                data = hit.to_dict()
                existing_activities = json.loads(
                    data.get('Activities', "[]") or "[]")  # Deserialize existing_activities if present.
                existing_activities.append(activity_data)
                update_body = {
                    "doc": {
                        "Activities": json.dumps(existing_activities)  # Serialize existing_activities before updating.
                    }
                }
                if not request_id:
                    update_body['UserName'] = 'System'
                    update_body['UserType'] = 'SYSTEM'

                EsClient.update(index=ACTIVITY_INDEX, id=index_id, body=update_body)
                EsClient.indices.refresh(index=ACTIVITY_INDEX)
            else:
                log_body = {
                    "RequestID": request_id,
                    "Activities": json.dumps([activity_data])
                    # Serialize activity_data before inserting a new document.
                }
                if not request_id:
                    log_body['UserName'] = 'System'
                    log_body['UserType'] = 'SYSTEM'
                EsClient.index(index=ACTIVITY_INDEX, body=log_body)
                EsClient.indices.refresh(index=ACTIVITY_INDEX)
        except Exception as error:
            print("Error saving activity: %s" % str(error))

    @classmethod
    def get_history(cls, mapped_obj, target, column):
        """
        This function helps to get history/old value of a column
        if any change available.
        SqlAlchemy model object hold the old value until changed in DB.
        """
        is_changed = False
        old_value = None
        column_attr = getattr(mapped_obj.attrs, column.key)
        history = column_attr.history
        latest_value = getattr(target, column.key)

        # If a scalar attribute has been changed, the old value will be in
        # deleted.
        if history.deleted:
            is_changed = True
            old_value = history.deleted[-1]
        if history.added:
            is_changed = True

        return {'is_changed': is_changed, 'latest': latest_value, 'old': old_value}

    @classmethod
    def get_value(cls, value):
        """
        This function is used to change type of value if value is non JSON serializable.
        Update this function if you need to change value type.
        """

        try:
            # Attempt to serialize the value using json.dumps()
            return json.loads(json.dumps(value))
        except (TypeError, ValueError):
            # Handle non-serializable values
            if isinstance(value, enum.Enum):
                return value.value if value else None
            elif isinstance(value, (datetime, date)):
                return value.isoformat()
            elif isinstance(value, Decimal):
                return float(value)
            else:
                return None
        except Exception:
            return str(value)

    def get_model_data(self, target, history=False):
        """
        Get model/columns data from model instance.
        """
        old_data = {}
        new_data = {}

        # SqlAlchemy inspect will provide mapper obj
        # With mapper object we can get model attributes and columns
        mapper_obj = inspect(target)
        for column in mapper_obj.mapper.column_attrs:
            history_data = self.get_history(mapper_obj, target, column)
            if history_data.get('is_changed'):
                if history:
                    old_data[column.key] = self.get_value(history_data.get('old'))
                new_data[column.key] = self.get_value(history_data.get('latest'))

        return new_data, old_data


class ActivityEvent(BaseEvents, ActivityMixin):
    """
    Contains default events to save activity,
    Inherit this activity class to add more events.
    """

    def before_update(self, mapper, connection, target):
        """
        Receiver function before update.
        """
        activity = "Update"
        new, old = self.get_model_data(target, history=True)
        self.save_activity(
            table_name=target.__tablename__,
            activity=activity,
            new_data=new,
            old_data=old
        )

        return target

    def after_insert(self, mapper, connection, target):
        """
        Receiver function after insert,
        Push user activity logs to Elasticsearch.
        """
        activity = "Create"
        new, old = self.get_model_data(target)
        self.save_activity(
            table_name=target.__tablename__,
            activity=activity,
            new_data=new
        )

        return target


def register_models():
    """
    Auto Register model to activity event.
    Check settings file to exclude models from activity events.
    """
    model_events = EventRegistry()
    module = importlib.import_module(APP_MODELS)
    for name, obj in module_inspect.getmembers(sys.modules[module.__name__]):
        if module_inspect.isclass(obj) and issubclass(obj, Model) and name not in EXCLUDE_MODEL_EVENTS:
            model_events.register(model=obj, events=EVENTS)


register_models()
