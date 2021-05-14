from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, ChatIdForm
from .models import ChatUser, Chat
import locale
import time
from django.views.decorators.csrf import csrf_exempt
from . import utils
import socket
from .utils import get_ip
from djangoChat.settings import STATIC_URL
from django.utils import timezone

# Create your views here.

def home(request):
    usernametohtml = ""
    usernameBool = False
    ip, pc = get_ip(request)
    suForm = SignUpForm()
    if request.POST.get("name"):
        for chatuser in ChatUser.objects.all():
            if chatuser.name == request.POST.get("name"):
                return render(request, 'chat/index.html',
                              {'formSignUp': SignUpForm, 'formLogin': LoginForm, 'ip': ip, 'restart': False,
                               'errorSignUp': True})
        utils.user['name'] = request.POST.get("name")
        utils.user['password'] = request.POST.get("password")
        utils.user['email'] = request.POST.get("email")
        utils.user['dateOfBirth'] = request.POST.get("dateOfBirth")
        utils.user['ip'] = " " + ip
        utils.user['lastPC'] = pc
        locale.setlocale(locale.LC_TIME, "ru_RU")
        date = time.strftime("%Y-%m-%d")
        if not request.POST.get("dateOfBirth"):
            utils.user['dateOfBirth'] = date
        a = ChatUser.objects.create(name=utils.user["name"], email=utils.user["email"], password=utils.user["password"], dateOfBirth=utils.user['dateOfBirth'], ip=utils.user['ip'], lastPC=utils.user['lastPC'])
        a.save()
        return render(request, 'chat/index.html', {'formSignUp': SignUpForm, 'formLogin': LoginForm, 'ip': ip, 'date': date, 'restart': True, })

    done = False
    for chatuser in ChatUser.objects.all():
        if chatuser.ip:
            for cIp in chatuser.ip.split(' '):
                if cIp == ip:
                    utils.user['name'] = chatuser.name
                    usernametohtml = chatuser.name
                    usernameBool = True
                    print(chatuser, chatuser.chat_set.all(), "   ll")
                    done = True

    if not done:
        utils.user = {}

    if request.GET.get("loginName"):
        print("request.get()")
        done = False
        for chatuser in ChatUser.objects.all():
            if chatuser.name == request.GET.get("loginName") and chatuser.password == request.GET.get("loginPassword"):
                chatuser.ip = chatuser.ip + " " + ip
                chatuser.lastPC = socket.gethostname()
                chatuser.save()
                utils.user['name'] = request.GET.get("loginName")
                utils.user['lastPC'] = socket.gethostname()
                print(chatuser.ip)
                done = True
                return HttpResponseRedirect('/home/')
        if not done:
            utils.user = {}
            return render(request, 'chat/index.html', {'formSignUp': SignUpForm, 'formLogin': LoginForm, 'ip': ip, 'restart': False, 'error': True})

    return render(request, 'chat/index.html', {'formSignUp': suForm, 'formLogin': LoginForm, 'ip': ip, 'username': usernametohtml, 'userBool': usernameBool})



def index(request):
    return HttpResponseRedirect("/home/")


