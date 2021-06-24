# Generated by Django 3.2 on 2021-05-04 06:19

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='yourmailaddress@yourserver.com', max_length=254),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+8841524204242', max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]