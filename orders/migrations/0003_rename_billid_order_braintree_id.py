# Generated by Django 3.2 on 2021-08-12 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_billid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billid',
            new_name='braintree_id',
        ),
    ]
