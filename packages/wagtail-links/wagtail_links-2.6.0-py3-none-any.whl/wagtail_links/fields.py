from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import SlugField


class NullSlugField(SlugField):
    """
    SlugField that stores '' as None and returns None as ''

    Useful when using unique=True and forms. Implies null==blank==True.
    """

    def __init__(self, *args, **kwargs):
        if not kwargs.get("null", True) or not kwargs.get("blank", True):
            raise ImproperlyConfigured("NullCharField implies null==blank==True")
        kwargs["null"] = kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, *args, **kwargs):
        value = self.to_python(value)
        # If the value was stored as null, return empty string instead
        return value if value is not None else ""

    def get_prep_value(self, value):
        prepped = super().get_prep_value(value)
        # If the value was stored as empty string, return None instead
        return prepped if prepped != "" else None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs
