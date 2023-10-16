"""Services to connect with service."""
import math
from elasticsearch_dsl import Search, Q
from . import EsClient, SERVICE_CACHE_INDEX
from .exceptions import APIException


class ServiceBase(object):
    def __init__(self, service_id, units, raise_exception=False):
        self.service_id = service_id
        self.units = units or 1
        self._total_price = 0.0
        self._total_commission = 0.0
        self._total_discount = 0.0
        self._tax_amount = 0.0
        self._coupon_code = None
        self._coupon_id = None
        self._service_details = None
        self.is_valid_service = False

        index_query = Search(
            using=EsClient, index=SERVICE_CACHE_INDEX
        ).query("match", id=self.service_id)

        response = index_query.execute()
        if len(response.hits) < 1:
            if raise_exception:
                raise APIException("Service not found", 404)
        else:
            self._service_details = response.hits[0]
            self.is_valid_service = True

    @staticmethod
    def percentage(part, whole):
        return (float(part) * float(whole)) / 100

    @property
    def total_commission(self):
        return self._total_commission

    @property
    def service_details(self):
        if not self._service_details:
            raise APIException("Service details not found")
        return self._service_details

    @property
    def data(self):
        return self.service_details.to_dict()

    @property
    def total_discount(self):
        return self._total_discount

    @property
    def coupon_code(self):
        return self._coupon_code

    @property
    def coupon_id(self):
        return self._coupon_id

    @property
    def tax_details(self):
        return self.service_details.tax.to_dict()

    @property
    def total_price(self):
        return self._total_price


