# Generated by Django 3.0.8 on 2020-07-20 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_partners', '0002_auto_20200720_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancemutation',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Balance'),
        ),
    ]