import datetime
from decimal import Decimal
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class Filter:

    query_relation_depth = 4
    exclude_from_terms = []
    query_float_fields = ['DecimalField', 'FloatField']
    query_char_fields = ['CharField', 'TextField']
    query_boolean_fields = ['BooleanField']
    query_date_fields = ['DateTimeField', 'DateField']
    query_int_fields = [
        'IntegerField', 'AutoField', 'BigAutoField', 'PositiveSmallIntegerField'
    ]

    LABEL_EXACT = _('Equals')
    LABEL_EXACT_NOT = _('Equals Not')
    LABEL_ICONTAINS = _('Contains')
    LABEL_ICONTAINS_NOT = _('Contains Not')
    LABEL_GTE = _('Greater or Equal')
    LABEL_LTE = _('Less or Equal')
    LABEL_TRUE = _('True')
    LABEL_FALSE = _('False')
    LABEL_SET = _('Is Set')
    LABEL_NOT_SET = _('Is Not Set')

    def __init__(
            self, model,
            query_relation_depth: int = 4,
            exclude_from_terms: list = None,
    ):
        self.model = model
        self.query_relation_depth = query_relation_depth
        self.exclude_from_terms = exclude_from_terms or []

    def get_choice_char_query_term(self, label, param, choices):
        choices = [(choice[0], str(choice[1])) for choice in choices]
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'selection',
                    'choices': choices,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_EXACT_NOT),
                    'data_type': 'selection',
                    'choices': choices,
                    'invert': True,
                    'param': 'exact'
                }
            ]
        }

    def get_char_query_term(self, label, param):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_ICONTAINS),
                    'data_type': 'text',
                    'param': 'icontains'
                },
                {
                    'label': str(self.LABEL_ICONTAINS_NOT),
                    'data_type': 'text',
                    'invert': True,
                    'param': 'icontains'
                },
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'text',
                    'param': 'exact'
                }
            ]
        }

    def get_float_query_term(self, label, param, step):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'number',
                    'step': step,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_EXACT_NOT),
                    'data_type': 'number',
                    'step': step,
                    'invert': True,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_GTE),
                    'data_type': 'number',
                    'step': step,
                    'param': 'gte'
                },
                {
                    'label': str(self.LABEL_LTE),
                    'data_type': 'number',
                    'step': step,
                    'param': 'lte'
                }
            ]
        }

    def get_int_query_term(self, label, param):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'number',
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_EXACT_NOT),
                    'data_type': 'number',
                    'invert': True,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_GTE),
                    'data_type': 'number',
                    'param': 'gte'
                },
                {
                    'label': str(self.LABEL_LTE),
                    'data_type': 'number',
                    'param': 'lte'
                }
            ]
        }

    def get_boolean_query_term(self, label, param):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_TRUE),
                    'data_type': 'bool',
                    'value': True,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_FALSE),
                    'data_type': 'bool',
                    'value': False,
                    'param': 'exact'
                }
            ]
        }

    def get_datetime_query_term(self, label, param):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'datetime-local',
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_EXACT_NOT),
                    'data_type': 'datetime-local',
                    'invert': True,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_GTE),
                    'data_type': 'datetime-local',
                    'param': 'gte'
                },
                {
                    'label': str(self.LABEL_LTE),
                    'data_type': 'datetime-local',
                    'param': 'lte'
                }
            ]
        }

    def get_date_query_term(self, label, param):
        return {
            'label': str(label),
            'param': param,
            'params': [
                {
                    'label': str(self.LABEL_EXACT),
                    'data_type': 'date',
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_EXACT_NOT),
                    'data_type': 'date',
                    'invert': True,
                    'param': 'exact'
                },
                {
                    'label': str(self.LABEL_GTE),
                    'data_type': 'date',
                    'param': 'gte'
                },
                {
                    'label': str(self.LABEL_LTE),
                    'data_type': 'date',
                    'param': 'lte'
                }
            ]
        }

    def get_null_params(self):
        return [
            {
                'label': str(self.LABEL_SET),
                'data_type': 'bool',
                'value': False,
                'param': 'isnull'
            },
            {
                'label': str(self.LABEL_NOT_SET),
                'data_type': 'bool',
                'value': True,
                'param': 'isnull'
            }
        ]

    def cast_decimal_places_to_step(self, descimal_places):
        if not descimal_places or descimal_places < 1:
            return '1'
        zero_count = descimal_places - 1
        return f'0.{"0" * zero_count}1'

    def get_query_term(self, field):
        internal_type = field.get_internal_type()
        label = str(field.verbose_name)
        param = str(field.name)
        if internal_type in self.query_char_fields:
            if field.choices:
                return self.get_choice_char_query_term(label, param, field.choices)
            return self.get_char_query_term(label, param)
        elif internal_type in self.query_float_fields:
            return self.get_float_query_term(
                label, param, self.cast_decimal_places_to_step(field.decimal_places or 0)
            )
        elif internal_type in self.query_int_fields:
            return self.get_int_query_term(label, param)
        elif internal_type in self.query_boolean_fields:
            return self.get_boolean_query_term(label, param)
        elif internal_type in self.query_date_fields:
            return self.get_date_query_term(label, param)

    def get_searchable_method_term(self, model, method):
        method_name = method['name']
        param = '_c_' + method_name
        method_label = str(method.get('label', method_name.capitalize()))
        func = getattr(model, method['name'])
        return_type = func.__annotations__.get('return')
        if return_type == str:
            return self.get_char_query_term(method_label, param)
        elif return_type == int:
            return self.get_int_query_term(method_label, param)
        elif return_type in [float, Decimal]:
            return self.get_float_query_term(method_label, param, 0)
        elif return_type == bool:
            return self.get_boolean_query_term(method_label, param)
        elif return_type == datetime.datetime:
            return self.get_datetime_query_term(method_label, param)
        elif return_type == datetime.date:
            return self.get_date_query_term(method_label, param)

    def get_relation_query_terms(self, model, path):
        terms = []
        if 'tenant' not in self.exclude_from_terms:
            self.exclude_from_terms.append('tenant')
        fields = filter(
            lambda x:
            x.is_relation and
            x.name not in self.exclude_from_terms,
            sorted(model._meta.get_fields(), key=lambda x: x.name.lower())
        )
        cpath = path.copy()
        for field in fields:
            if field.related_model not in cpath:
                cpath.append(field.related_model)
                try:
                    label = field.verbose_name
                except AttributeError:
                    label = field.related_model._meta.verbose_name
                rel_term = {
                    'label': str(label),
                    'param': field.name,
                    'params': self._get_query_terms(field.related_model, cpath)
                }
                rel_term['params'] = self.get_null_params() + rel_term['params']
                if rel_term['params']:
                    terms.append(rel_term)
        return terms

    def get_local_query_terms(self, model):
        terms = []
        fields = filter(lambda x: not x.is_relation, model._meta.get_fields())
        searchable_methods = []
        if hasattr(model, 'searchable_methods'):
            searchable_methods = model.searchable_methods
        for field in fields:
            term = self.get_query_term(field)
            if field.null is True and term.get('params'):
                term['params'].extend(self.get_null_params())
            if term is not None:
                terms.append(term)
        for searchable_method in searchable_methods:
            terms.append(self.get_searchable_method_term(model, searchable_method))
        terms = sorted(terms, key=lambda x: x['label'])
        return terms

    def _get_query_terms(self, model=None, path=None):
        if model is None:
            model = self.model
            path = [model]
        terms = []
        terms.extend(self.get_local_query_terms(model))
        if len(path) <= self.query_relation_depth:
            terms.extend(self.get_relation_query_terms(model, path))
        return terms

    def get_query_terms(self):
        key = f'query-terms-{self.model.__module__}.{self.model.__name__}'
        terms = cache.get(key)
        if not terms:
            terms = self._get_query_terms()
            cache.set(key, terms, 60 * 15)
        return terms
