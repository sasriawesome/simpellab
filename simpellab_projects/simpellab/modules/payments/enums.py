from django.utils.translation import ugettext_lazy as _


class PaymentStatus:
    WAITING = 'waiting'
    PREAUTH = 'preauth'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    REFUNDED = 'refunded'
    ERROR = 'error'
    INPUT = 'input'

    CHOICES = [
        (WAITING, _('Waiting for confirmation')),
        (PREAUTH, _('Pre-authorized')),
        (CONFIRMED, _('Confirmed')),
        (REJECTED, _('Rejected')),
        (REFUNDED, _('Refunded')),
        (ERROR, _('Error')),
        (INPUT, _('Input'))]