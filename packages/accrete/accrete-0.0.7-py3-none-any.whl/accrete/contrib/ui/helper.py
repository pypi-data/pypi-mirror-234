import datetime
import logging
import json
from dataclasses import dataclass, field
from django.db.models.functions import Lower
from django.db.models import Model, QuerySet, Q, CharField, Manager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
from accrete.contrib.ui.filter import Filter
from . import config

_logger = logging.getLogger(__name__)

ACTIONS_TEMPLATE = config.ACCRETE_UI_ACTIONS_TEMPLATE


@dataclass
class ClientAction:

    name: str
    url: str = None
    submit: bool = False
    form_id: str = 'form'
    class_list: list = field(default_factory=list)
    mobile: bool = True
    tablet: bool = True


def parse_client_actions(actions: list[ClientAction], actions_template: str = None):
    tablet = (not all(action.tablet for action in actions))
    mobile = (not all(action.mobile for action in actions))
    return {
        'actions_template': actions_template or ACTIONS_TEMPLATE,
        'actions': actions,
        'action_button': {'mobile': mobile, 'tablet': tablet}
    }


@dataclass
class BreadCrumb:

    name: str
    url:str


@dataclass
class ListContext:

    model: type[Model]
    get_params: dict
    title: str = None
    context: dict = field(default_factory=dict)
    queryset: QuerySet = None
    extra_query: Q = None
    related_fields: list[str] = field(default_factory=list)
    prefetch_fields: list[str] = field(default_factory=list)
    paginate_by: int = 20
    order_by: list[str] = None
    column_width: int = 12
    filter_relation_depth: int = 4
    actions: list[ClientAction] = field(default_factory=list)
    breadcrumbs: list[BreadCrumb] = field(default_factory=list)

    def get_queryset(self):
        order = self.get_order()
        if isinstance(order, str):
            if order == 'None':
                order = None
        return (self.queryset or queryset_from_querystring(
            self.model, self.get_params.get('q', '[]'), order)
                .filter(self.extra_query or Q())
                .select_related(*self.related_fields)
                .prefetch_related(*self.prefetch_fields)
                .distinct())

    def get_page_number(self, paginator):
        page_number = self.get_params.get('page', '1')

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        if page_number < 1:
            page_number = 1
        elif page_number > paginator.num_pages:
            page_number = paginator.num_pages
        return page_number

    def get_order(self):
        return self.get_params.get('order_by', None) or self.order_by

    def get_paginate_by(self):
        paginate_by = self.get_params.get('paginate_by', self.paginate_by)
        try:
            paginate_by = int(paginate_by)
        except ValueError:
            paginate_by = self.paginate_by
        return paginate_by

    def get_context(self):
        paginate_by = self.get_paginate_by()
        paginator = Paginator(self.get_queryset(), paginate_by)
        page = paginator.page(self.get_page_number(paginator))
        context = {
            'paginate_by': paginate_by,
            'order_by': self.get_params.get('order_by', self.model._meta.ordering),
            'paginator': paginator,
            'page': page,
            'list_pagination': True,
            'column_width': self.column_width,
            'title': self.title or self.model._meta.verbose_name_plural,
            'filter_terms': Filter(self.model, self.filter_relation_depth).get_query_terms(),
            'view_type': 'list',
            'breadcrumbs': self.breadcrumbs,
            'querystring': build_querystring(self.get_params)
        }
        if self.actions:
            context.update(parse_client_actions(self.actions))
        context.update(self.context)
        return context


