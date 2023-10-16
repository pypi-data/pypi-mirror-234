from django.apps import apps as django_apps


class ReferenceModelValidationError(Exception):
    pass


class ReferenceFieldValidationError(Exception):
    pass


class ReferenceDuplicateField(Exception):
    pass


class ReferenceFieldAlreadyAdded(Exception):
    pass


class ReferenceModelConfig:
    reference_model = "edc_reference.reference"

    def __init__(self, name: str = None, fields: list[str] = None):
        """
        Keywords:
            name = app_label.model_name for CRFs
            name = app_label.model_name.panel for Requisitions

        Note: `app_label.model_name` may not be a proxy model
        """

        if not fields:
            raise ReferenceFieldValidationError("No fields declared.")
        self.field_names: list[str] = list(set(fields))
        self.field_names.sort()
        self.name: str = name.lower()
        self.model: str = ".".join(name.split(".")[:2])
        if len(fields) != len(self.field_names):
            raise ReferenceDuplicateField(
                f"Duplicate field detected. Got {fields}. See '{self.name}'"
            )

    def add_fields(self, fields: list[str] = None) -> None:
        for field_name in fields:
            if field_name in self.field_names:
                raise ReferenceFieldAlreadyAdded(
                    f"Field already added. Got {field_name}. See '{self.name}'"
                )
        self.field_names.extend(fields)
        self.field_names = list(set(self.field_names))
        self.field_names.sort()

    def remove_fields(self, fields=None) -> None:
        for field in fields:
            self.field_names.remove(field)
        self.field_names = list(set(self.field_names))
        self.field_names.sort()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, fields={self.field_names})"

    def check(self):
        """Validates the model class by doing a django.get_model lookup
        and confirming all fields exist on the model class.
        """
        try:
            model_cls = django_apps.get_model(self.model)
        except LookupError:
            raise ReferenceModelValidationError(
                f"Invalid app label or model name. Got {self.model}. See {repr(self)}."
            )
        model_field_names = [fld.name for fld in model_cls._meta.get_fields()]
        for field_name in self.field_names:
            if field_name not in model_field_names:
                raise ReferenceFieldValidationError(
                    f"Invalid reference field. Got {field_name} not found "
                    f"on model {repr(model_cls)}. See {repr(self)}."
                )
        try:
            model_cls.reference_updater_cls
        except AttributeError:
            raise ReferenceFieldValidationError(
                "Missing reference model mixin. (reference_updater_cls) "
                f"See model {repr(model_cls)}"
            )
        try:
            model_cls.reference_deleter_cls
        except AttributeError:
            raise ReferenceFieldValidationError(
                "Missing reference model mixin. (reference_deleter_cls) "
                f"See model {repr(model_cls)}"
            )
