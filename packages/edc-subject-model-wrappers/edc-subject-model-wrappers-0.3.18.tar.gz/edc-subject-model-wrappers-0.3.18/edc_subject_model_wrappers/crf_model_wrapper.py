from edc_model_wrapper import ModelWrapper, PermissionsModelWrapperMixin


class CrfModelWrapper(PermissionsModelWrapperMixin, ModelWrapper):
    related_visit_model_attr = "subject_visit"
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["appointment", "subject_identifier"]
    querystring_attrs = [related_visit_model_attr]

    def get_related_visit_model_attr(self) -> str:
        return self.related_visit_model_attr or self.object.related_visit_model_attr()

    @property
    def related_visit(self) -> str:
        return str(getattr(self.object, self.get_related_visit_model_attr()).id)

    @property
    def appointment(self) -> str:
        return str(getattr(self.object, self.get_related_visit_model_attr()).appointment.id)

    @property
    def subject_identifier(self):
        return getattr(self.object, self.get_related_visit_model_attr()).subject_identifier

    @property
    def html_id(self):
        return f'id_{self.model_cls._meta.label_lower.replace(".", "_")}'
