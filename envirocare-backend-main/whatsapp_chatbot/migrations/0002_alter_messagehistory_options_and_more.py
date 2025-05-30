# Generated by Django 5.1.7 on 2025-03-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp_chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagehistory',
            options={'ordering': ['-created_at'], 'verbose_name': 'Message History', 'verbose_name_plural': 'Message Histories'},
        ),
        migrations.AlterModelOptions(
            name='responsecache',
            options={'ordering': ['-created_at'], 'verbose_name': 'Response Cache', 'verbose_name_plural': 'Response Caches'},
        ),
        migrations.AlterModelOptions(
            name='whatsappuser',
            options={'ordering': ['-created_at'], 'verbose_name': 'WhatsApp User', 'verbose_name_plural': 'WhatsApp Users'},
        ),
        migrations.RemoveField(
            model_name='whatsappuser',
            name='last_interaction',
        ),
        migrations.AddField(
            model_name='whatsappuser',
            name='state_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='messagehistory',
            name='message_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='responsecache',
            name='key',
            field=models.CharField(max_length=255),
        ),
    ]
