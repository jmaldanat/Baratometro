# Generated by Django 4.2.23 on 2025-07-13 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productprice_max_on_productprice_min_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprice',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productprice',
            name='sku',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
