# Generated by Django 3.0.8 on 2020-07-20 06:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('simpellab_partners', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(blank=True, max_length=80, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='simpellab_products.Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('alias_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alias name')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=80, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='fee')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(0)], verbose_name='total price')),
                ('is_locked', models.BooleanField(default=False, editable=False, help_text='Lock to prevent unwanted editing', verbose_name='Locked')),
                ('is_active', models.BooleanField(default=True, editable=False, help_text='Deletion is not good, set to inactive instead', verbose_name='Active')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='simpellab_products.Category', verbose_name='Category')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_simpellab_products.product_set+', to='contenttypes.ContentType')),
                ('suppliers', models.ManyToManyField(blank=True, limit_choices_to={'is_supplier': True}, related_name='products', to='simpellab_partners.Partner', verbose_name='Suppliers')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'permissions': (('lock_product', 'Can lock Product'), ('unlock_product', 'Can unlock Product'), ('export_product', 'Can export Product'), ('import_product', 'Can import Product')),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Product')),
                ('sn', models.CharField(blank=True, max_length=150, null=True, verbose_name='serial number')),
                ('min_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='min stock')),
                ('max_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='max stock')),
                ('stock_on_hand', models.IntegerField(default=0, verbose_name='stock on hand')),
                ('stock_on_delivery', models.IntegerField(default=0, verbose_name='stock on delivery')),
                ('stock_on_request', models.IntegerField(default=0, verbose_name='stock on request')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
                'permissions': (('lock_asset', 'Can lock Asset'), ('unlock_asset', 'Can unlock Asset'), ('export_asset', 'Can export Asset'), ('import_asset', 'Can import Asset')),
            },
            bases=('simpellab_products.product', models.Model),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Product')),
                ('sn', models.CharField(blank=True, max_length=150, null=True, verbose_name='serial number')),
                ('min_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='min stock')),
                ('max_stock', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='max stock')),
                ('stock_on_hand', models.IntegerField(default=0, verbose_name='stock on hand')),
                ('stock_on_delivery', models.IntegerField(default=0, verbose_name='stock on delivery')),
                ('stock_on_request', models.IntegerField(default=0, verbose_name='stock on request')),
                ('display_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
                'permissions': (('lock_inventory', 'Can lock Inventory'), ('unlock_inventory', 'Can unlock Inventory'), ('export_inventory', 'Can export Inventory'), ('import_inventory', 'Can import Inventory')),
            },
            bases=('simpellab_products.product', models.Model),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_products.Product')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'permissions': (('lock_service', 'Can lock Service'), ('unlock_service', 'Can unlock Service'), ('export_service', 'Can export Service'), ('import_service', 'Can import Service')),
            },
            bases=('simpellab_products.product',),
        ),
        migrations.CreateModel(
            name='TaggedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_products', to='simpellab_products.Product')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_products', to='simpellab_products.Tag')),
            ],
            options={
                'verbose_name': 'Tagged',
                'verbose_name_plural': 'Taggeds',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='products', through='simpellab_products.TaggedProduct', to='simpellab_products.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_of_measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='simpellab_products.UnitOfMeasure', verbose_name='Unit'),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('ptype', models.CharField(choices=[('LAB', 'Laboratory'), ('LIT', 'Inspection')], default='Laboratory', max_length=3, verbose_name='Parameter type')),
                ('code', models.CharField(blank=True, max_length=128, null=True, verbose_name='code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='price')),
                ('date_effective', models.DateField(default=django.utils.timezone.now, verbose_name='Date effective')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='simpellab_products.UnitOfMeasure', verbose_name='Unit')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Price')),
                ('date_effective', models.DateField(default=django.utils.timezone.now, verbose_name='Date effective')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='simpellab_products.UnitOfMeasure', verbose_name='Unit')),
            ],
            options={
                'verbose_name': 'Fee',
                'verbose_name_plural': 'Fees',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('feature', models.CharField(max_length=255, verbose_name='Feature')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='simpellab_products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Specification',
                'verbose_name_plural': 'Specifications',
                'unique_together': {('product', 'feature')},
            },
        ),
        migrations.CreateModel(
            name='ProductFee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Price')),
                ('date_effective', models.DateField(default=django.utils.timezone.now, verbose_name='Date effective')),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_fees', to='simpellab_products.Fee', verbose_name='Fee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_fees', to='simpellab_products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Fee',
                'verbose_name_plural': 'Product Fees',
                'unique_together': {('product', 'fee')},
            },
        ),
    ]
