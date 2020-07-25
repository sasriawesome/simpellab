from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django_numerators.models import NumeratorMixin

from simpellab.core.enums import MaxLength
from simpellab.core.models import SimpleBaseModel, BaseModel
from simpellab.modules.carts.models import Cart
from simpellab.modules.products.models import Service, Parameter
from simpellab.modules.blueprints.models import Blueprint
from simpellab.modules.sales.models import SalesOrder, OrderItem, OrderItemParameter

_ = translation.ugettext_lazy


__all__ = [
    'InspectionService',
    'InspectionBlueprint',
    'InspectionBlueprintParameter',
    'InspectionCart',
    'InspectionCartParameter',
    'InspectionOrder',
    'InspectionOrderItem',
    'InspectionOrderItemParameter'
]


class InspectionService(Service):
    class Meta:
        verbose_name = _('Technical Inspection')
        verbose_name_plural = _('Technical Inspections')

    def add_to_cart(self, request):
        with transaction.atomic():
            matrix = {'user':request.user, 'product': self, 'quantity':1}
            cart = InspectionCart.objects.create(**matrix)
            return cart
            
    def get_doc_prefix(self):
        return 'LIT'


class InspectionCart(Cart):
    class Meta:
        verbose_name =_('Inspection Cart')
        verbose_name_plural =_('Inspection Carts')

    product = models.ForeignKey(
        InspectionService,
        on_delete=models.CASCADE,
        related_name='lit_carts',
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


class InspectionCartParameter(SimpleBaseModel):
    class Meta:
        verbose_name = _('Inspection Cart Parameter')
        verbose_name_plural = _('Inspection Cart Parameters')
        unique_together = ('cart', 'parameter')

    cart = models.ForeignKey(
        InspectionCart,
        on_delete=models.CASCADE,
        related_name='parameters',
        verbose_name=_('Cart')
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name='lit_carts'
    )
    note = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Note'))

    def __str__(self):
        return str(self.parameter)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class InspectionBlueprint(Blueprint):
    class Meta:
        verbose_name = _('Inspection Blueprint')
        verbose_name_plural = _('Inspection Blueprints')
    
    product = models.ForeignKey(
        InspectionService,
        on_delete=models.CASCADE,
        related_name='blueprints'
        )

    def add_to_cart(self, request):
        with transaction.atomic():
            cart = InspectionCart.objects.create(
                user=request.user,
                product=self.product,
                name=self.name,
                note=self.note,
                quantity=1
            )
            for bp_param in self.parameters.all():
                InspectionCartParameter.objects.create(
                    cart=cart,
                    parameter=bp_param.parameter,
                    note=bp_param.note
                )
            return cart

class InspectionBlueprintParameter(SimpleBaseModel):
    class Meta:
        verbose_name = _('Blueprint Parameter')
        verbose_name_plural = _('Blueprint Parameters')
        unique_together = ('blueprint', 'parameter')

    blueprint = models.ForeignKey(
        InspectionBlueprint,
        on_delete=models.CASCADE,
        related_name='parameters',
        verbose_name=_('Blueprint')
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        related_name='lit_blueprints'
    )
    note = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_('Note'))

    def __str__(self):
        return str(self.parameter)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class InspectionOrder(SalesOrder):
    class Meta:
        verbose_name = _('Inspection Order')
        verbose_name_plural = _('Inspection Orders')

    def get_order_items(self):
        """ Get child object order_items """
        return self.order_items

        
class InspectionOrderItem(OrderItem):
    class Meta:
        verbose_name = _('Inspection Order Item')
        verbose_name_plural = _('Inspection Order Items')

    doc_prefix = 'ILIT'

    order = models.ForeignKey(
        InspectionOrder, 
        on_delete=models.CASCADE,
        related_name='order_items')
    product = models.ForeignKey(
        InspectionService,
        on_delete=models.PROTECT,
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


class InspectionOrderItemParameter(OrderItemParameter):
    class Meta:
        verbose_name = _('Parameter')
        verbose_name_plural = _('Parameters')
        unique_together = ('order_item', 'parameter')

    order_item = models.ForeignKey(
        InspectionOrderItem,
        related_name='parameters',
        on_delete=models.CASCADE,
        verbose_name=_('Product'))
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE,
        related_name='lit_parameters',
        verbose_name=_('Parameter'))
    

@receiver(post_save, sender=InspectionOrderItem)
def after_save_lit_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=InspectionOrderItem)
def after_delete_lit_item(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_save, sender=InspectionOrderItemParameter)
def after_save_lit_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()


@receiver(post_delete, sender=InspectionOrderItemParameter)
def after_delete_lit_parameter(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    print(instance.order_item)
    instance.order_item.save()