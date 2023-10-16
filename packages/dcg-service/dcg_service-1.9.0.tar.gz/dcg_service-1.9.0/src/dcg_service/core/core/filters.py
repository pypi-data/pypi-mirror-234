"""
This filter file contains custom Filter classes, SQLAlchemy model classes and SQLAlchemy query filter.
note: File is created for code optimization purpose.
"""
from flask import request
from flask_sqlalchemy import BaseQuery


class Filter(object):
    """
    Flask filter class,
    Inherit this class to apply filters on queryset.

    e.g.

    class ModelFilter(Filter):
        model = model_name
        def add_filter(self, *args, **kwargs):
            queryset = self.get_queryset()
            queryset = queryset.filter_by(**self.request_params)
            return queryset

    use this filter class in your API view or function.

    class APIView():
        filter_class = ModelFilter
        def get():
            queryset = self.filter_class(queryset).apply()

    """

    model = None
    query_class = BaseQuery

    def __init__(self, queryset):
        self.filter_added = False
        self.result = None
        self.request_params = request.args.copy()

        if not self.model:
            raise TypeError("<class '%s'> requires model name." % self.__class__.__name__)

        if not isinstance(queryset, self.query_class):
            raise TypeError("queryset must be instance of <class '%s'>" % self.query_class.__name__)

        self.queryset = queryset

    def get_queryset(self):
        return self.queryset

    def all(self):
        """
        Return the results as a list object.
        """
        if not self.filter_added:
            raise TypeError("Queryset filter not applied on <class '%s'>, "
                            "Please '.apply()' filter first." % self.__class__.__name__)
        return self.result.all()

    def add_filter(self, *args, **kwargs):
        """
        Override this func to add custom filters on queryset.
        """
        if not self.filter_added:
            raise TypeError("Queryset filter not applied on <class '%s'>, "
                            "Please '.apply()' filter first." % self.__class__.__name__)
        queryset = self.get_queryset()
        return queryset.filter(*args, **kwargs)

    def apply(self, *args, **kwargs):
        """
        Apply filter on queryset and return results.
        """
        self.filter_added = True
        self.result = self.add_filter(*args, **kwargs)
        return self.result
