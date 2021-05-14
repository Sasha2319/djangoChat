# Generated by Django 3.2 on 2021-04-07 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatuser_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_chat', models.CharField(max_length=50, verbose_name='Названия чата')),
                ('ChatUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chatuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50, verbose_name='Имя автора сообщения')),
                ('messageText', models.TextField(verbose_name='Текст сообщения')),
                ('pub_date', models.TimeField(auto_now_add=True, verbose_name='время публикации сообщения')),
                ('Chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]