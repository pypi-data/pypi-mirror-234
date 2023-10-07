class ViewMixinDynamicFormBackendClass:
    def get_form_schema(self):
        return self.get_backend_class().get_form_schema(
            **self.get_form_schema_extra_kwargs()
        )

    def get_form_schema_extra_kwargs(self):
        return {}