class PriceCatalog(ServiceBase):
    """
    Service price class to fetch service fee structure from `Elasticsearch` index.
    service_id: Respective service id,
    units: Units/quantity of service
    -----------------------------------------------------------------------------
    Call `ServicePrice(service_id, units).get_fee_details()` to get service fee details.

    """
    FLAT = 'FLAT'
    TIER_SPLIT = 'TIER_SPLIT'
    TIER_GROUPING = 'TIER_GROUPING'
    TIER_BUNDLE = 'TIER_BUNDLE'

    def get_fee_details(self, include_tax=False):
        """
        Return Service fee details based on service fee structure (FLAT/TIER).
        """
        response = dict()
        units = self.units
        obj = self.service_details

        response['service_name'] = obj.name
        response['short_code'] = obj.short_code
        response['service_price_type'] = obj.service_price_type

        obj.service_price_type = obj.service_price_type.upper()

        if obj.service_price_type == ServicePrice.FLAT:

            if not obj.service_price_type:
                raise APIException(
                    'Flat service fee structure pricing not available'
                )

            flat = obj.service_price_details[0]
            if flat.is_hard_cost_included:
                self._total_price = flat.hard_cost + flat.price
            else:
                self._total_price = flat.price

            self._total_price = units * self._total_price if flat.is_per_unit_cost else self._total_price

            response['hard_cost'] = flat.hard_cost
            response['total_price'] = self._total_price
            response['total_commission'] = self.get_commission_details(flat, self._total_price)
            response['amount_break_down'] = [flat.to_dict()]

        elif obj.service_price_type == ServicePrice.TIER_SPLIT:
            tiers = obj.service_price_details
            tiers = list(filter(lambda k: k.start_quantity <= units and k.tier_type == ServicePrice.TIER_SPLIT, tiers))
            tiers = sorted(tiers, key=lambda k: k.start_quantity)

            if not tiers:
                raise APIException(
                    'Tier service fee structure pricing not available'
                )

            # Removed as per client requirement
            # if tiers[0].unit_to and tiers[0].unit_to < units:
            #     raise APIException(
            #         'You can take max of ' + str(tiers[0].unit_to) + ' units'
            #     )

            total_price, total_commission = self.tier_split_price_generator(tiers)

            response['total_price'] = total_price
            response['total_commission'] = total_commission
            response['amount_break_down'] = [tier.to_dict() for tier in tiers]

        elif obj.service_price_type == ServicePrice.TIER_GROUPING:
            tiers_group = obj.service_price_details

            tiers_group = list(
                filter(
                    lambda k: (k.start_quantity <= units <= k.end_quantity or k.end_quantity == -1)
                              and (k.tier_type == ServicePrice.TIER_GROUPING),
                    tiers_group
                )
            )

            if not tiers_group:
                raise APIException(
                    'Tier service fee structure pricing not available'
                )

            tier_group = tiers_group[0]

            if tier_group.is_hard_cost_included:
                self._total_price = tier_group.hard_cost + tier_group.price
            else:
                self._total_price = tier_group.price

            self._total_price = units * self._total_price if tier_group.is_per_unit_cost else self._total_price

            response['hard_cost'] = tier_group.hard_cost
            response['total_price'] = self._total_price
            response['total_commission'] = self.get_commission_details(tier_group, self._total_price)
            response['amount_break_down'] = [tier_group.to_dict()]

        elif obj.service_price_type == ServicePrice.TIER_BUNDLE:
            tiers = obj.service_price_details
            tiers = list(filter(lambda k: k.start_quantity <= units and k.tier_type == ServicePrice.TIER_BUNDLE, tiers))
            tiers = sorted(tiers, key=lambda k: k.start_quantity)

            if not tiers:
                raise APIException(
                    'Tier service fee structure pricing not available'
                )

            total_price, total_commission = self.tier_bundle_price_generator(tiers)

            response['total_price'] = total_price
            response['total_commission'] = total_commission
            response['amount_break_down'] = [tier.to_dict() for tier in tiers]

        service_tax = getattr(obj, 'tax_details', None)
        if service_tax and service_tax.tax_percentage:
            self._tax_amount = self.get_service_tax(self._total_price)
            if include_tax:
                self._total_price += self._tax_amount

        response['total_price'] = self._total_price
        response['tax_amount'] = self._tax_amount
        response['tax_code'] = obj.unique_tax_code
        response['tax_percentage'] = getattr(service_tax, 'tax_percentage', None)

        return response

    def get_service_tax(self, total_price):
        service_tax = getattr(self.service_details, 'tax', None)
        tax_amount = self.percentage(total_price, getattr(service_tax, 'tax_percentage', 0))
        return tax_amount

    def tier_bundle_price_generator(self, tiers):
        """
        Return/calculate tier bundle based service price and commission.
        """
        units = self.units
        self._total_price = 0.0
        self._total_commission = 0.0

        for obj in tiers:
            if obj.end_quantity == -1:
                unit = units - (obj.start_quantity - 1)
            else:
                if obj.end_quantity and (obj.start_quantity <= units <= obj.end_quantity):
                    unit = units - (obj.start_quantity - 1)
                else:
                    unit = obj.end_quantity - (obj.start_quantity - 1)

            obj.total_price = obj.price * (math.ceil(unit / obj.tier_bundle_size))

            if obj.is_hard_cost_included:
                self._total_price = obj.hard_cost + obj.total_price

            self._total_commission += self.get_commission_details(obj, obj.total_price)
            self._total_price += obj.total_price
        return self._total_price, self._total_commission

    def tier_split_price_generator(self, tiers):
        """
        Return/calculate tier split based service price and commission.
        """
        units = self.units
        self._total_price = 0.0
        self._total_commission = 0.0

        for obj in tiers:
            if obj.end_quantity == -1:
                unit = units - (obj.start_quantity - 1)
            else:
                if obj.end_quantity and (obj.start_quantity <= units <= obj.end_quantity):
                    unit = units - (obj.start_quantity - 1)
                else:
                    unit = obj.end_quantity - (obj.start_quantity - 1)

            obj.total_price = unit * obj.price if obj.is_per_unit_cost else obj.price

            if obj.is_hard_cost_included:
                self._total_price = obj.hard_cost + obj.total_price

            self._total_commission += self.get_commission_details(obj, obj.total_price)
            self._total_price += obj.total_price
        return self._total_price, self._total_commission

    def get_commission_details(self, service_obj, service_price):
        """
        Calculates commission from ServiceCommissions.
        If The commission_type is Flat return commission as figure value.
        If The commission_type is PERCENTAGE Calculate commission
        by ((service_total_price*commission.figure_value)/100).
        """
        total_commission = 0.0

        if not getattr(service_obj, 'service_commission_details', None):
            return total_commission

        commission_obj = service_obj.service_commission_details[0]

        if commission_obj.commission_type == "FLAT":
            total_commission = commission_obj.commission_for_each
        else:
            total_commission = self.percentage(service_price, commission_obj.commission_for_each)

        self._total_commission = total_commission

        return total_commission


