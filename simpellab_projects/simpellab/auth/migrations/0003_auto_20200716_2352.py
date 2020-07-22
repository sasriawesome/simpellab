# Generated by Django 3.0.8 on 2020-07-17 06:52

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_auth', '0002_auto_20200716_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaddress',
            name='privacy',
        ),
        migrations.AddField(
            model_name='personaddress',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='personaddress',
            name='modified_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]