from edc_model_admin.admin_site import EdcAdminSite

from .apps import AppConfig

edc_reference_admin = EdcAdminSite(name="edc_reference_admin", app_label=AppConfig.name)
