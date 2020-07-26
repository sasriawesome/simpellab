# Generated by Django 3.0.8 on 2020-07-26 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tenant_users.permissions.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, tenant_users.permissions.models.PermissionsMixinFacade),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('full_name', models.CharField(max_length=30, verbose_name='full name')),
                ('short_name', models.CharField(blank=True, max_length=150, verbose_name='short name')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='Title')),
                ('pid', models.CharField(blank=True, help_text='Personal Identifier Number', max_length=256, null=True, verbose_name='PID')),
                ('gender', models.CharField(choices=[('L', 'Male'), ('P', 'Female')], default='L', max_length=1, verbose_name='gender')),
                ('date_of_birth', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date of birth')),
                ('place_of_birth', models.CharField(blank=True, max_length=255, null=True, verbose_name='place of birth')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User account')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'permissions': (('export_person', 'Can export Person'), ('import_person', 'Can import Person'), ('change_status_person', 'Can change status Person')),
            },
        ),
        migrations.CreateModel(
            name='PersonContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='phone')),
                ('fax', models.CharField(blank=True, max_length=128, null=True, verbose_name='fax')),
                ('email', models.CharField(blank=True, help_text='your public email', max_length=128, null=True, verbose_name='email')),
                ('whatsapp', models.CharField(blank=True, max_length=128, null=True, verbose_name='whatsapp')),
                ('website', models.CharField(blank=True, max_length=128, null=True, verbose_name='website')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sister_auth.Person')),
            ],
            options={
                'verbose_name': 'Person address',
                'verbose_name_plural': 'Person addresses',
            },
        ),
        migrations.CreateModel(
            name='PersonAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_primary', models.BooleanField(default=True, verbose_name='primary')),
                ('name', models.CharField(choices=[('home', 'Home'), ('office', 'Office')], default='home', help_text='E.g. Home Address or Office Address', max_length=256, null=True, verbose_name='name')),
                ('street', models.CharField(blank=True, max_length=512, null=True, verbose_name='street')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='city')),
                ('province', models.CharField(blank=True, max_length=128, null=True, verbose_name='province')),
                ('country', models.CharField(blank=True, max_length=128, null=True, verbose_name='country')),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True, verbose_name='zip code')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='sister_auth.Person')),
            ],
            options={
                'verbose_name': 'Person address',
                'verbose_name_plural': 'Person addresses',
            },
        ),
    ]
