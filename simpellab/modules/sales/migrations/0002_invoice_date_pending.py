# Generated by Django 3.0.8 on 2020-07-20 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date_pending',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='date pending'),
        ),
    ]
