# Generated by Django 4.2.5 on 2024-07-12 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_cart_product_quantity_available_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity_available',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
