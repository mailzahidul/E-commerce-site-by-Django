# Generated by Django 3.2 on 2021-05-13 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_mulytic_labs_test_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mulytic_labs_test',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_code/'),
        ),
    ]