# Generated by Django 3.2 on 2021-05-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_out_source',
            field=models.URLField(null=True),
        ),
    ]