@dataclass
class DetailContext:

    obj: Model
    get_params: dict
    order_by: str = None
    paginate_by: int = 20
    title: str = None
    queryset: type[QuerySet] = None
    extra_query: Q = None
    related_fields: list[str] = field(default_factory=list)
    prefetch_fields: list[str] = field(default_factory=list)
    actions: list[ClientAction] = field(default_factory=list)
    breadcrumbs: list[BreadCrumb] = field(default_factory=list)

    def get_queryset(self):
        order = self.get_order()
        if isinstance(order, str):
            if order == 'None':
                order = None
        return (self.queryset or queryset_from_querystring(
            self.obj._meta.model, self.get_params.get('q', '[]'), order)
                .filter(self.extra_query or Q())
                .select_related(*self.related_fields)
                .prefetch_related(*self.prefetch_fields)
                .distinct())

    def get_order(self):
        return self.get_params.get('order_by', None) or self.order_by

    def get_paginate_by(self):
        paginate_by = self.get_params.get('paginate_by', self.paginate_by)
        try:
            paginate_by = int(paginate_by)
        except ValueError:
            paginate_by = self.paginate_by
        return paginate_by

    def get_pagination_context(self):
        if not hasattr(self.obj, 'get_absolute_url'):
            _logger.warning(
                'Detail pagination disabled for models without the '
                'get_absolute_url attribute. Set paginate_by to 0 to '
                'deactivate pagination.'
            )
            return {}
        queryset = self.get_queryset()
        idx = (*queryset,).index(self.obj)
        previous_object_url = (
            queryset[idx - 1] if idx - 1 >= 0 else queryset.last()
        ).get_absolute_url()
        next_object_url = (
            queryset[idx + 1] if idx + 1 <= queryset.count() - 1 else queryset.first()
        ).get_absolute_url()
        ctx = {
            'previous_object_url': previous_object_url,
            'next_object_url': next_object_url,
            'current_object_idx': idx + 1,
            'total_objects': queryset.count(),
            'detail_pagination': True
        }
        return ctx

    def get_context(self):
        paginate_by = self.get_paginate_by()
        ctx = {
            'object': self.obj,
            'title': self.title or self.obj,
            'order_by': self.get_params.get('order_by', self.obj._meta.model._meta.ordering),
            'paginate_by': paginate_by,
            'detail_pagination': False,
            'view_type': 'detail',
            'breadcrumbs': self.breadcrumbs,
            'querystring': build_querystring(self.get_params, ['page'])
        }
        if self.paginate_by > 0:
            ctx.update(self.get_pagination_context())
        if self.actions:
            ctx.update(parse_client_actions(self.actions))
        return ctx


@dataclass
class FormContext:

    model: Model|type[Model]
    get_params: dict
    title: str = None
    context: dict = field(default_factory=dict)
    form_id: str = 'form'
    add_default_actions: bool = True
    discard_url: str = None

    def get_default_form_actions(self):
        actions = [
            ClientAction(
                name=_('Save'),
                submit=True,
                class_list=['is-success'],
                form_id=self.form_id
            )
        ]
        try:
            url = self.discard_url or self.model.get_absolute_url()
        except TypeError as e:
            _logger.exception(
                'Supply the discard_url parameter if FormContext is called '
                'with a model class instead of an instance.'
            )
            raise e
        except AttributeError as e:
            _logger.error(
                'Supply the discard_url parameter if FormContext is '
                'called with a model instance that has the get_absolute_url '
                'method not defined.'
            )
            raise e

        actions.append(
            ClientAction(
                name=_('Discard'),
                url=url
            )
        )
        return actions

    def get_title(self):
        if self.title:
            return self.title
        try:
            int(self.model.pk)
            return f'Edit {self.model}'
        except TypeError:
            return f'Add {self.model._meta.verbose_name}'

    def get_context(self):
        ctx = {
            'title': self.get_title(),
            'view_type': 'form',
            'form_id': self.form_id,
            'querystring': build_querystring(self.get_params, ['page'])
        }
        if self.add_default_actions:
            ctx.update(parse_client_actions(self.get_default_form_actions()))
        ctx.update(self.context)
        return ctx


def build_querystring(get_params: dict, extra_params: list[str] = None) -> str:
    querystring = f'?q={get_params.get("q", "[]")}'
    if paginate_by := get_params.get('paginate_by', False):
        querystring += f'&paginate_by={paginate_by}'
    if order_by := get_params.get('order_by', False):
        querystring += f'&order_by={order_by}'
    for param in extra_params or []:
        if value := get_params.get(param, False):
            querystring += f'&{param}={value}'
    return querystring


