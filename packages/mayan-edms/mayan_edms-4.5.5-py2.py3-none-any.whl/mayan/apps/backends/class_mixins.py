class DynamicFormBackendMixin:
    """
    The fields attribute is a list of dictionaries with the format:
    {
        'name': ''  # Field internal name
        'label': ''  # Label to show to users
        'initial': ''  # Field initial value
        'default': ''  # Default value.
    }
    """
    form_fieldset_exclude_list = ('backend_data',)

    @classmethod
    def get_form_field_order(cls):
        return getattr(
            cls, 'form_field_order', ()
        )

    @classmethod
    def get_form_field_widgets(cls):
        return getattr(
            cls, 'form_field_widgets', {}
        )

    @classmethod
    def get_form_fields(cls):
        return getattr(
            cls, 'form_fields', {}
        )

    @classmethod
    def get_form_fieldset_exclude_list(cls):
        return getattr(
            cls, 'form_fieldset_exclude_list', ()
        )

    @classmethod
    def get_form_fieldsets(cls):
        return getattr(
            cls, 'form_fieldsets', ()
        )

    @classmethod
    def get_form_media(cls):
        return getattr(
            cls, 'form_media', {}
        )

    @classmethod
    def get_form_schema(cls, *args, **kwargs):
        form_fields = cls.get_form_fields(**kwargs)

        result = {
            'fields': form_fields,
            'fieldset_exclude_list': cls.get_form_fieldset_exclude_list(**kwargs),
            'fieldsets': cls.get_form_fieldsets(**kwargs),
            'media': cls.get_form_media(),
            'widgets': cls.get_form_field_widgets(**kwargs)
        }

        form_field_order = cls.get_form_field_order(**kwargs) or tuple(
            form_fields.keys()
        )

        result['field_order'] = form_field_order

        return result
