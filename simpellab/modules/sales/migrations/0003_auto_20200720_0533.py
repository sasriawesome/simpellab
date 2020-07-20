# Generated by Django 3.0.8 on 2020-07-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpellab_sales', '0002_invoice_date_pending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='downpayment',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='repayment',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('TRS', 'Trash'), ('DRF', 'Draft'), ('VLD', 'Valid'), ('APP', 'Approved'), ('RJC', 'Rejected'), ('PRS', 'Processed'), ('CMP', 'Complete'), ('INV', 'Invoiced'), ('PND', 'Pending'), ('UNP', 'Un Paid'), ('PID', 'Paid'), ('CLS', 'Closed'), ('PST', 'Posted')], default='DRF', max_length=6, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(choices=[('TRS', 'Trash'), ('DRF', 'Draft'), ('VLD', 'Valid'), ('APP', 'Approved'), ('RJC', 'Rejected'), ('PRS', 'Processed'), ('CMP', 'Complete'), ('INV', 'Invoiced'), ('PND', 'Pending'), ('UNP', 'Un Paid'), ('PID', 'Paid'), ('CLS', 'Closed'), ('PST', 'Posted')], default='DRF', max_length=6, verbose_name='Status'),
        ),
    ]