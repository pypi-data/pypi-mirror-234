from edc_lab import LabProfile, RequisitionPanel
from edc_lab_panel.panels import cd4_panel, fbc_panel, vl_panel
from edc_lab_panel.processing_profiles import fbc_processing

panel_one = RequisitionPanel(name="one", verbose_name="One", processing_profile=fbc_processing)

panel_two = RequisitionPanel(name="two", verbose_name="Two", processing_profile=fbc_processing)

lab_profile = LabProfile(
    name="lab_profile", requisition_model="reference_app.subjectrequisition"
)

lab_profile.add_panel(panel_one)
lab_profile.add_panel(panel_two)
lab_profile.add_panel(cd4_panel)
lab_profile.add_panel(vl_panel)
lab_profile.add_panel(fbc_panel)
