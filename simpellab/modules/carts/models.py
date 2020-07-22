from django.db import models
from django.utils import translation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


from django_numerators.models import NumeratorMixin
from polymorphic.models import PolymorphicModel

from simpellab.core.enums import MaxLength
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.modules.partners.models import Partner
from simpellab.modules.products.models import Product
from simpellab.modules.sales.models import SalesOrder

_ = translation.gettext_lazy


class Cart(PolymorphicModel):
    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
    
    user = models.ForeignKey(
        get_user_model(),
        editable=False,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('User')
        )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantity')
    )
    def __str__(self):
        return str(self.user)

    
class CommonCart(Cart):
    class Meta:
        verbose_name =_('Common Cart')
        verbose_name_plural =_('Common Carts')

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='common_carts',
        verbose_name=_('Product')
        )
