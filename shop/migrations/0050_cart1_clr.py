# Generated by Django 4.2.5 on 2024-07-15 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0049_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart1',
            name='clr',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.product_color'),
        ),
    ]
