# Generated by Django 3.0.8 on 2020-07-18 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales_inspection', '0003_auto_20200718_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionserviceparameter',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='simpellab_sales_inspection.InspectionService', verbose_name='Service'),
        ),
    ]
