from hashlib import md5
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from simpellab.core.models import BaseModel
from simpellab.core.enums import MaxLength


class ShortUrl(BaseModel):
    class Meta:
        verbose_name = _('Short Url')
        verbose_name_plural = _('Short Urls')

    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Name')
        )    
    description = models.TextField(
        max_length=MaxLength.TEXT.value,
        null=True, blank=True,
        verbose_name=_('Description')
        )
    hashed_url = models.CharField(
        unique=True, editable=False,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Hashed url')
        )
    original_url = models.URLField(
        unique=True,
        verbose_name='Original Url'
    )
    ads = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    clicked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self._meta

    def get_absolute_url(self):
        return reverse('goto_shorturl', args=(self.hashed_url,))

    def click(self):
        self.clicked += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.hashed_url = md5(self.original_url.encode()).hexdigest()[:10]

        return super().save(*args, **kwargs)