class CouponMixin(ServiceBase):
    """
    Coupon mixin class contains coupon related functions and validator.
    Add function and methods according to your need.
    """

    FLAT_COUPON = 'FLAT'
    PERCENTAGE_COUPON = 'PERCENTAGE'
    QUANTITY_COUPON = 'QUANTITY'

    @classmethod
    def get_coupon_by_id(cls, service_id, coupon_id, to_dict=False):
        """
        Return elastic search dsl object of coupon or None.
        to_dict: True will return dict obj of coupon.
        """
        coupon_obj = dict() if to_dict else None

        if service_id and coupon_id:
            result = Search(
                using=EsClient,
                index=SERVICE_CACHE_INDEX
            ).query('nested',
                    path='service_coupons',
                    query=Q('match',
                            service_coupons__id=coupon_id)).filter(
                Q('bool',
                  should=Q('match', id=service_id), minimum_should_match=1)).execute()
            if result and result.hits:
                coupon_obj = result.hits[0]
                if to_dict:
                    coupon_obj = coupon_obj.to_dict()

        return coupon_obj

    @classmethod
    def get_coupon_by_service(cls, service_id, coupon_code, to_dict=False):
        """
        Return elastic search dsl object of coupon or None.
        to_dict: True will return dict obj of coupon.
        """
        coupon_obj = None
        if service_id and coupon_code:
            result = Search(
                using=EsClient,
                index=SERVICE_CACHE_INDEX
            ).query('nested',
                    path='service_coupons',
                    query=Q('match',
                            service_coupons__name=coupon_code)).filter(
                Q('bool',
                  should=Q('match', id=service_id), minimum_should_match=1)).execute()
            if result and result.hits:
                coupon_obj = result.hits[0]
                if to_dict:
                    coupon_obj = coupon_obj.to_dict()

        return coupon_obj

    def get_coupon_from_service(self, coupon_code, service=None):
        """
        Returns coupon from service coupons list.
        """
        if not service:
            service = self.service_details

        coupon = list(
            filter(
                lambda coup: coup.name == coupon_code, service.service_coupons
            )
        )
        if coupon:
            return coupon[0]

        return None

    def get_coupon_details(self, coupon_code=None, **kwargs):
        """
        Fetch respective coupon from the service coupon index,
        Validate coupon price and apply on service total price.

        pass get_coupon_details(service_list=list(service_list))
        Service list is required to validate coupon of dependent services,
        If coupon is dependent on other service then we need to check that service
        is added in service list.
        """
        total_price = self.total_price
        coupons_to_apply = list()
        coupon_results = dict()

        coupon_code_list = kwargs.get('coupon_code_list') or list()
        availed_coupons = kwargs.get('availed_coupons') or list()
        service = self.service_details
        service_coupons = service.service_coupons or list()

        if coupon_code:
            coupon_code_list.append(coupon_code)

        for c_code in coupon_code_list:
            coupons_to_apply += list(
                filter(
                    lambda coup: coup.name == c_code and coup.name not in availed_coupons, service_coupons
                )
            )

        for coupon in service_coupons:
            if coupon.is_auto_apply and coupon.id not in [c.id for c in coupons_to_apply]:
                coupons_to_apply.append(coupon)

        filtered_coupon_list = []

        for coupon in coupons_to_apply:
            coupon.coupon_type = coupon.coupon_type.upper() if coupon.coupon_type else coupon.coupon_type
            if coupon.coupon_type == CouponMixin.PERCENTAGE_COUPON and self.units >= coupon.actual_service_quantity:
                coupon_value = round((coupon.discount_value / 100) * total_price, 2)
                coupon.coupon_value = min([coupon_value, total_price])
                filtered_coupon_list.append(coupon)
            elif coupon.coupon_type == CouponMixin.FLAT_COUPON and self.units >= coupon.actual_service_quantity:
                coupon_value = coupon.discount_value
                if total_price >= coupon_value:
                    filtered_coupon_list.append(coupon)
            elif coupon.coupon_type == CouponMixin.QUANTITY_COUPON and self.units >= coupon.actual_service_quantity:
                pass

        coupons_to_apply = filtered_coupon_list

        if coupons_to_apply:
            coupon_to_be_apply = self._get_coupon_with_max_discount(coupons_to_apply)

            if coupon_to_be_apply and (coupon_to_be_apply.discount_value * self.units) < total_price:
                self._total_discount = coupon_to_be_apply.discount_value
                self._coupon_code = coupon_to_be_apply.name
                self._coupon_id = coupon_to_be_apply.id

        coupon_results['total_discount'] = self._total_discount
        coupon_results['coupon_code'] = self._coupon_code
        coupon_results['coupon_id'] = self._coupon_id

        return coupon_results

    @classmethod
    def _get_coupon_with_max_discount(cls, coupon_list):
        if coupon_list:
            return max(coupon_list, key=lambda k: k.discount_value)

    @classmethod
    def _remove_coupon_from_list(cls, coupon_code, coupon_list):
        coupons_to_apply = []

        for coupon in coupon_list:
            if coupon.name != coupon_code:
                coupons_to_apply.append(coupon)

        return coupons_to_apply

    def validate_coupon_code(self, coupon_code: str, service_list=None, raise_exception=False, **kwargs):
        """
        Validates the coupon is valid with respect to service_list passed.
        Service list is required to validate coupon of dependent services,
        If coupon is dependent on other service then we need to check that service
        is added in service list.
        """
        is_valid_coupon = False
        service = self.service_details

        if not service_list:
            service_list = list()

        if service_list and kwargs.get('re_fetch'):
            coupon_search_query = Search(
                using=EsClient, index=SERVICE_CACHE_INDEX
            ).query('nested', path='service_coupons', query=Q('match', service_coupons__name=coupon_code)).filter(
                Q('bool',
                  should=[Q('match', id=service_id) for service_id in service_list],
                  minimum_should_match=1)
            )
            response = coupon_search_query.execute()
            if response and response.hits:
                is_valid_coupon = True
                service = response.hits[0]

        coupon = self.get_coupon_from_service(coupon_code, service)

        if coupon:
            if coupon.dependent_services:
                # Service list is required to validate coupon of dependent services,
                # If coupon is dependent on other service then we need to check that service
                # is added in service list.
                service_list = service_list or []
                is_valid_coupon = any(dependent.service_id in service_list for dependent in coupon.dependent_services)
            else:
                is_valid_coupon = True

        if not is_valid_coupon and raise_exception:
            raise APIException({'coupon_code': ['Invalid coupon code']})

        return is_valid_coupon


