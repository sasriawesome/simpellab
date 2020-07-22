from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import translation, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.sales.models import SalesOrder, OrderItem, OrderItemParameter
from simpellab.modules.blueprints.models import Blueprint
from simpellab.modules.carts.models import Cart


_ = translation.ugettext_lazy


__all__ = [
    'LaboratoriumService',
    'LaboratoriumCart',
    'LaboratoriumCartParameter',
    'LaboratoriumBlueprint',
    'LaboratoriumBlueprintParameter',
    'LaboratoriumOrder',
    'LaboratoriumOrderItem',
    'LaboratoriumOrderItemParameter'
]


class LaboratoriumService(Service):
    class Meta:
        verbose_name = _('Laboratorium Test')
        verbose_name_plural = _('Laboratorium Tests')

    def get_doc_prefix(self):
        return 'LAB'

    def add_to_cart(self, request):
        with transaction.atomic():
            matrix = {'user':request.user, 'product': self, 'quantity':1}
            cart = LaboratoriumCart.objects.create(**matrix)
            return cart

class LaboratoriumCart(Cart):
    class Meta:
        verbose_name =_('Laboratorium Cart')
        verbose_name_plural =_('Laboratorium Carts')

    product = models.ForeignKey(
        LaboratoriumService,
        on_delete=models.CASCADE,
        related_name='lab_carts',
        verbose_name=_('Product')
        )
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_('Name'),
        help_text=_('Sample name or identifier')
        )
    note = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.TEXT.value,
        verbose_name=_('Note')
        )


class LaboratoriumCartParameter(SimpleBaseModel):
    class Meta:
        verbose_name = _('Laboratorium Cart Parameter')
        verbose_name_plural = _('Laboratorium Cart Parameters')
        unique_together = ('cart', 'parameter')

    cart = models.ForeignKey(
        LaboratoriumCart,
        on_delete=models.CASCADE,
        related_name='parameters',
        verbose_name=_('Cart')
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name='lab_carts'
    )
    note = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Note'))

    def __str__(self):
        return str(self.parameter)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class LaboratoriumBlueprint(Blueprint):
    class Meta:
        verbose_name = _('Blueprint')
        verbose_name_plural = _('Blueprints')
    
    product = models.ForeignKey(
        LaboratoriumService,
        on_delete=models.CASCADE,
        related_name='blueprints'
        )

    def add_to_cart(self, request):
        with transaction.atomic():
            cart = LaboratoriumCart.objects.create(
                user=request.user,
                product=self.product,
                name=self.name,
                note=self.note,
                quantity=1
            )
            for bp_param in self.parameters.all():
                LaboratoriumCartParameter.objects.create(
                    cart=cart,
                    parameter=bp_param.parameter,
                    note=bp_param.note
                )
            return cart

class LaboratoriumBlueprintParameter(SimpleBaseModel):
    class Meta:
        verbose_name = _('Blueprint Parameter')
        verbose_name_plural = _('Blueprint Parameters')
        unique_together = ('blueprint', 'parameter')

    blueprint = models.ForeignKey(
        LaboratoriumBlueprint,
        on_delete=models.CASCADE,
        related_name='parameters',
        verbose_name=_('Blueprint')
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name='lab_blueprints'
    )
    note = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Note'))

    def __str__(self):
        return str(self.parameter)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class LaboratoriumOrder(SalesOrder):
    class Meta:
        verbose_name = _('Laboratorium Order')
        verbose_name_plural = _('Laboratorium Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items


class LaboratoriumOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Laboratorium Order Item')
        verbose_name_plural = _('Laboratorium Order Items')

    doc_prefix = 'ILAB'

    order = models.ForeignKey(
        LaboratoriumOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        LaboratoriumService,
        on_delete=models.CASCADE,
        related_name='orders')
    
    def get_parameter_prices(self):
        return self.parameters.aggregate(
            total_parameters=models.Sum('price')
        )['total_parameters'] or 0

    def calculate_unit_price(self):
        base_price = self.product.get_real_instance().total_price
        parameters = self.get_parameter_prices()
        unit_price = base_price + parameters
        return unit_price


class LaboratoriumOrderItemParameter(OrderItemParameter):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        LaboratoriumOrderItem,
        related_name='parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lab_parameters',
        verbose_name=_('Parameter'))


@receiver(post_save, sender=LaboratoriumOrderItem)
def after_save_lab_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=LaboratoriumOrderItem)
def after_delete_lab_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_save, sender=LaboratoriumOrderItemParameter)
def after_save_lab_item_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()


@receiver(post_delete, sender=LaboratoriumOrderItemParameter)
def after_delete_lab_item_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()