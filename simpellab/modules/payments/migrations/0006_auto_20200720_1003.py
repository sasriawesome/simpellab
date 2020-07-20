# Generated by Django 3.0.8 on 2020-07-20 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_payments', '0005_auto_20200720_0911'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'verbose_name': 'Method', 'verbose_name_plural': 'Methods'},
        ),
        migrations.AlterField(
            model_name='cashflow',
            name='ptype',
            field=models.CharField(blank=True, choices=[('DP', 'Down Payment'), ('RP', 'Repayment')], default=None, help_text='Determine Down Payment or Repayment', max_length=2, null=True, verbose_name='Payment Type'),
        ),
    ]