@csrf_exempt
def chats(request):
    utils.allchats = []
    usersToLogout = []
    chatIdForm = ChatIdForm()
    ip, pc = get_ip(request)

    done=False
    for chatuser in ChatUser.objects.all():
        if request.GET.get(f"check{chatuser.id}"):
            usersToLogout.append(chatuser.id)
            done = True
    if done:
        print(usersToLogout)
        for userId in usersToLogout:
            logoutuser = ChatUser.objects.get(id=userId)
            if logoutuser.ip:
                for cIp in logoutuser.ip.split(" "):
                    if cIp == ip:
                        logoutuser.ip = logoutuser.ip.split(" ")
                        logoutuser.ip.remove(cIp)
                        logoutuser.ip = ' '.join(logoutuser.ip)
            logoutuser.lastPC = ''
            logoutuser.save()
        return HttpResponseRedirect("/chats/")


    done = False
    for chatuser in ChatUser.objects.all():
        if chatuser.ip:
            for cIp in chatuser.ip.split(' '):
                print(f'{ip}-{cIp}')
                if cIp == ip and chatuser.lastPC == pc:
                    print()
                    utils.user['name'] = chatuser.name
                    print(chatuser, chatuser.chat_set.all())
                    done = True
                    for c in chatuser.chat_set.all():
                        print(c)
                        if c not in utils.allchats:
                            utils.allchats.append(c)

        for cUser2 in ChatUser.objects.all():
            if cUser2.id != chatuser.id:
                print("-d")
                if chatuser.lastPC == cUser2.lastPC and chatuser.lastPC and cUser2.lastPC:
                    print('okokok')
                    string = str(chatuser.lastPC)
                    string += str(cUser2.lastPC)
                    print(chatuser, cUser2)
                    usersWithOnePc = []

                    for u in ChatUser.objects.all():
                        for j in ChatUser.objects.all():
                            if u != j:
                                if u.lastPC == j.lastPC and u.lastPC and j.lastPC:
                                    if u not in usersWithOnePc:
                                        usersWithOnePc.append(u)
                                    if j not in usersWithOnePc:
                                        usersWithOnePc.append(j)

                    return render(request, 'chat/LogOut.html', {'cUser2': cUser2, 'chatuser': chatuser, 'UWOP': usersWithOnePc})

            else:
                print(1111111)


    if not done:
        return HttpResponse("<center><h1>Sign up or login please</h1></br><a href='/home/'>Go Home page</a></center>")

    for c in Chat.objects.all():
        for member in c.members.split(" "):
            if member == utils.user['name']:
                print(member)
                for j in Chat.objects.filter(id=c.id):
                    if j not in utils.allchats:
                        utils.allchats.append(j)

    if request.POST.get("chatId"):
        chat = Chat.objects.get(id = request.POST.get("chatId"))
        if chat:
            chat.members += " " + str(utils.user['name'])
            chat.save()
            return HttpResponseRedirect("/chats/")

    utils.allchats.sort(key=lambda x: x.lastMessageTime, reverse=True)
    return render(request, 'chat/chats.html', {'chats': utils.allchats, 'chatIdForm': chatIdForm, 'username': utils.user['name'], 'userBool': True})




def chatView(request, chat_id):
    pc = socket.gethostname()
    ip, pc = get_ip(request)
    try:
        a = Chat.objects.get(id=chat_id)
    except:
        return HttpResponse("404 Errror")

    done = False
    for chatuser in ChatUser.objects.all():
        if chatuser.ip:
            for cIp in chatuser.ip.split(' '):
                print(f'{ip}-{cIp}')
                if cIp == ip and chatuser.lastPC == pc:
                    print()
                    utils.user['name'] = chatuser.name
                    print(chatuser, chatuser.chat_set.all())
                    done = True

    if request.is_ajax():
        data = {
            'author_name': request.POST.get('author_name'),
            'messageText': request.POST.get('messageText'),
        }
        locale.setlocale(locale.LC_TIME, "ru_RU")
        data['pub_date'] = time.strftime("%d %B %Y г. %H:%M")

        a.message_set.create(author_name=data['author_name'],messageText=data['messageText'],pub_date=timezone.now())
        a.save()

        return JsonResponse(data)

    chat = Chat.objects.get(id=chat_id)
    messages_set = chat.message_set.order_by('pub_date')
    messages = []
    for m in messages_set:
        if m.author_name == utils.user['name']:
            messages.append({
                'author_name': m.author_name,
                'messageText': m.messageText,
                'pub_date': m.pub_date,
                'sender': 'me'
            })
        else:
            messages.append({
                'author_name': m.author_name,
                'messageText': m.messageText,
                'pub_date': m.pub_date,
                'sender': 'you'
            })
    return render(request, 'chat/chat.html', {'chatId': chat_id, 'messages': messages, 'username':utils.user['name'], 'static': STATIC_URL})




def logout(request):
    ip, pc = get_ip(request)
    for chatuser in ChatUser.objects.all():
        if chatuser.ip:
            for cIp in chatuser.ip.split(' '):
                print(f'{ip}-{cIp}')
                if cIp == ip:
                    print("=============")
                    chatuser.ip = chatuser.ip.split(' ')
                    chatuser.ip.remove(cIp)
                    chatuser.ip = ' '.join(chatuser.ip)
                    print(chatuser.ip.split(' '))
                    print(chatuser.ip)
                    chatuser.lastPC = ''
                    chatuser.save()
                    return HttpResponseRedirect("/home/")

def changePassword(request):
    pass

