# Generated by Django 3.0.8 on 2020-07-20 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales', '0006_salesorder_qrcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='refund',
            new_name='refundable',
        ),
    ]
