# Generated by Django 5.0 on 2024-07-30 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='device_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
