# Generated by Django 3.2 on 2021-04-27 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_chatuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=True, verbose_name='Просмотрено'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.TimeField(auto_now_add=True, verbose_name='Время публикации сообщения'),
        ),
    ]