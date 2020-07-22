from django.db import models
from django.utils import translation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from django_numerators.models import NumeratorMixin
from polymorphic.models import PolymorphicModel

from simpellab.core.enums import MaxLength
from simpellab.core.models import BaseModel, SimpleBaseModel
from simpellab.modules.partners.models import Partner


_ = translation.gettext_lazy


class Term(PolymorphicModel, NumeratorMixin, SimpleBaseModel):
    class Meta:
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')

    doc_prefix = 'TRM'
    
    title = models.CharField(
        max_length=MaxLength.LONG.value
        verbose_name=_('Title')
        )
    description = models.CharField(
        max_length=MaxLength.TEXT.value
        verbose_name=_('Description')
        )
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.inner_id
