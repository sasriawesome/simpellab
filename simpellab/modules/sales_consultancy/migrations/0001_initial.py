# Generated by Django 3.0.8 on 2020-07-20 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simpellab_products', '0001_initial'),
        ('simpellab_sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultancyOrder',
            fields=[
                ('salesorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_sales.SalesOrder')),
            ],
            options={
                'verbose_name': 'Consultancy Order',
                'verbose_name_plural': 'Consultancy Orders',
            },
            bases=('simpellab_sales.salesorder',),
        ),
        migrations.CreateModel(
            name='ConsultancyService',
            fields=[
                ('service_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Service')),
            ],
            options={
                'verbose_name': 'Consultancy',
                'verbose_name_plural': 'Consultancies',
            },
            bases=('simpellab_products.service',),
        ),
        migrations.CreateModel(
            name='ConsultancyOrderItem',
            fields=[
                ('orderitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_sales.OrderItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='simpellab_sales_consultancy.ConsultancyOrder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='simpellab_sales_consultancy.ConsultancyService')),
            ],
            options={
                'verbose_name': 'Consultancy Order Item',
                'verbose_name_plural': 'Consultancy Order Items',
            },
            bases=('simpellab_sales.orderitem',),
        ),
    ]
