# Generated by Django 3.2 on 2021-04-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_chatuser_lastpc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='lastPC',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Последнее устройство'),
        ),
    ]
