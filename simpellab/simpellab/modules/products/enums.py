import enum
from django.utils.translation import ugettext_lazy as _


class ProductType(enum.Enum):
    AST = _('Asset')
    INV = _('Inventory')
    LAB = _('Laboratory')
    LIT = _('Inspection')
    KAL = _('Calibration')
    LIB = _('Research and Development')
    KSL = _('Consultancy')
    PRO = _('Product Certification')
    LAT = _('Training')
    ANY = _('Any')

    CHOICES = (
        ('AST', _('Asset')),
        ('INV', _('Inventory')),
        ('LAB', _('Laboratory')),
        ('LIT', _('Inspection')),
        ('KAL', _('Calibration')),
        ('LIB', _('Research and Development')),
        ('KSL', _('Consultancy')),
        ('PRO', _('Product Certification')),
        ('LAT', _('Training')),
        ('ANY', _('Any')),
    )


class ServiceType(enum.Enum):
    LAB = _('Laboratory')
    LIT = _('Inspection')
    KAL = _('Calibration')
    LIB = _('Research and Development')
    KSL = _('Consultancy')
    PRO = _('Product Certification')
    LAT = _('Training')
    ANY = _('Any')

    CHOICES = (
        ('LAB', _('Laboratory')),
        ('LIT', _('Inspection')),
        ('KAL', _('Calibration')),
        ('LIB', _('Research and Development')),
        ('KSL', _('Consultancy')),
        ('PRO', _('Product Certification')),
        ('LAT', _('Training')),
        ('ANY', _('Any')),
    )
