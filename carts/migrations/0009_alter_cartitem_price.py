# Generated by Django 4.0.5 on 2022-08-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_alter_cartitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
