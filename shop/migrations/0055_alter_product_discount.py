# Generated by Django 4.2.5 on 2024-07-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0054_remove_product_totalstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
