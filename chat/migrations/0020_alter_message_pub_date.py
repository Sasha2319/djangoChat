# Generated by Django 3.2 on 2021-05-02 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_auto_20210427_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.TimeField(auto_now=True, verbose_name='Время публикации сообщения'),
        ),
    ]
