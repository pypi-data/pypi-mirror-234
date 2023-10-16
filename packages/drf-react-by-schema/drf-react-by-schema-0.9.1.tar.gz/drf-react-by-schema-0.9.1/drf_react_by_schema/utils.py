import re
import operator
import functools
from django.db.models import Q, Count, Case, When, IntegerField
from django.apps import apps


def is_tmp_id(id):
    if not id:
        return True
    return str(id)[:3] == 'tmp'


def update_simple_related_objects(**kwargs):
    instance = kwargs['instance']
    key = kwargs['key']
    related_objects_data = kwargs['related_objects_data']
    related_objects_data_ids = []
    for related_obj in related_objects_data:
        if not related_obj.get('id', None):
            # Create new related object with this label:
            labelKey = kwargs.pop('labelKey', 'nome')
            related_object_model = getattr(instance, key).model
            new_related_object_name = related_obj.get('label', None)
            if not new_related_object_name:
                continue
            new_related_object_data = {labelKey: new_related_object_name}
            try:
                (new_related_obj, created) = related_object_model.objects.get_or_create(
                    **new_related_object_data)
            except:
                continue
            related_objects_data_ids.append(new_related_obj.id)
        else:
            related_objects_data_ids.append(related_obj['id'])
    getattr(instance, key).set(related_objects_data_ids)
    for related_object in getattr(instance, key).all():
        if not related_object.id in related_objects_data_ids:
            getattr(instance, key).remove(related_object)
    return instance


def update_foreignkey(**kwargs):
    instance = kwargs['instance']
    key = kwargs['key']
    related_object_model = kwargs['related_object_model']
    old_related_object = getattr(instance, key)
    related_object_id = kwargs['related_object_id']

    if related_object_id:
        try:
            related_object = related_object_model.objects.get(
                pk=related_object_id)
            if not old_related_object or related_object.id != old_related_object.id:
                setattr(instance, key, related_object)
            return instance
        except:
            pass

    if not old_related_object is None:
        setattr(instance, key, None)

    return instance


def create_or_update_foreignkey(**kwargs):
    labelKey = kwargs.pop('labelKey', 'nome')
    data = kwargs.pop('data', None)
    kwargs['related_object_id'] = data
    if type(data) is dict:
        kwargs['related_object_id'] = data.pop('id', None)
        if 'label' in data:
            data[labelKey] = data.pop('label')

        if is_tmp_id(kwargs['related_object_id']) and data.get(labelKey, None):
            related_object_model = kwargs['related_object_model']
            (related_object, created) = related_object_model.objects.get_or_create(**data)
            kwargs['related_object_id'] = related_object.id
    return update_foreignkey(**kwargs)


def get_model(app, model_name):
    if not app or not model_name:
        return None
    return apps.get_model(app_label=app, model_name=model_name)


