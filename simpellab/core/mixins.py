from django.db import models, transaction
from django.utils import translation, timezone
from simpellab.core.enums import Status

_ = translation.gettext_lazy


class StatusMixin(models.Model):
    """ Base for status mixin used in sales order,
        warehouse transfer or invoice """

    class Meta:
        abstract = True

    status = models.CharField(
        choices=Status.CHOICES.value,
        default=Status.DRAFT.value,
        max_length=6,
        editable=False,
        verbose_name=_('Status'))

    @property
    def is_editable(self) -> bool:
        """ Check order is editable """
        return self.is_trash or self.is_draft


class StatusMessage(models.Model):
    class Meta:
        abstract = True

    @property
    def opts(self):
        return self._meta

    def get_status_msg(self, action):
        msg = _("{}, {} is {}, it can't be {}.")
        return str(msg).format(
                self.opts.verbose_name,
                self,
                self.get_status_display(),
                action
            )


class TrashMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_trashed = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date trashed")
    )

    @property
    def is_trash(self):
        """ Check order status is trashed """
        return self.status == Status.TRASH.value

    def trash(self):
        """ Trash drafted order """
        if self.is_trash:
            return
        if self.is_draft:
            self.status = Status.TRASH.value
            self.date_trashed = timezone.now()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('trash'))


class DraftMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_drafted = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date drafted")
    )

    @property
    def is_draft(self):
        """ Check order status is draft """
        return self.status == Status.DRAFT.value

    def draft(self):
        """ Draft trashed """
        if self.is_draft:
            return
        if self.is_trash:
            self.status = Status.DRAFT.value
            self.date_drafted = timezone.now()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('draft'))


class PendingMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_pending = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date pending")
    )

    @property
    def is_pending(self):
        """ Check order status is pending """
        return self.status == Status.PENDING.value

    def pending(self):
        """ pending trashed """
        if self.is_pending:
            return
        if self.is_trash:
            self.status = Status.PENDING.value
            self.date_pending = timezone.now()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('pending'))


class ValidateMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_validated = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date validated")
    )

    @property
    def is_valid(self):
        """ Check order status is valid """
        return self.status == Status.VALID.value

    @property
    def validate_ignore_condition(self):
        raise NotImplementedError

    @property
    def validate_valid_condition(self):
        raise NotImplementedError

    def pre_validate_action(self):
        pass

    def post_validate_action(self):
        pass

    @transaction.atomic
    def validate(self):
        """ Validate drafted order """
        if self.validate_ignore_condition:
            return
        if self.validate_valid_condition:
            self.pre_validate_action()
            self.status = Status.VALID.value
            self.date_validated = timezone.now()
            self.post_validate_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('validated'))


class ApproveMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_approved = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date approved")
    )

    @property
    def is_approved(self):
        """ Check order status is approved """
        return self.status == Status.APPROVED.value

    @property
    def approve_ignore_condition(self):
        raise NotImplementedError

    @property
    def approve_valid_condition(self):
        raise NotImplementedError

    def pre_approve_action(self):
        pass

    def post_approve_action(self):
        pass

    @transaction.atomic
    def approve(self):
        """ Approve valid order """
        if self.approve_ignore_condition:
            return
        if self.approve_valid_condition:
            self.pre_approve_action()
            self.status = Status.APPROVED.value
            self.date_approved = timezone.now()
            self.post_approve_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('approved'))


class RejectMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_rejected = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date rejected")
    )

    @property
    def is_rejected(self):
        """ Check order status is rejected """
        return self.status == Status.REJECTED.value

    @property
    def reject_ignore_condition(self):
        raise NotImplementedError

    @property
    def reject_valid_condition(self):
        raise NotImplementedError

    def pre_reject_action(self):
        pass

    def post_reject_action(self):
        pass

    @transaction.atomic
    def reject(self):
        """ Reject valid order """
        if self.reject_ignore_condition:
            return
        if self.reject_valid_condition:
            self.pre_reject_action()
            self.status = Status.REJECTED.value
            self.date_rejected = timezone.now()
            self.post_reject_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('rejected'))


class CompleteMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_completed = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date completed")
    )

    @property
    def is_complete(self):
        """ Check order status is complete """
        return self.status == Status.COMPLETE.value

    def pre_complete_action(self):
        pass

    def post_complete_action(self):
        pass

    @property
    def complete_ignore_condition(self):
        raise NotImplementedError

    @property
    def complete_valid_condition(self):
        raise NotImplementedError

    @transaction.atomic
    def complete(self):
        """ Complete validated order """
        if self.complete_ignore_condition:
            return
        if self.complete_valid_condition:
            self.pre_complete_action()
            self.status = Status.COMPLETE.value
            self.date_completed = timezone.now()
            self.post_complete_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('completed'))


class ProcessMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_processed = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date processed")
    )

    @property
    def is_processed(self):
        """ Check order status is processed """
        return self.status == Status.PROCESSED.value

    @property
    def process_ignore_condition(self):
        raise NotImplementedError

    @property
    def process_valid_condition(self):
        raise NotImplementedError

    def pre_process_action(self):
        pass

    def post_process_action(self):
        pass

    @transaction.atomic
    def process(self):
        """ Process valid order """
        if self.process_ignore_condition:
            return
        if self.process_valid_condition:
            self.pre_process_action()
            self.status = Status.PROCESSED.value
            self.date_processed = timezone.now()
            self.post_process_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('processed'))


class PaidMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_paid = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date paid")
    )

    @property
    def paid_ignore_condition(self):
        raise NotImplementedError

    @property
    def paid_valid_condition(self):
        raise NotImplementedError

    def pre_paid_action(self):
        pass

    def post_paid_action(self):
        pass

    @transaction.atomic
    def paid(self):
        """ Paid pending order """
        if self.paid_ignore_condition:
            return
        if self.paid_valid_condition:
            self.pre_paid_action()
            self.status = Status.PAID.value
            self.date_paid = timezone.now()
            self.post_paid_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('paid'))


class CloseMixin(StatusMessage, models.Model):
    class Meta:
        abstract = True

    date_closed = models.DateTimeField(
        null=True, blank=True, editable=False,
        verbose_name=_("date closed")
    )

    @property
    def is_closed(self) -> bool:
        """ Check order status is closed """
        return self.status == Status.CLOSED.value

    @property
    def close_ignore_condition(self):
        raise NotImplementedError

    @property
    def close_valid_condition(self):
        raise NotImplementedError

    def pre_close_action(self):
        pass

    def post_close_action(self):
        pass

    def close(self):
        """ Close the order """
        if self.close_ignore_condition:
            return
        if self.close_valid_condition:
            self.pre_close_action()
            self.status = Status.CLOSED.value
            self.date_closed = timezone.now()
            self.post_close_action()
            self.save()
        else:
            raise PermissionError(self.get_status_msg('closed'))


class ThreeStepStatusMixin(DraftMixin,
                           TrashMixin,
                           ValidateMixin,
                           CompleteMixin,
                           StatusMixin):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> complete
    """

    class Meta:
        abstract = True

    @property
    def validate_valid_condition(self):
        return self.is_draft

    @property
    def validate_ignore_condition(self):
        return self.is_valid

    @property
    def complete_ignore_condition(self):
        return self.is_complete

    @property
    def complete_valid_condition(self):
        return self.is_valid


class FourStepStatusMixin(DraftMixin,
                          TrashMixin,
                          ValidateMixin,
                          ProcessMixin,
                          CompleteMixin,
                          StatusMixin,
                          ):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> process -> complete
    """

    class Meta:
        abstract = True

    @property
    def validate_ignore_condition(self):
        return self.is_valid

    @property
    def validate_valid_condition(self):
        return self.is_draft

    @property
    def process_ignore_condition(self):
        return self.is_processed

    @property
    def process_valid_condition(self):
        return self.is_valid

    @property
    def complete_ignore_condition(self):
        return self.is_complete

    @property
    def complete_valid_condition(self):
        return self.is_valid


class FiveStepStatusMixin(DraftMixin,
                          TrashMixin,
                          ValidateMixin,
                          ApproveMixin,
                          RejectMixin,
                          ProcessMixin,
                          CompleteMixin,
                          StatusMixin):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> approve/reject -> process -> complete
    """

    class Meta:
        abstract = True

    @property
    def validate_ignore_condition(self):
        return self.is_valid

    @property
    def validate_valid_condition(self):
        return self.is_draft

    @property
    def approve_ignore_condition(self):
        return self.is_approved

    @property
    def approve_valid_condition(self):
        return self.is_valid

    @property
    def reject_ignore_condition(self):
        return self.is_rejected

    @property
    def reject_valid_condition(self):
        return self.is_valid

    @property
    def process_ignore_condition(self):
        return self.is_processed

    @property
    def process_valid_condition(self):
        return self.is_approved

    @property
    def complete_ignore_condition(self):
        return self.is_complete

    @property
    def complete_valid_condition(self):
        return self.is_processed
