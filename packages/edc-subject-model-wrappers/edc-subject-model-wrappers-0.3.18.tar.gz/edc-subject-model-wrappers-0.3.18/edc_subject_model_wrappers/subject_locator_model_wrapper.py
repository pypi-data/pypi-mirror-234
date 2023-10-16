from edc_locator.utils import get_locator_model
from edc_model_wrapper.wrappers import ModelWrapper


class SubjectLocatorModelWrapper(ModelWrapper):
    model = get_locator_model()
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
