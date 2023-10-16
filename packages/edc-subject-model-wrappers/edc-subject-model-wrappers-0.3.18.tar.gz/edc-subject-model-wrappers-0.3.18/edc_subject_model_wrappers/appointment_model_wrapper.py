from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps as django_apps
from django.urls.base import reverse
from edc_dashboard.url_names import url_names
from edc_model_wrapper import ModelWrapper

if TYPE_CHECKING:
    from edc_visit_schedule.schedule import Schedule
    from edc_visit_schedule.visit_schedule import VisitSchedule
    from edc_visit_tracking.model_mixins import VisitModelMixin


class AppointmentModelWrapperError(Exception):
    pass


class AppointmentModelWrapper(ModelWrapper):
    dashboard_url_name = "subject_dashboard_url"
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
    querystring_attrs = ["reason"]
    unscheduled_appointment_url_name = "edc_appointment:unscheduled_appointment_url"
    model = "edc_appointment.appointment"
    visit_model_wrapper_cls = None

    def get_appt_status_display(self) -> str:
        return self.object.get_appt_status_display()

    @property
    def title(self) -> str:
        return self.object.title

    @property
    def visit_code_sequence(self) -> int:
        return self.object.visit_code_sequence

    @property
    def reason(self) -> str:
        return self.object.appt_reason

    @property
    def visit_schedule(self) -> VisitSchedule:
        return self.object.visit_schedule

    @property
    def schedule(self) -> Schedule:
        return self.object.schedule

    @property
    def wrapped_visit(self) -> VisitModelMixin:
        """Returns a wrapped persisted or non-persisted
        visit model instance.
        """
        model_obj = self.object.related_visit
        if not model_obj:
            visit_model = django_apps.get_model(self.visit_model_wrapper_cls.model)
            model_obj = visit_model(
                appointment=self.object,
                subject_identifier=self.object.subject_identifier,
                reason=self.object.appt_reason,
                report_datetime=self.object.appt_datetime,
            )
        visit_model_wrapper = self.visit_model_wrapper_cls(
            model_obj=model_obj, force_wrap=True
        )
        if (
            visit_model_wrapper.appointment_model_cls._meta.label_lower
            != self.model_cls._meta.label_lower
        ):
            raise AppointmentModelWrapperError(
                f"Declared model does not match appointment "
                f"model in visit_model_wrapper. "
                f"Got {self.model_cls._meta.label_lower} <> "
                f"{visit_model_wrapper.appointment_model_cls._meta.label_lower}"
            )
        return visit_model_wrapper

    @property
    def dashboard_url(self: Any) -> str:
        return url_names.get(self.dashboard_url_name)

    @property
    def forms_url(self: Any) -> str:
        """Returns a reversed URL to show forms for this appointment/visit.

        This is standard for edc_dashboard.
        """
        kwargs = dict(subject_identifier=self.subject_identifier, appointment=self.object.id)
        return reverse(self.dashboard_url, kwargs=kwargs)

    @property
    def unscheduled_appointment_url(self: Any) -> str:
        """Returns a url for the unscheduled appointment."""
        appointment_model_cls = django_apps.get_model("edc_appointment.appointment")
        kwargs = dict(
            subject_identifier=self.subject_identifier,
            visit_schedule_name=self.object.visit_schedule_name,
            schedule_name=self.object.schedule_name,
            visit_code=self.object.visit_code,
            timepoint=self.object.timepoint,
        )
        appointment = (
            appointment_model_cls.objects.filter(visit_code_sequence__gt=0, **kwargs)
            .order_by("visit_code_sequence")
            .last()
        )
        try:
            visit_code_sequence = appointment.visit_code_sequence + 1
        except AttributeError:
            visit_code_sequence = 1
        kwargs.update(
            timepoint=str(self.object.timepoint),
            visit_code_sequence=str(visit_code_sequence),
            redirect_url=self.dashboard_url,
        )
        return reverse(self.unscheduled_appointment_url_name, kwargs=kwargs)
