# Generated by Django 4.2.5 on 2024-07-13 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_cart1_gst'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart1',
            name='gst',
        ),
    ]
