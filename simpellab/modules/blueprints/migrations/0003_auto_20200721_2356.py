# Generated by Django 3.0.8 on 2020-07-22 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_blueprints', '0002_auto_20200721_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blueprint',
            name='name',
            field=models.CharField(help_text='Sample name or identifier', max_length=512, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='blueprint',
            name='note',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='Note'),
        ),
    ]
