# Generated by Django 3.0.8 on 2020-07-17 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales', '0009_auto_20200717_0602'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trainingorderitem',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='trainingorderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='trainingorderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='TrainingOrder',
        ),
        migrations.DeleteModel(
            name='TrainingOrderItem',
        ),
    ]
