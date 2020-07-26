from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from sister.tenants.models import Client, Domain

class Command(BaseCommand):
    help = 'Setups Sister Tenants'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):

        # create your public tenant
        tenant = Client(schema_name='public',
                        name='Schemas Inc.',
                        paid_until='2016-12-05',
                        on_trial=False)
        tenant.save()

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = 'localhost' # don't add your port or www here! on a local server you'll want to use localhost here
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()



