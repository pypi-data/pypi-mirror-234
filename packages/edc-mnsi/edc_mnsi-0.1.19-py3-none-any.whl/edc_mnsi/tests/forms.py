from django import forms
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from edc_mnsi.form_validator import MnsiFormValidatorMixin
from edc_mnsi.models import Mnsi


class MnsiFormValidator(MnsiFormValidatorMixin, FormValidator):
    pass


class MnsiForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MnsiFormValidator

    class Meta:
        model = Mnsi
        fields = "__all__"
