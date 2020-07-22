# Generated by Django 3.0.8 on 2020-07-21 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_products', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('simpellab_carts', '0002_auto_20200721_0217'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonCart',
            fields=[
                ('cart_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simpellab_carts.Cart')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='simpellab_products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Common Cart',
                'verbose_name_plural': 'Common Carts',
            },
            bases=('simpellab_carts.cart',),
        ),
        migrations.RemoveField(
            model_name='commoncartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='commoncartitem',
            name='cartitem_ptr',
        ),
        migrations.RemoveField(
            model_name='commoncartitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_simpellab_carts.cart_set+', to='contenttypes.ContentType'),
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='CommonCartItem',
        ),
    ]
