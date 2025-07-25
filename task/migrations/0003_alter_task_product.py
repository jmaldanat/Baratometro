# Generated by Django 4.2.23 on 2025-07-14 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productprice_link_productprice_sku'),
        ('task', '0002_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='product.product'),
        ),
    ]
