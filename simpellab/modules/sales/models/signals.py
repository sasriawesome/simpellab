from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from simpellab.modules.sales.models.quotations import (
    QuotationExtraFee,
    QuotationProduct
    )
from simpellab.modules.sales.models.orders import (
    OrderFee,
    OrderProduct,
    ExtraParameter
    )


@receiver(post_save, sender=QuotationExtraFee)
def after_save_quotation_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_delete, sender=QuotationExtraFee)
def after_delete_quotation_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_save, sender=QuotationProduct)
def after_save_quotation_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_delete, sender=QuotationProduct)
def after_delete_quotation_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.quotation.save()


@receiver(post_save, sender=OrderFee)
def after_save_order_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=OrderFee)
def after_delete_order_fee(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_save, sender=OrderProduct)
def after_save_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_delete, sender=OrderProduct)
def after_delete_order_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.order.save()


@receiver(post_save, sender=ExtraParameter)
def after_save_product(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.product.save()


@receiver(post_delete, sender=ExtraParameter)
def after_delete_parameter_lab(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    instance.product.save()
