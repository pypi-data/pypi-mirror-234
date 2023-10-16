import sys

from django.core.checks import Warning
from django.core.management import color_style

from .site_reference import site_reference_configs

style = color_style()


def check_site_reference_configs(app_configs, **kwargs):
    sys.stdout.write(style.SQL_KEYWORD("check_site_reference_configs ... \r"))
    errors = []
    site_results = site_reference_configs.check()
    for result in site_results.values():
        errors.append(Warning(result, id="edc_reference.001"))
    sys.stdout.write(style.SQL_KEYWORD("check_site_reference_configs ... done.\n"))
    return errors
