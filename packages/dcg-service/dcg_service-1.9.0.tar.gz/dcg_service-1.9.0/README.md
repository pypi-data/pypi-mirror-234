The module contains several features that provide functionality for various aspects of your application. Here is a breakdown of each feature:

1. Activity Events:
   - SqlAlchemy events are used to log user activity logs to Elasticsearch.
   - The `dcg_service.core.events.py` file contains more details about these events.
   - It includes SqlAlchemy model events such as `before_create`, `after_create`, `before_update`, and `after_update`.
   - The module includes an `ActivityEvent` class and registers the event class in the `__init__.py` file.
   - You can exclude specific model names from activity events by adding them to the `EXCLUDE_MODEL_EVENTS` list in the `settings.py` file.
   - You can add events to log activity by specifying them in the `EVENTS` list in the `settings.py` file.
   - The model file path can be specified using the `APP_MODELS` variable in the `settings.py` file.

2. Authentication/Permission:
   - User authentication is handled using JWT tokens.
   - You need to set the signing key and JWT algorithms in your settings file.
   - The `is_authenticated` function from `dcg_service.core.permissions` can be used as a decorator to enforce authentication on API views.

3. Service Cache:
   - The module includes a `ServicePrice` class that fetches service fee structure from an Elasticsearch index.
   - To retrieve service fee details, you can call `ServicePrice(service_id, units).get_fee_details()`.
   - The `get_fee_details` function has an optional `include_tax` parameter to include/exclude tax details.
   - Additionally, you can use `get_coupon_details` to retrieve the total discount and coupon code.

4. Filters:
   - The module provides a Flask filter class that can be inherited to apply filters on querysets.
   - You can create a custom filter class by inheriting from `Filter` and implementing the `add_filter` method.
   - In your API views or functions, you can use the filter class by setting the `filter_class` attribute and calling `apply()` on an instance of the filter class.

5. Custom Response Handler:
   - You can change the default API response format by overriding the `CustomResponse` class from `dcg_service.core.response`.
   - The overridden class should provide a response JSON with the following structure: `{"data": data, "message": message, "title": self.response.status, "code": self.response.status_code}`.

6. Logger:
   - The module provides an overridden logger for better app debugging.

7. Encryption:
   - The module includes functions for encrypting and decrypting data.
   - You need to set the `CIPHER_PRIVATE_KEY` environment variable with a 16-character key for AES128 encryption.

8. Elastic-search DSL:
   - The module utilizes Elastic-search DSL for connecting and querying Elastic search indexes.
   - You need to set the `ELASTICSEARCH_URL` environment variable in your settings file.
   - The `ACTIVITY_INDEX` and `SERVICE_CACHE_INDEX` variables can be set to specify the indexes to be used for activity logs and service caching, respectively.


# Elastic-search DSL
Elastic-search DSL is used to connect/query on elastic search indexes.

Must add following in your settings.py file:

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ACTIVITY_INDEX = os.environ.get('ACTIVITY_INDEX', '').lower() # must be lower
    SERVICE_CACHE_INDEX = os.environ.get('SERVICE_CACHE_INDEX')


# Activity Events

SqlAlchemy events are used to log user activity logs to 'Elasticsearch'.

You can check dcg_service.core.events.py file for details.

Contains:
SqlAlchemy model events before_create, after_create, before_update, after_update.

    Activity event class,
    registerd event class in __init__.py file

    e.g.
    def register_events():
        from . import events
        activity_events = events.ActivityEvent()
        activity_events.initialise_events()

    register_events()

Add models names of your apps in settings.py to exclude from activity events.

    e.g.  EXCLUDE_MODEL_EVENTS = ['Cart']

Add events to log activity.

    e.g.  EVENTS = ['after_insert', 'before_update']

Add model file path.

    e.g APP_MODELS = 'order_app.models'


# Authentication/Permission

User authentication JWT token, set following details in your settings file.

        SIGNING_KEY = os.environ.get('SIGNING_KEY')
        JWT_ALGORITHMS = ['HS256']

Start using:

    from dcg_service.core.permissions import is_authenticated

    class ExampleView(views.MethodView):
    """
    APIs Methods
    -----------
    GET: Get list.
    """
    decorators = [is_authenticated]

    def get(self):

# Service cache

        Service price class to fetch service fee structure from `Elasticsearch` index.
        service_id: Respective service id,
        units: Units/quantity of service
        -----------------------------------------------------------------------------
        Call `ServicePrice(service_id, units).get_fee_details()` to get service fee details.
        
        For more information check file function docs.

Start using:

    from dcg_service.core.services import ServicePrice
    service = ServicePrice(service_id, units)
    price_details = service.get_fee_details(include_tax=False)
    total_discount, coupon_code = service.get_coupon_details()

# Filters

Flask filter class, Inherit this class to apply filters on queryset.

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

# Custom Response handler
Change default API response, override dcg_service.core.response.CustomResponse  class according to your need.

    returns:

    response_json = {
                "data": data,
                "message": message,
                "title": self.response.status,
                "code": self.response.status_code
            }

# Logger
Logger override for maintain app debugging.

# Encryption
Contain encrypt, decrypt functions for encryption.

Must add "CIPHER_PRIVATE_KEY" in your env:

    key = os.environ['CIPHER_PRIVATE_KEY']  # Must Be 16 char for AES128
