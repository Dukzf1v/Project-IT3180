# Generated by Django 5.2.1 on 2025-06-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment_management', '0009_alter_chitietphitheothang_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chitietphitheothang',
            name='so_tien',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
