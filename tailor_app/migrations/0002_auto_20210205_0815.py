# Generated by Django 3.1.1 on 2021-02-05 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Processing', 'Processing'), ('Ready', 'Ready'), ('Delivered', 'Delivered')], default='Confirmed', max_length=100),
        ),
    ]
