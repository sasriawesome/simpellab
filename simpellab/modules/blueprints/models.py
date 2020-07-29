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


_ = translation.gettext_lazy


class Blueprint(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _('Blueprint')
        verbose_name_plural = _('Blueprints')
    
    user = models.ForeignKey(
        get_user_model(),
        editable=False,
        on_delete=models.CASCADE,
        related_name='blueprints',
        verbose_name=_('User')
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

    def __str__(self):
        return self.name