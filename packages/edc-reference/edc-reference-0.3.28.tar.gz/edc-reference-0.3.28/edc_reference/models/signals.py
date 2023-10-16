from django.db.models.signals import post_delete
from django.dispatch import receiver

from ..reference import ReferenceDeleterError


@receiver(post_delete, weak=False, dispatch_uid="edc_reference_post_delete")
def reference_post_delete(instance, using, **kwargs):
    try:
        instance.reference_deleter_cls(model_obj=instance)
    except AttributeError as e:
        if "reference_deleter_cls" not in str(e):
            raise
        pass
    except ReferenceDeleterError:
        pass
