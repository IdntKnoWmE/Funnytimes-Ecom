# Generated by Django 4.0 on 2022-03-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funnytimes', '0006_order_order_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['order_date', 'order_id']},
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='razon_payment_id',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