def camel_to_snake(name, suffix=None):
    if suffix:
        name = name.removesuffix(suffix)
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def apply_data_grid_filter(qs, serializer, column_field, operator_value, value):
    field = serializer.fields.get(column_field, None)
    if field is None:
        return qs
    source_field = field.source.replace('.', '__')
    if getattr(field, 'label_field', None):
        source_field += f"__{field.label_field}"

    if operator_value == 'contains' and value:
        return qs.filter(**{f"{source_field}__icontains": value})
    if operator_value == 'equals' and value:
        return qs.filter(**{f"{source_field}__iexact": value})
    if operator_value == 'startsWith' and value:
        return qs.filter(**{f"{source_field}__istartswith": value})
    if operator_value == 'endsWith' and value:
        return qs.filter(**{f"{source_field}__iendswith": value})
    if operator_value == 'isEmpty':
        if field.__class__.__name__ in ['DateField', 'DecimalField', 'IntegerField']:
            return qs.filter(Q(**{f"{source_field}__isnull": True}))
        return qs.filter(
            Q(**{f"{source_field}__isnull": True}) |
            Q(**{f"{source_field}": ''})
        )
    if operator_value == 'isNotEmpty':
        if field.__class__.__name__ in ['DateField', 'DecimalField', 'IntegerField']:
            return qs.exclude(Q(**{f"{source_field}__isnull": True}))
        return qs.exclude(
            Q(**{f"{source_field}__isnull": True}) |
            Q(**{f"{source_field}": ''})
        )
    if operator_value == 'isAnyOf' and value:
        values = value.split(',')
        if field.__class__.__name__ in ['DecimalField', 'IntegerField']:
            condition = functools.reduce(
                operator.or_, [Q(**{f"{source_field}": item})
                               for item in values]
            )
            return qs.filter(condition)
        condition = functools.reduce(
            operator.or_, [Q(**{f"{source_field}__iexact": item})
                           for item in values]
        )
        return qs.filter(condition)

    # DATE filters:
    if operator_value == 'is' and value:
        return qs.filter(**{f"{source_field}": value})
    if operator_value == 'not' and value:
        return qs.exclude(**{f"{source_field}": value})
    if operator_value == 'after' and value:
        return qs.filter(**{f"{source_field}__gt": value})
    if operator_value == 'before' and value:
        return qs.filter(**{f"{source_field}__lt": value})
    if operator_value == 'onOrAfter' and value:
        return qs.filter(**{f"{source_field}__gte": value})
    if operator_value == 'onOrBefore' and value:
        return qs.filter(**{f"{source_field}__lte": value})
    if operator_value == 'entre' and value:
        values = value.split(',')
        if len(values) == 2 and values[0] and values[1]:
            return qs.filter(**{
                f"{source_field}__gte": values[0],
                f"{source_field}__lte": values[1]
            })
        elif values[0]:
            return qs.filter(**{f"{source_field}__gte": values[0]})
        elif values[1]:
            return qs.filter(**{f"{source_field}__lte": values[1]})

    # NUMBER filters:
    if operator_value == '=' and value:
        return qs.filter(**{f"{source_field}": value})
    if operator_value == '!=' and value:
        return qs.exclude(**{f"{source_field}": value})
    if operator_value == '>' and value:
        return qs.filter(**{f"{source_field}__gt": value})
    if operator_value == '>=' and value:
        return qs.filter(**{f"{source_field}__gte": value})
    if operator_value == '<' and value:
        return qs.filter(**{f"{source_field}__lt": value})
    if operator_value == '<=' and value:
        return qs.filter(**{f"{source_field}__lte": value})

    return qs


def get_target_field(view, field, prefix=None):
    field_name = getattr(field, 'name', None)
    related_model = getattr(field, 'related_model', None)
    if related_model is None:
        if field_name is not None:
            return f"{prefix}__{field_name}" if prefix else field_name
    else:
        related_model_fields = related_model._meta.get_fields()
        related_model_serializer = view.serializer_class().fields.get(field_name)
        # TODO: Check why ManyToMany fields have no "label_field" in serializer.
        # Without the label_field, It's not possible to add this model to search and filters.
        label_field = getattr(related_model_serializer, 'label_field', None)
        if label_field:
            for related_model_field in related_model_fields:
                related_model_field_name = getattr(
                    related_model_field, 'name', None)
                if related_model_field_name == label_field:
                    return f"{prefix}__{field_name}__{related_model_field_name}" if prefix else f"{field_name}__{related_model_field_name}"
    return None


def serializer_to_model_field(view, serializer_field):
    if serializer_field is None or serializer_field.source == 'id':
        return None

    field_sources = serializer_field.source.split('.')
    field = None
    first_field_source = field_sources.pop(0)
    if first_field_source == '*':
        return None

    try:
        field = view.model._meta.get_field(first_field_source)
    except:
        pass  # Serializer field doesnt exist in model

    if field or len(field_sources) > 0:
        target_field = None
        if len(field_sources) == 0:
            target_field = get_target_field(view, field)
        else:
            related_model = getattr(field, 'related_model', None)

            if len(field_sources) == 1:
                field = related_model._meta.get_field(
                    field_sources[0])
                target_field = get_target_field(
                    view, field, first_field_source)

            if len(field_sources) == 2:
                second_field = related_model._meta.get_field(
                    field_sources[0])
                second_related_model = getattr(
                    second_field, 'related_model', None)
                third_field = second_related_model._meta.get_field(
                    field_sources[1])
                prefix = f"{first_field_source}__{second_field.name}"
                target_field = get_target_field(
                    view, third_field, prefix)

        return target_field

    return serializer_field.source


def serializer_to_model_fields(view, fields_raw):
    fields = []
    for field_raw in fields_raw:
        field = field_raw[1:] if field_raw.startswith("-") else field_raw
        serializer_field = view.serializer_class().fields.get(field, None)
        target_field = serializer_to_model_field(view, serializer_field)
        if target_field:
            fields.append(
                f"-{target_field}" if field_raw.startswith("-") else target_field)

    return fields if len(fields) > 0 else None
