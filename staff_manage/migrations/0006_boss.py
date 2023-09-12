# Generated by Django 4.2.4 on 2023-08-14 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_manage", "0005_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Boss",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="姓名")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("img", models.CharField(max_length=128, verbose_name="头像")),
            ],
        ),
    ]
