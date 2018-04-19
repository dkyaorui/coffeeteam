from django.shortcuts import render,HttpResponse,redirect
from Chat.models import Chat
from blog.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def dealChat(request):
    if request.method == "POST":
        chatType = request.POST['chatType']
        print(chatType)
        if chatType == "sendChat":
            toUsername = request.POST['toUsername']
            uid = request.POST['uid']
            chatDetial = request.POST['chatDetial']
            user = User.objects.filter(id = uid).first()
            toUser = User.objects.filter(username = toUsername).first()
            if not toUser:
                return HttpResponse("error")
            Chat.objects.create(user=user,toUser=toUser,content=chatDetial)
            return HttpResponse("发送成功！")
        elif chatType == "getChat":
            print("getting")
            lastChatId = request.POST['lastChatId']
            user = request.user
            print("lastMsgId:",lastChatId)
            print("user:",user)
            chats = Chat.objects.filter(id__gt=lastChatId, toUser=user).all()
            data = serializers.serialize("json", chats)
            return HttpResponse(data)
    return HttpResponse("error")
