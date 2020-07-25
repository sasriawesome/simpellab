import uuid
from django.db import models
from django.db.utils import cached_property
from django.core.exceptions import ValidationError
from django.utils import timezone, translation
from sister.core.managers import ParanoidManager

_ = translation.ugettext_lazy


class SimpleBaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    modified_at = models.DateTimeField(default=timezone.now, editable=False)
    
    @cached_property
    def opts(self):
        return self._meta

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding:
            self.modified_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)


class BaseModel(SimpleBaseModel):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now, editable=False)


class ParanoidMixin(models.Model):
    class Meta:
        abstract = True
        
    objects = ParanoidManager()

    deleted = models.BooleanField(default=False, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    def pass_delete_validation(self):
        return True

    def get_deletion_error_message(self):
        msg = _("E1001: %s deletion can't be performed.")
        return msg % self._meta.verbose_name

    def get_deletion_message(self):
        msg = _("E1010: %s deleted succesfully.")
        return msg % self._meta.verbose_name

    def delete(self, using=None,
               keep_parents=False,
               paranoid=False, user=None):
        """
            Give paranoid delete mechanism to each record
        """
        if not self.pass_delete_validation():
            raise ValidationError(self.get_deletion_error_message())

        if paranoid:
            self.deleted = True
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def pass_restore_validation(self):
        return self.deleted

    def get_restoration_error_message(self):
        msg = _("E1002: %s restoration can't be performed.")
        return msg % self._meta.verbose_name

    def restore(self):
        if not self.pass_restore_validation():
            raise ValidationError(self.get_restoration_error_message())
        self.deleted = False
        self.deleted_at = None
        self.save()