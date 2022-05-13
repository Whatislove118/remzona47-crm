from django.forms import model_to_dict


class ValidationMixin:
    def run_validators(self) -> None:
        for field_name, field_value in model_to_dict(self).items():
            model_field = getattr(self.__class__, field_name)
            field = getattr(model_field, "field", object())
            validators = getattr(field, "validators", list())
            for validator_func in validators:
                if field_value is not None:
                    validator_func(field_value)


class OverloadedQuerysetManagerMixin:
    def get_queryset(self):
        if queryset := getattr(self, "overloaded_queryset", None):
            return queryset
        return super().get_queryset()

    def __call__(self, overloaded_queryset):
        self.overloaded_queryset = overloaded_queryset
        return self
