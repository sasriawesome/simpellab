# Generated by Django 3.0.8 on 2020-07-20 06:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simpellab_products', '0001_initial'),
        ('simpellab_sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingOrder',
            fields=[
                ('salesorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_sales.SalesOrder')),
            ],
            options={
                'verbose_name': 'Training Order',
                'verbose_name_plural': 'Training Orders',
            },
            bases=('simpellab_sales.salesorder',),
        ),
        migrations.CreateModel(
            name='TrainingService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Service')),
                ('audience_min', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Minimum audience')),
                ('audience_criterias', models.TextField(max_length=2048, verbose_name='Audience criterias')),
            ],
            options={
                'verbose_name': 'Training and Coaching',
                'verbose_name_plural': 'Training and Coachings',
            },
            bases=('simpellab_products.service',),
        ),
        migrations.CreateModel(
            name='TrainingTopic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(max_length=2048)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='simpellab_sales_training.TrainingService', verbose_name='Service')),
            ],
            options={
                'verbose_name': 'Training Topic',
                'verbose_name_plural': 'Training Topics',
            },
        ),
        migrations.CreateModel(
            name='TrainingOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_sales.OrderItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='simpellab_sales_training.TrainingOrder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='simpellab_sales_training.TrainingService')),
            ],
            options={
                'verbose_name': 'Training Order Item',
                'verbose_name_plural': 'Training Order Items',
            },
            bases=('simpellab_sales.orderitem',),
        ),
    ]
