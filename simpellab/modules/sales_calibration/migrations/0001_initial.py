# Generated by Django 3.0.8 on 2020-07-17 15:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simpellab_sales', '0001_initial'),
        ('simpellab_products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalibrationOrder',
            fields=[
                ('salesorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_sales.SalesOrder')),
            ],
            options={
                'verbose_name': 'Calibration Order',
                'verbose_name_plural': 'Calibration Orders',
            },
            bases=('simpellab_sales.salesorder',),
        ),
        migrations.CreateModel(
            name='CalibrationService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Service')),
            ],
            options={
                'verbose_name': 'Calibration',
                'verbose_name_plural': 'Calibration',
            },
            bases=('simpellab_products.service',),
        ),
        migrations.CreateModel(
            name='CalibrationOrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('name', models.CharField(blank=True, max_length=512, null=True, verbose_name='Name')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Product price')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Minimal value: 1'), django.core.validators.MaxValueValidator(500, message='Maximal value: 500')], verbose_name='Quantity')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Total Price')),
                ('note', models.CharField(blank=True, max_length=512, null=True, verbose_name='Note')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='simpellab_sales_calibration.CalibrationOrder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='simpellab_sales_calibration.CalibrationService')),
            ],
            options={
                'verbose_name': 'Calibration Order Item',
                'verbose_name_plural': 'Calibration Order Items',
                'ordering': ('product',),
                'unique_together': {('order', 'product')},
            },
        ),
    ]
