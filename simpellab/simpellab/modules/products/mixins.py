from django.db import models
from django.db.utils import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


class PostMixin(models.Model):
    class Meta:
        abstract = True

    seo_title = models.CharField(
        verbose_name=_("page title"),
        max_length=255,
        blank=True,
        help_text=_(
            "Optional. 'Search Engine Friendly' title."
            + "This will appear at the top of the browser window.")
            )
    seo_description = models.TextField(
        verbose_name=_('seo description'), blank=True)

    live = models.BooleanField(
        verbose_name=_('live'),
        default=True)
    go_live_at = models.DateTimeField(
        verbose_name=_("go live date/time"),
        blank=True, null=True)
    expired = models.BooleanField(
        verbose_name=_('expired'),
        default=False, editable=False)
    expire_at = models.DateTimeField(
        verbose_name=_("expiry date/time"),
        blank=True, null=True)

    locked = models.BooleanField(
        verbose_name=_('locked'),
        default=False,
        editable=False
        )
    locked_at = models.DateTimeField(
        verbose_name=_('locked at'),
        null=True, editable=False
        )
    locked_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_('locked by'),
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name='locked_%(class)ss')
    first_published_at = models.DateTimeField(
        verbose_name=_('first published at'),
        blank=True,
        null=True,
        db_index=True)
    last_published_at = models.DateTimeField(
        verbose_name=_('last published at'),
        null=True,
        editable=False)
    latest_revision_created_at = models.DateTimeField(
        verbose_name=_('latest revision created at'),
        null=True,
        editable=False)


class StockableMixin(models.Model):
    class Meta:
        abstract = True
    sn = models.CharField(
        max_length=150,
        null=True, blank=True,
        verbose_name=_("serial number"))
    min_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("min stock"))
    max_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("max stock"))
    stock_on_hand = models.IntegerField(
        default=0,
        verbose_name=_("stock on hand"))
    stock_on_delivery = models.IntegerField(
        default=0,
        verbose_name=_("stock on delivery"))
    stock_on_request = models.IntegerField(
        default=0,
        verbose_name=_("stock on request"))

    @cached_property
    def soh_value(self):
        return self.stock_on_hand * self.price

    @cached_property
    def sod_value(self):
        return self.stock_on_delivery * self.price

    @cached_property
    def sor_value(self):
        return self.stock_on_request * self.price


class SellableMixin(models.Model):
    class Meta:
        abstract = True

    display_price = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)
    discount = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)