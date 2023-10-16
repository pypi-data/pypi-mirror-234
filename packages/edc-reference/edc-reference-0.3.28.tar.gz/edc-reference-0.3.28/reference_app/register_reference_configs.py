from edc_reference import site_reference_configs


def register_reference_configs():
    site_reference_configs.registry = {}
    site_reference_configs.loaded = False

    site_reference_configs.register_from_visit_schedule(
        visit_models={"edc_appointment.appointment": "edc_visit_tracking.subjectvisit"}
    )

    site_reference_configs.add_fields_to_config(
        name="reference_app.testmodel", fields=["field_str"]
    )

    configs = {
        "reference_app.crfone": [
            "field_str",
            "field_date",
            "field_datetime",
            "field_int",
        ],
    }

    for reference_name, fields in configs.items():
        site_reference_configs.add_fields_to_config(name=reference_name, fields=fields)
