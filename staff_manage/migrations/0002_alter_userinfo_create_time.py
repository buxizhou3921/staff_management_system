# Generated by Django 4.2.4 on 2023-08-07 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_manage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="create_time",
            field=models.DateField(verbose_name="入职时间"),
        ),
    ]
