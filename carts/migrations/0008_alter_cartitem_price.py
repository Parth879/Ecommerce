# Generated by Django 4.0.5 on 2022-08-04 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_alter_cartitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
