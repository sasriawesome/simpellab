from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from simpellab.modules.sales.models import SalesOrder

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = '__all__'