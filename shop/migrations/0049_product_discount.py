# Generated by Django 5.0.6 on 2024-07-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_rename_product_color_product_color_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(null=True),
        ),
    ]
