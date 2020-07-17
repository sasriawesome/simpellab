from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet

from simpellab.modules.products.enums import ProductType


class OrderProductFormset(BaseInlineFormSet):
    def clean(self):
        order_type = getattr(self.instance, 'product_type', None)
        if getattr(self.instance, 'product_type', False):
            for child in self.forms:
                product = child.cleaned_data.get('product', None)
                service_type = getattr(product, 'service_type', None)
                if product:
                    if service_type != ProductType[order_type].name:
                        msg = _("{} is not {} product. please select correct products.")
                        type_display = self.instance.get_product_type_display()
                        raise ValidationError(str(msg).format(product.name, type_display))
                else:
                    ValidationError(_("Please select product"))
        else:
            raise ValidationError(_("Please select service"))