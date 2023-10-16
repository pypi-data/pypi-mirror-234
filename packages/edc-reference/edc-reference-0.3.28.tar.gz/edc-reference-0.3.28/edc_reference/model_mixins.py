from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .reference import ReferenceDeleter, ReferenceUpdater


class ReferenceModelMixinError(Exception):
    pass


class ReferenceModelMixin(models.Model):
    reference_deleter_cls = ReferenceDeleter
    reference_updater_cls = ReferenceUpdater

    def update_reference_on_save(self) -> None:
        """Update references for this model only.

        Self will be a CRF/requistion model instance.

        See also signal in edc-metadata.
        """
        self.model_reference_validate()
        if self.reference_updater_cls:
            self.reference_updater_cls(model_obj=self)

    def update_references_on_save(self) -> None:
        """Update references for all existing models for this
        related visit / timepoint.

        Self is the related_visit model instance.
        """
        for model_cls in self.visit.get_models():
            opts = {model_cls.related_visit_model_attr(): self}
            try:
                model_obj = model_cls.objects.get(**opts)
            except ObjectDoesNotExist:
                pass
            else:
                model_obj.update_reference_on_save()

    @property
    def reference_name(self) -> str:
        return self._meta.label_lower

    def model_reference_validate(self) -> None:
        if "panel" in [f.name for f in self._meta.get_fields()]:
            raise ReferenceModelMixinError(
                "Detected field panel. Is this a requisition?. "
                "Use RequisitionReferenceModelMixin "
                "instead of ReferenceModelMixin"
            )

    class Meta:
        abstract = True


class RequisitionReferenceModelMixin(ReferenceModelMixin, models.Model):
    @property
    def reference_name(self) -> str:
        return f"{self._meta.label_lower}.{self.panel.name}"

    def model_reference_validate(self) -> None:
        if "panel" not in [f.name for f in self._meta.get_fields()]:
            raise ReferenceModelMixinError(
                "Did not detect field panel. Is this a CRF?. "
                "Use ReferenceModelMixin "
                "instead of RequisitionReferenceModelMixin"
            )

    class Meta:
        abstract = True
