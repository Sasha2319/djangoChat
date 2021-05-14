# Generated by Django 3.2 on 2021-04-18 09:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_chat_lastmassagetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='lastMassageTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата последнего сообщения'),
        ),
    ]
