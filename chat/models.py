from django.db import models
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True  # specify this model as an Abstract Model
        app_label = 'chat'

class ChatUser(BaseModel):
    name = models.CharField('имя пользователя', max_length=50, unique=True)
    password = models.CharField('Пароль', max_length=50)
    email = models.CharField('Email', blank=True, max_length=50, null=True)
    dateOfBirth = models.DateField('Дата рождения', blank=True, null=True)
    ip = models.TextField('Ip, если несколько, через пробел:', blank=True)
    lastPC = models.CharField('Последнее устройство', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Chat(BaseModel):
    ChatUser = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    name_of_chat = models.CharField('Названия чата', max_length=50)
    members = models.TextField('Участники чата через пробел', null=True, blank=True)
    lastMessageTime = models.DateTimeField('Дата последнего сообщения', default=timezone.now)

    def __str__(self):
        return self.name_of_chat

    def update(self):
        self.lastMessageTime = timezone.now()

class Message(BaseModel):
    Chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author_name = models.CharField('Имя автора сообщения', max_length=50)
    messageText = models.TextField('Текст сообщения')
    pub_date = models.DateTimeField('Время публикации сообщения')
    def __str__(self):
        return self.author_name


# class Chat(models.Model):

