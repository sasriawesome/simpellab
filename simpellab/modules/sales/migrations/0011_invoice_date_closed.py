# Generated by Django 3.0.8 on 2020-07-20 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales', '0010_remove_invoice_date_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date_closed',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Date closed'),
        ),
    ]