# Generated by Django 3.1.1 on 2021-02-05 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailor_app', '0003_auto_20210205_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]