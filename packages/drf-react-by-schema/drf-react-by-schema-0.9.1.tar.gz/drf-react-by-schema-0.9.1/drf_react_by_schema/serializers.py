from django.apps import apps
from rest_framework import serializers

from . import settings, autocomplete_serializers
from .utils import (
    update_foreignkey,
    create_or_update_foreignkey,
    update_simple_related_objects,
    get_model
)

class GenericSerializer(autocomplete_serializers.GenericAutocompleteSerializer):
    update_related = []
    model_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_fields = self.Meta.model._meta.get_fields()
        for field in self.model_fields:
            field_class_name = field.__class__.__name__
            if field.related_model:
                serializer = getattr(
                    autocomplete_serializers, f"{field.related_model.__name__}Serializer", None)
                # TODO: rename label to verbose_name in ForeignKey
                field_label = getattr(field, 'label', '')
                label = getattr(field, 'verbose_name', None)
                if not label:
                    label = field_label if field_label != '' else getattr(
                        field.related_model._meta, 'verbose_name', field.related_model.__name__)
                if field_class_name == 'OneToOneField':
                    self.update_related.append(field.name)
                    if serializer:
                        self.fields[field.name] = serializer(
                            read_only=True, label=label)
                    continue
                if field_class_name == 'ForeignKey':
                    if getattr(field, 'related_editable', False):
                        self.update_related.append((field.name, 'creatable'))
                    else:
                        self.update_related.append(field.name)
                    if serializer:
                        self.fields[field.name] = serializer(
                            read_only=True, label=label)
                    continue
                if field_class_name == 'ManyToManyField':
                    self.update_related.append((field.name, 'many'))
                    if serializer:
                        self.fields[field.name] = serializer(
                            read_only=True, label=label, many=True)
                    continue
                # if field_class_name == 'ManyToOneRel':
                    # if serializer:
                    #     self.fields[field.name] = serializer(read_only=True, many=True)
                    # continue
                    # Self.update_related.append(field.name)
                    # continue

    def update(self, instance, validated_data, *args, **kwargs):
        request_data = self.context['request'].data
        for item in self.update_related:
            key = item if type(item) is str else item[0]
            action = 'update' if type(
                item) is str or len(item) < 2 else item[1]
            obj = getattr(instance, key, None)
            if key and key in request_data:
                value = request_data[key]

                if action == 'many':
                    instance = update_simple_related_objects(
                        instance=instance,
                        key=key,
                        related_objects_data=value
                    )
                    continue

                for field in self.model_fields:
                    if getattr(field, 'name', None) != key:
                        continue

                    if action == 'creatable':
                        instance = create_or_update_foreignkey(
                            instance=instance,
                            key=key,
                            data=value,
                            related_object_model=field.related_model
                        )
                        break

                    if action == 'update':
                        instance = update_foreignkey(
                            instance=instance,
                            key=key,
                            related_object_id=value,
                            related_object_model=field.related_model,
                        )
                        break

        only_add_existing = request_data.pop('onlyAddExisting', None)
        if only_add_existing:
            for field in self.model_fields:
                if getattr(field, 'name', None) != only_add_existing['key']:
                    continue
                obj_to_add = field.related_model.objects.get(
                    pk=only_add_existing['value'])
                getattr(instance, only_add_existing['key']).add(obj_to_add)

        return super().update(instance, validated_data)

    class Meta:
        fields = '__all__'

######################


for app in settings['APPS']:
    for name, model in apps.all_models[app].items():
        model_name = model.__name__
        if isinstance(model, type):
            serializer_list_name = f"{model_name}ListSerializer"
            serializer_name = f"{model_name}Serializer"
            if not serializer_name in dir():
                meta = type("Meta", (), {
                    'fields': '__all__',
                    'model': model
                })
                generated_class = type(serializer_list_name, (GenericSerializer,), {
                    'Meta': meta,
                })
                globals()[serializer_list_name] = generated_class

                generated_class = type(serializer_name, (GenericSerializer,), {
                    'Meta': meta
                })
                globals()[serializer_name] = generated_class

                # Generate serializers for nested viewsets:
                # for field in model._meta.get_fields():
                #     if field.__class__.__name__ == 'ManyToOneRel':
                #         related_serializer_name = f"{model_name}Related{related_model_name}Serializer"
                #         related_model_name = field.related_model.__name__
                #         related_meta = type("Meta",(),{
                #             'fields':'__all__',
                #             'model':field.related_model
                #         })
                #         generated_class = type(serializer_name, (GenericSerializer,), {
                #             'Meta': related_meta
                #         })
                #         globals()[related_serializer_name] = generated_class
