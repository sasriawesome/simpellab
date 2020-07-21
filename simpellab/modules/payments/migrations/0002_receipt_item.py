# Generated by Django 3.0.8 on 2020-07-21 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simpellab_payments', '0001_initial'),
        ('simpellab_sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpellab_sales.Invoice', verbose_name='Item'),
        ),
    ]
