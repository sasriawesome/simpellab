import xlrd
import uuid
from logging import getLogger
from datetime import date, datetime

from django.conf import settings
from django.utils import datetime_safe, timezone
from django.utils.encoding import force_text

from import_export import widgets


class ExcelDateWidget(widgets.Widget):
    """ Widget for converting excel date fields """

    def __init__(self, date_format=None, date_mode=0):
        if date_format is None:
            if not settings.DATE_INPUT_FORMATS:
                formats = ("%Y-%m-%d",)
            else:
                formats = settings.DATE_INPUT_FORMATS
        else:
            formats = (date_format,)
        self.formats = formats
        self.date_mode = date_mode

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        if isinstance(value, date):
            return value
        try:
            return timezone.datetime(*xlrd.xldate_as_tuple(value, datemode=self.date_mode)[0:3])
        except ValueError:
            for date_format in self.formats:
                try:
                    return timezone.make_aware(datetime.strptime(value, date_format).date())
                except (ValueError, TypeError):
                    logger = getLogger()
                    logger.debug('Cannot create Date object from ' + str(value))

    def render(self, value, obj=None):
        if not value:
            return ""
        try:
            return value.strftime(self.formats[0])
        except:
            return datetime_safe.new_date(value).strftime(self.formats[0])


class UUIDWidget(widgets.Widget):
    """
    Widget for converting UUID fields.
    """

    def render(self, value, obj=None):
        if value in [None, '']:
            return None
        return str(value)

    def clean(self, value, row=None, *args, **kwargs):
        if value in [None, '']:
            return None
        return uuid.UUID('{%s}' % force_text(value))
