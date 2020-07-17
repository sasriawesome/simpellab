import enum
from django.utils.translation import ugettext_lazy as _


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class ActiveStatus(enum.Enum):
    ACTIVE = 'ACT'
    INACTIVE = 'INC'

    CHOICES = (
        (ACTIVE, _("active")),
        (INACTIVE, _("inactive")),
    )


class PrivacyStatus(enum.Enum):
    ME = 1
    USERS = 2
    FRIENDS = 3
    STUDENTS = 4
    TEACHERS = 5
    EMPLOYEES = 6
    MANAGERS = 7
    ANYONE = 99

    CHOICES = (
        (ME, _('Only me')),
        (USERS, _('All users')),
        (FRIENDS, _('All friends')),
        (STUDENTS, _('All students')),
        (TEACHERS, _('All teachers')),
        (EMPLOYEES, _('All employees')),
        (MANAGERS, _('All managers')),
        (ANYONE, _("Anyone"))
    )


class Status(enum.Enum):
    TRASH = 'TRS'
    DRAFT = 'DRF'
    VALID = 'VLD'
    APPROVED = 'APP'
    REJECTED = 'RJC'
    PROCESSED = 'PRS'
    COMPLETE = 'CMP'
    INVOICED = 'INV'
    PENDING = 'PND'
    UNPAID = 'UNP'
    PAID = 'PID'
    CLOSED = 'CLS'
    POSTED = 'PST'

    CHOICES = (
        (TRASH, _('Trash')),
        (DRAFT, _('Draft')),
        (VALID, _('Valid')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (PROCESSED, _('Processed')),
        (COMPLETE, _('Complete')),
        (INVOICED, _('Invoiced')),
        (PENDING, _('Pending')),
        (UNPAID, _('Un Paid')),
        (PAID, _('Paid')),
        (CLOSED, _('Closed')),
        (POSTED, _('Posted')),
    )