def queryset_from_querystring(
        model: type[Model|Manager],
        query_string: str,
        order_by: str|list[str] = None,
) -> QuerySet:
    """
    param url_query_string: json serializable string
    [[{"name__iexact": "asdf"}, {"active": true}], [{"group__name__isnull": false}]]
    """

    if not isinstance(model, Manager):
        model = model.objects

    query_data = json.loads(query_string)
    query = Q()

    for query_block in query_data:
        block_query = Q()
        for query_term in query_block:
            if isinstance(query_term, dict):
                for param, value in query_term.items():
                    block_query &= get_query(model.model, param, value)
            elif isinstance(query_term, list):
                inner_block_query = Q()
                for inner_query_term in query_term:
                    for param, value in inner_query_term.items():
                        inner_block_query |= get_query(model.model, param, value)
                block_query &= inner_block_query
        query |= block_query

    queryset = model.filter(query)

    if order_by is None:
        return queryset

    try:
        order = order_by.split(',')
    except AttributeError:
        order = order_by or []

    for o in order_by:
        desc = False
        if o.startswith('-'):
            o = o[1:]
            desc = True
        try:
            model_field = model.model._meta.get_field(o)
        except FieldDoesNotExist:
            model_field = None
            if o == 'pk':
                pass
        if isinstance(model_field, CharField):
            if desc:
                order.append(Lower(o).desc())
            else:
                order.append(Lower(o).asc())
        else:
            order.append(f'{"-" if desc else ""}{o}')
    return queryset.order_by(*order)


def get_related_model(model, path):
    related_model = model
    for part in path:
        try:
            related_model = related_model._meta.fields_map[part].related_model
            continue
        except (AttributeError, KeyError):
            pass
        # try:
        #     related_model = getattr(related_model, part).model
        #     continue
        # except AttributeError:
        #     pass
        # try:
        #     related_model = getattr(related_model.rel.related_model, part)
        #     continue
        # except AttributeError:
        #     pass
        # try:
        #     related_model = getattr(related_model, part).field.related_model
        #     continue
        # except AttributeError:
        #     pass
        raise AttributeError(
            f'Could not resolve relation for model: {model} with path "{path}" at {part}'
        )
    return related_model


def get_query(model, param: str, value) -> Q:
    invert = False
    parts = param.split('__')
    if param.startswith('~'):
        param = param[1:]
        invert = True
    if len(parts) == 1:
        parts.append('exact')
    attribute = parts[-2]

    if not attribute.startswith('_c_'):
        query = Q(**{param: value})
        return ~query if invert else query

    operator = parts[-1]
    related_model = get_related_model(model, parts[:-2])
    func = getattr(related_model, attribute[3:])

    obj_ids = [
        obj.id for obj in
        filter(
            lambda instance:
            evaluate(instance, func, value, operator),
            related_model.objects.all()
        )
    ]

    query = Q(**{
        f'{"__".join(parts[:-2])}{"__" if parts[:-2] else ""}id__in': obj_ids
    })
    return ~query if invert else query


def evaluate(instance, func, value, operator):
    return_type = func.__annotations__.get('return', str)
    try:
        value = return_type(value)
    except TypeError as e:
        if isinstance(return_type, datetime.datetime):
            value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        elif isinstance(return_type, datetime.date):
            value = datetime.datetime.strptime(value, '%Y-%m-%d')
        else:
            raise e

    return_value = func(instance)

    if operator == 'exact':
        return value == return_value
    elif operator == 'icontains':
        return value.lower() in return_value.lower()
    elif operator == 'contains':
        return value in return_value
    elif operator == 'gt':
        return return_value > value
    elif operator == 'gte':
        return return_value >= value
    elif operator == 'lte':
        return return_value <= value
    elif operator == 'lt':
        return return_value < value
