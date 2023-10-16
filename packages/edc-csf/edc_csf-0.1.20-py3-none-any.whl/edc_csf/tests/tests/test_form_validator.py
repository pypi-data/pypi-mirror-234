from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_constants.constants import NO, NOT_DONE, YES
from edc_reference import site_reference_configs
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from visit_schedule_app.models import SubjectVisit
from visit_schedule_app.visit_schedule import visit_schedule

from edc_csf.form_validators import LpCsfFormValidator
from edc_csf.models import LpCsf
from edc_csf.panels import csf_panel
from edc_csf_app.models import Panel, SubjectRequisition


class TestLpFormValidator(TestCase):
    def setUp(self):
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule)
        site_reference_configs.register_from_visit_schedule(
            visit_models={"edc_appointment.appointment": "edc_visit_tracking.subjectvisit"}
        )
        self.subject_identifier = "1234"
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code="1000",
            visit_code_sequence=0,
            visit_schedule_name="visit_schedule",
            schedule_name="schedule",
            timepoint=Decimal("1.0"),
        )
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            visit_code_sequence=0,
            visit_code="1000",
            reason=SCHEDULED,
            visit_schedule_name="visit_schedule",
            schedule_name="schedule",
        )

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code="3000",
            visit_code_sequence=0,
            visit_schedule_name="visit_schedule",
            schedule_name="schedule",
            timepoint=Decimal("1.0"),
        )
        self.subject_visit_d3 = SubjectVisit.objects.create(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            visit_code_sequence=0,
            visit_code="3000",
            reason=SCHEDULED,
            visit_schedule_name="visit_schedule",
            schedule_name="schedule",
        )

    def test_pressure(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "opening_pressure": 10,
            "closing_pressure": 9,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

        cleaned_data = {
            "subject_visit": self.subject_visit,
            "opening_pressure": 10,
            "closing_pressure": 11,
        }

        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("closing_pressure", form_validator._errors)
        self.assertIn("Cannot be greater", str(form_validator._errors.get("closing_pressure")))

    def test_other_csf_culture_required(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_culture": YES,
            "other_csf_culture": None,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("other_csf_culture", form_validator._errors)
        self.assertIn("is required", str(form_validator._errors.get("other_csf_culture")))

    def test_other_csf_culture_not_required(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_culture": NO,
            "other_csf_culture": "blah",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("other_csf_culture", form_validator._errors)
        self.assertIn("not required", str(form_validator._errors.get("other_csf_culture")))

    def test_csf_culture_not_perfomed(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_culture": NOT_DONE,
            "other_csf_culture": "culture",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("other_csf_culture", form_validator._errors)
        self.assertIn("not required", str(form_validator._errors.get("other_csf_culture")))

    def test_qc_culture(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "qc_requisition": None,
            "qc_assay_datetime": None,
            "quantitative_culture": None,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexpectedly raised")

    def test_qc_culture_requisition_not_required_if_no_result(self):
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit, panel=panel
        )
        requisition.panel_object = csf_panel
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "qc_requisition": requisition,
            "qc_assay_datetime": get_utcnow(),
            "quantitative_culture": None,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            "This field is not required",
            str(form_validator._errors.get("qc_requisition")),
        )

    def test_qc_assay_datetime_not_required_if_no_result(self):
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit, panel=panel
        )
        requisition.panel_object = csf_panel
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "qc_requisition": None,
            "qc_assay_datetime": get_utcnow(),
            "quantitative_culture": None,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            "This field is not required",
            str(form_validator._errors.get("qc_assay_datetime")),
        )

    def test_qc_culture_requisition_required_if_value(self):
        """Requisition is required if there is a value."""
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "qc_requisition": None,
            "qc_assay_datetime": None,
            "quantitative_culture": "12",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            "This field is required", str(form_validator._errors.get("qc_requisition"))
        )

    def test_qc_assay_datetime_required_if_value(self):
        """Requisition is required if there is a value."""
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit, panel=panel
        )
        requisition.panel_object = csf_panel
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "qc_requisition": requisition,
            "qc_assay_datetime": None,
            "quantitative_culture": "12",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            "This field is required",
            str(form_validator._errors.get("qc_assay_datetime")),
        )

    def test_india_ink_csf_arg_not_done_invalid(self):
        """Assert that either csf_cr_ag or india_ink is done."""
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_crag": NOT_DONE,
            "india_ink": NOT_DONE,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("csf_crag", form_validator._errors)
        self.assertIn("india_ink", form_validator._errors)

    def test_csf_wbc_cell_count_not_required_day1(self):
        cleaned_data = {"subject_visit": self.subject_visit, "csf_wbc_cell_count": None}
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexpectedly raised")

    def test_csf_wbc_cell_count_not_required_day3(self):
        cleaned_data = {
            "subject_visit": self.subject_visit_d3,
            "csf_wbc_cell_count": None,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexpectedly raised")

    def test_csf_wbc_cell_count_min_max(self):
        for i in range(0, 5):
            cleaned_data = {
                "subject_visit": self.subject_visit_d3,
                "csf_wbc_cell_count": i,
            }
            form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
            try:
                form_validator.validate()
            except ValidationError:
                self.fail(
                    f"ValidationError unexpectedly raised. " f"Got {form_validator._errors}"
                )

    def test_csf_crag_not_done_csf_crag_lfa_not_required(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_crag": NOT_DONE,
            "csf_crag_lfa": YES,
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("csf_crag_lfa", form_validator._errors)
        self.assertIn("not required", str(form_validator._errors.get("csf_crag_lfa")))

    def test_differential_neutrophil_count_percent_limit_passed(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_wbc_cell_count": 4,
            "differential_lymphocyte_count": 50,
            "differential_lymphocyte_unit": "%",
            "differential_neutrophil_count": 125.6,
            "differential_neutrophil_unit": "%",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("differential_neutrophil_count", form_validator._errors)
        self.assertIn(
            "Cannot be greater than 100%",
            str(form_validator._errors.get("differential_neutrophil_count")),
        )

    def test_differential_lymphocyte_count_percent_limit_passed(self):
        cleaned_data = {
            "subject_visit": self.subject_visit,
            "csf_wbc_cell_count": 4,
            "differential_lymphocyte_count": 125.6,
            "differential_lymphocyte_unit": "%",
        }
        form_validator = LpCsfFormValidator(cleaned_data=cleaned_data, instance=LpCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("differential_lymphocyte_count", form_validator._errors)
        self.assertIn(
            "Cannot be greater than 100%",
            str(form_validator._errors.get("differential_lymphocyte_count")),
        )
