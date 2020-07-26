# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model

# from tenant_users.tenants.tasks import provision_tenant
# from tenant_users.tenants.utils import create_public_tenant


# class Command(BaseCommand):
#     help = 'Setups Sister Tenants'

#     def __init__(self, *args, **kwargs):
#         super(Command, self).__init__(*args, **kwargs)

#     def handle(self, *args, **options):
#         create_public_tenant("localhost", "admin@example.com")
#         user_model = get_user_model()
#         user_model.objects.create_superuser(email="superuser@example.com", password='password', is_active=True)

#         user_model.objects.create_user(email="tenant1@example.com", password='password', is_active=True, is_staff=True)
#         provision_tenant("Tenant1", "tenant1", "tenant1@example.com", is_staff=True)

#         user_model.objects.create_user(email="tenant2@example.com", password='password', is_active=True, is_staff=True)
#         provision_tenant("Tenant2", "tenant2", "tenant2@example.com", is_staff=True)
#         print('Done')