class ServicePrice(PriceCatalog, CouponMixin):
    """
    Service price class to fetch service fee structure from `Elasticsearch` index.
    service_id: Respective service id,
    units: Units/quantity of service
    -----------------------------------------------------------------------------
    Call `ServicePrice(service_id, units).get_fee_details()` to get service fee details.

    Add more functions & calculations acc. to your need.
    """

    pass


class ServiceValidator(object):
    """
    Validate service or service list passed to validator,
    search and validate service using service_id from `Elasticsearch`.
    """

    def __init__(self, service_id=None, raise_exception=False, **kwargs):
        """
        kwargs service_list: validates list of services.
        kwargs match_all: validates all services else validate at least one service.
        """
        self.is_valid_service = False
        self.service_list = kwargs.get('service_list') or list()
        self.minimum_should_match = 1
        if service_id:
            self.service_list.append(service_id)
        if kwargs.get('match_all'):
            self.minimum_should_match = len(self.service_list)

        self.is_valid_service = self.validate_service_list()

        if not self.is_valid_service and raise_exception:
            raise APIException("Invalid service")

    def validate_service_list(self):
        """
        Search and return bool of service exists in Elasticsearch or not.
        """
        result = Search(
            using=EsClient,
            index=SERVICE_CACHE_INDEX
        ).query(
            Q('bool',
              should=[Q('match', id=service_id) for service_id in self.service_list],
              minimum_should_match=self.minimum_should_match)
        ).execute()
        if result and result.hits:
            return True
        return False
