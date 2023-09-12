# Generated by Django 4.2.4 on 2023-08-08 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_manage", "0003_prettynum_alter_userinfo_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="Admin",
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
                ("username", models.CharField(max_length=32, verbose_name="用户名")),
                ("password", models.CharField(max_length=64, verbose_name="密码")),
            ],
        ),
    ]