from dateutil.relativedelta import relativedelta
from edc_lab_panel.panels import cd4_panel, fbc_panel, vl_panel
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf, FormsCollection, Requisition, Visit
from edc_visit_schedule.visit_schedule import VisitSchedule

from ..lab_profiles import panel_one, panel_two

crfs = FormsCollection(
    Crf(show_order=10, model="reference_app.crfone", required=True),
    Crf(show_order=20, model="reference_app.testmodel", required=True),
)

requisitions = FormsCollection(
    Requisition(show_order=10, panel=cd4_panel, required=True, additional=False),
    Requisition(show_order=20, panel=panel_one, required=True, additional=False),
    Requisition(show_order=30, panel=panel_two, required=True, additional=False),
    Requisition(show_order=40, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=50, panel=vl_panel, required=True, additional=False),
)

visit0 = Visit(
    code="1000",
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
    requisitions=requisitions,
    facility_name="7-day-clinic",
)

visit1 = Visit(
    code="2000",
    title="Day 2",
    timepoint=1,
    rbase=relativedelta(days=7),
    rlower=relativedelta(days=6),
    rupper=relativedelta(days=6),
    crfs=crfs,
    requisitions=requisitions,
    facility_name="7-day-clinic",
)

visit2 = Visit(
    code="3000",
    title="Day 3",
    timepoint=2,
    rbase=relativedelta(days=14),
    rlower=relativedelta(days=6),
    rupper=relativedelta(days=6),
    crfs=crfs,
    requisitions=requisitions,
    facility_name="7-day-clinic",
)

schedule = Schedule(
    name="schedule1",
    onschedule_model="reference_app.onschedule",
    offschedule_model="reference_app.offschedule",
    appointment_model="edc_appointment.appointment",
    consent_model="reference_app.subjectconsent",
)

schedule.add_visit(visit0)
schedule.add_visit(visit1)
schedule.add_visit(visit2)

visit_schedule1 = VisitSchedule(
    name="visit_schedule1",
    offstudy_model="reference_app.subjectoffstudy",
    death_report_model="reference_app.deathreport",
)

visit_schedule1.add_schedule(schedule)
