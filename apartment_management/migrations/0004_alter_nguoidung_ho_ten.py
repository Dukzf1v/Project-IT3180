# Generated by Django 5.2.1 on 2025-06-02 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment_management', '0003_danhsachphidonggop_noi_dung_nguoidung_ho_ten_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoidung',
            name='ho_ten',
            field=models.CharField(max_length=100),
        ),
    ]
