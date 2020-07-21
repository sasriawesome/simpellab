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


_ = translation.gettext_lazy


class Cart(models.Model):
    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
    
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('User')
        )

    def __str__(self):
        return self.inner_id


class CartItem(PolymorphicModel):
    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')


class CommonCartItem(CartItem):
    class Meta:
        verbose_name =_('Common Cart Item')
        verbose_name_plural =_('Common Cart Items')

    cart = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products'
        )    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name=_('Product')
        )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantity')
    )
    
    def __str__(self):
        return str(self.product)