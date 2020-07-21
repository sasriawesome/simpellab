# Generated by Django 3.0.8 on 2020-07-21 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('name', models.CharField(help_text='Partner name eg. Google .Inc or person name if partner is personal', max_length=255, verbose_name='Partner name')),
                ('is_company', models.BooleanField(default=True, verbose_name='Company')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Customer')),
                ('is_supplier', models.BooleanField(default=False, verbose_name='Supplier')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Balance')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner', to=settings.AUTH_USER_MODEL, verbose_name='User account')),
            ],
            options={
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
                'permissions': (('export_partner', 'Can export Partner'), ('import_partner', 'Can import Partner')),
            },
        ),
        migrations.CreateModel(
            name='PartnerContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='phone')),
                ('fax', models.CharField(blank=True, max_length=128, null=True, verbose_name='fax')),
                ('email', models.CharField(blank=True, help_text='your public email', max_length=128, null=True, verbose_name='email')),
                ('whatsapp', models.CharField(blank=True, max_length=128, null=True, verbose_name='whatsapp')),
                ('website', models.CharField(blank=True, max_length=128, null=True, verbose_name='website')),
                ('partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='simpellab_partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Partner Contact',
                'verbose_name_plural': 'Partner Contacts',
            },
        ),
        migrations.CreateModel(
            name='PartnerAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_primary', models.BooleanField(default=True, verbose_name='primary')),
                ('street', models.CharField(blank=True, max_length=512, null=True, verbose_name='street')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='city')),
                ('province', models.CharField(blank=True, max_length=128, null=True, verbose_name='province')),
                ('country', models.CharField(blank=True, max_length=128, null=True, verbose_name='country')),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True, verbose_name='zip code')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='simpellab_partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Partner Address',
                'verbose_name_plural': 'Partner Addresses',
            },
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('department', models.CharField(blank=True, max_length=255, null=True, verbose_name='Department')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_persons', to='simpellab_partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Contact Person',
                'verbose_name_plural': 'Contact Persons',
            },
        ),
        migrations.CreateModel(
            name='BalanceMutation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('flow', models.CharField(choices=[('IN', 'In'), ('OUT', 'Out')], default='IN', max_length=3, verbose_name='Cash flow')),
                ('reference', models.CharField(max_length=125, verbose_name='reference')),
                ('note', models.TextField(blank=True, max_length=225, null=True, verbose_name='Note')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpellab_partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Balance Mutations',
            },
        ),
    ]
