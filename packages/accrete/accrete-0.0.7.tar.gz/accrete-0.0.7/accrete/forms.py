import logging
from uuid import uuid4
from functools import partial

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import transaction
from accrete.tenant import get_tenant
from accrete.models import Tenant
from accrete.queries import is_member

_logger = logging.getLogger(__name__)
User = get_user_model()


class One2ManyModelForm(forms.ModelForm):
    """
    Template Access:
    In Templates/Forms the generated fields can be accessed via
    form.get_>>related_name<< e.g. form.get_items returns
    a list of dictionaries containing the fields.

    Cleaning:
    For every One2Many field, clean_>>related_name<< is called.
    To clean all entries together, self.cleaned_data[>>related_name<<] is
    available in clean() containing a list of all entries

    Initial data can be supplied by creating a form method called
    get_initial_>>related_name<<_>>field_name<< which takes the
    related instance as a parameter
    or by setting an attribute on the model which can be a callable


    One2Many field configuration:
    o2m_fields = {
        # related_name
        'items': {
            # field that holds the key to self.model
            'fk_field': 'pricelist',
            # Order by the given fields value, can be prefixed by '-' to
            # control ascending/descending order
            'order': '-pk'
            # fields of the related model that are needed in the form
            'fields': {
                # pk field must be present for updating existing rows.
                # Otherwise, all related objects will be deleted and recreated
                # upon saving.
                'pk': {
                    'field_class': partial(
                        forms.IntegerField,
                        required=False,
                        widget=forms.HiddenInput
                    ),
                    # if only data is sent with fields that have
                    # "count_as_empty" set to true, the whole fieldset is
                    # ignored and won't be added to self.fields
                    'count_as_empty': True
                },
                'product': {
                    'field_class': partial(
                        forms.ModelChoiceField,
                        Product.objects.all(),
                        label=_('Product')
                    )
                }
            }
        }
    }
    """
    o2m_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.o2m_keys = None
        if self.instance and self.instance.pk and not kwargs.get('data'):
            self.add_instance_o2m_objects()
        else:
            self.add_o2m_fields(**kwargs)
        self.add_o2m_getter()

    def add_instance_o2m_objects(self):
        self.o2m_keys = set()
        for field in self.o2m_fields.keys():
            related_objects = getattr(self.instance, field)
            for o in related_objects.all():
                field_key = f'{field}_{str(uuid4())[:8]}'
                for k, v in self.o2m_fields[field]['fields'].items():
                    func_name = f'get_initial_{field}_{k}'
                    field_name = f'{field_key}-{k}'
                    self.fields[field_name] = v['field_class']()
                    if hasattr(self, func_name):
                        initial = getattr(self, func_name)(o)
                    else:
                        initial = getattr(o, k) if hasattr(o, k) else False
                    if callable(self.fields[field_name].initial):
                        initial = initial()
                    self.fields[field_name].initial = initial
                self.o2m_keys.add(field_key)

    def add_o2m_fields(self, **kwargs):
        self.o2m_keys = set()
        data = kwargs.get('data', {})
        for field, config in self.o2m_fields.items():
            fields = config['fields']
            field_keys = set(
                k.split('-')[0] for k in data.keys() if k.startswith(field)
            )
            if not field_keys:
                field_keys = set(
                    f'{k}_1' for k in self.o2m_fields.keys()
                )
            for field_key in field_keys:
                to_add = any([
                    data.get(f'{field_key}-{name}')
                    for name in list(fields.keys())
                    if not fields.get(f'{name}', {}).get('count_as_empty')
                ])
                if to_add:
                    for k, v in fields.items():
                        fname = f'{field_key}-{k}'
                        self.fields[fname] = v['field_class']()
                        self.fields[fname].initial = kwargs.get(fname)
                    self.o2m_keys.add(field_key)

    def add_o2m_getter(self):
        for k in self.o2m_fields.keys():
            func_name = f'get_{k}'
            setattr(self, func_name, partial(self.get_o2m_fields, k))

    def get_o2m_fields(self, prefix):
        fields = []
        for k in self.o2m_keys:
            if k.startswith(prefix):
                fnames = list(
                    self.o2m_fields.get(prefix, {}).get('fields', [])
                )
                fields.append({
                    fname: self[f'{k}-{fname}']
                    for fname in fnames
                })

        order = self.o2m_fields.get(prefix, {}).get('order')
        reverse = False
        if order and order.startswith('-'):
            order = order[1:]
            reverse = True
        if order and fields:
            fields = sorted(
                fields, key=lambda x: x[order].value(), reverse=reverse
            )
        return fields

    def _clean_fields(self):
        super()._clean_fields()
        self._clean_o2m_fields()

    def _clean_o2m_fields(self):
        for related_name, related_field_config in self.o2m_fields.items():
            self.cleaned_data[related_name] = []
            fields = related_field_config['fields'].keys()
            entries = filter(
                lambda x: x.startswith(related_name), self.o2m_keys
            )
            for entry in entries:
                value = {
                    fname: self.cleaned_data.get(f'{entry}-{fname}')
                    for fname in fields
                }
                try:
                    self.cleaned_data[related_name].append(
                        getattr(self, f'clean_{related_name}')(value)
                    )
                except AttributeError:
                    self.cleaned_data[related_name].append(value)
                except forms.ValidationError as error:
                    self.add_error(entry, error)

    def save_o2m(self):
        for field in self.o2m_fields.keys():
            fk_field = self.o2m_fields[field].get('fk_field')
            if not fk_field:
                raise KeyError(
                    'One2Many Form definition is missing the '
                    f'"fk_field" attribute on field {field}'
                )

            related_objects = getattr(self.instance, field)
            if not self.cleaned_data.get(field, []):
                related_objects.all().delete()

            related_object_fields = [
                field.name for field
                in related_objects.model._meta.get_fields()
            ]
            update_pks, to_update, to_create = [], [], []

            for item in self.cleaned_data.get(field, []):
                item.update({fk_field: self.instance})
                if pk := item.get('pk'):
                    update_pks.append(pk)
                    to_update.append(item)
                else:
                    to_create.append(item)

            qs = related_objects.filter(pk__in=update_pks).order_by('pk')
            related_objects.exclude(pk__in=update_pks).delete()
            to_update = sorted(to_update, key=lambda x: x['pk'])
            if qs.count() != len(to_update):
                raise ValueError(
                    'Mismatching length of found objects and update data'
                )
            updated = []
            for obj, update in zip(qs, to_update):
                for k, v in update.items():
                    if k not in related_object_fields:
                        continue
                    setattr(obj, k, v)
                    updated.append(obj)
            objects_to_create = []
            for c in to_create:
                values = {}
                for k, v in c.items():
                    if k in related_object_fields:
                        values.update({k: v})
                objects_to_create.append(related_objects.model(**values))
            if updated:
                field_list = [
                    f for f in to_update[0].keys()
                    if f in related_object_fields
                ]
                related_objects.bulk_update(
                    updated, fields=field_list
                )
            if to_create:
                related_objects.bulk_create(objects_to_create)

    def save(self, commit=True):
        super().save(commit=commit)
        if commit:
            self.save_o2m()
        return self.instance


class TenantForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.tenant = get_tenant()
        super().__init__(*args, **kwargs)
        fields_to_filter = filter(
            lambda x:
            hasattr(x, 'queryset') and hasattr(x.queryset.model, 'tenant'),
            self.fields.values()
        )
        for field in fields_to_filter:
            field.queryset = field.queryset.filter(tenant=self.tenant)


class TenantModelForm(One2ManyModelForm):

    def __init__(self, *args, **kwargs):
        self.tenant = get_tenant()
        super().__init__(*args, **kwargs)
        fields_to_filter = filter(
            lambda x:
            hasattr(x, 'queryset') and hasattr(x.queryset.model, 'tenant'),
            self.fields.values()
        )
        for field in fields_to_filter:
            field.queryset = field.queryset.filter(tenant=self.tenant)

    def save_o2m(self):
        o2m_fields = self.o2m_fields.keys()
        for field in o2m_fields:
            for item in self.cleaned_data.get(field, []):
                item.update({'tenant': self.tenant})
        return super().save_o2m()

    def save(self, commit=True):
        super().save(commit=False)
        if not self.instance.pk or not self.instance.tenant:
            self.instance.tenant = self.tenant

        if commit:
            self.instance.save()
            self.save_m2m()
            self.save_o2m()

        return self.instance


def save_form(form, reraise=False):
    form.is_saved = False
    try:
        if form.is_valid():
            with transaction.atomic():
                form.save()
            form.is_saved = True
    except Exception as e:
        error_id = str(uuid4())[:8]
        _logger.exception(f'{error_id}: {e}')
        form.save_error = e
        form.save_error_id = error_id
        if reraise:
            raise e
    return form