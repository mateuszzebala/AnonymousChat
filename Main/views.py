from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as login_user, authenticate, logout as logout_user
from .models import Chat, AnonymousUser, Text
from django.db.models import Q
from django.contrib.auth.models import User

def index(request):
    return render(request, "index.html", {})

def new_chat(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        chat = Chat.objects.filter(user2__isnull=True).first()
        if chat is None:
            chat = Chat(user1=request.anon)
            chat.save()
        else:
            chat.user2 = request.anon
            chat.save()
    return chat


def chat(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        chat = new_chat(request)
    return render(request, "chat.html", {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect('index')
        else:
            return render(request, "login.html", {"bad":True})
        
        
    return render(request, "login.html", {})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User(username=username, email=email, password=password)
        user.save()
        return redirect('login')
        
    return render(request, "register.html", {
        
    })

def logout(request):
    logout_user(request)
    return redirect('index')

@csrf_exempt
def message(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    data = json.loads(request.body.decode("utf-8"))
    text = data.get('text')
    if chat.user1 == request.anon:
        chat.user1_typeing = False
    elif chat.user2 == request.anon:
        chat.user2_typeing = False
    chat.save()
    
    if text != "" and text is not None and chat is not None and chat.is_connected():
        text = Text(user=request.anon, chat=chat, content=text)
        text.save()
    return JsonResponse({})

@csrf_exempt
def messages(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        return JsonResponse({})
    texts = Text.objects.filter(chat=chat)
    txts = {
        'typeing': chat.user1_typeing if chat.user2 == request.anon else chat.user2_typeing,
        'messages': dict()
    }
    i = 0
    for txt in texts:
        txts['messages'][i] = {"from":1 if txt.user == request.anon else 0, "text":txt.content}
        i += 1
    return JsonResponse(txts)

@csrf_exempt
def next_chat(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        chat = new_chat(request)
        return JsonResponse({})
    if chat.user1 == request.anon:
        chat.user1 = None
    else:
        chat.user2 = None
    chat.save()
    if chat.user1 is None and chat.user2 is None:
        chat.delete()
    chat = new_chat(request)
    return JsonResponse({})
    
@csrf_exempt
def disconnect(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        return JsonResponse({})
    
    chat.delete()
    
    return JsonResponse({})
    
@csrf_exempt
def chat_info(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat is None:
        return JsonResponse({
            "two_users": False,
        })
    return JsonResponse({
        "two_users": chat.is_connected()
    })


def typeing(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat.user1 == request.anon:
        chat.user1_typeing = True
    else:
        chat.user2_typeing = True
    chat.save()

    return JsonResponse({})

def not_typeing(request):
    chat = Chat.objects.filter(Q(user1=request.anon) | Q(user2=request.anon)).first()
    if chat.user1 == request.anon:
        chat.user1_typeing = False
    else:
        chat.user2_typeing = False
    chat.save()

    return JsonResponse({})


def favicon(request):
    return FileResponse(open("static/img/favicon.ico", "rb"))

def map(request):
    return FileResponse(open('static/map.xml'))


def error404(request):
    return render(request, "404.html", {})