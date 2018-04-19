from django.shortcuts import render,redirect,HttpResponse
from blog.models import *
from Chat.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
from django.conf import settings as django_settings
from utils.method import PageHalper,save_file,listHelper_small,listHelper_big,comment_list_helper,random_codeStr
import time
import os,base64
import json

# Create your views here.
@csrf_exempt
def index(request):
    news = News.objects.filter(newType = 1).all()[0:5]
    eduction = News.objects.filter(newType=2).all()[0:5]
    activities = News.objects.filter(newType = 3).all()[0:5]
    coffe_blog = News.objects.filter(newType=4).all()[0:5]
    eductionlist = listHelper_small(eduction)
    newslist = listHelper_big(news)
    activitieslist = listHelper_big(activities)
    coffe_bloglist = listHelper_small(coffe_blog)

    context = {"newslist": newslist, "eductionlist": eductionlist, "activitieslist":activitieslist,"coffe_bloglist":coffe_bloglist}
    return render(request,'Home.html',context=context)

@csrf_exempt
def to_login(request):
    return render(request, 'login.html')

@csrf_exempt
def to_register(request):
    return render(request, 'register.html')

@csrf_exempt
def Login(request):
    msg = ''
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = authenticate(request,email=email,password =pwd)
        if user:
             if user.is_authenticate == True:
                login(request,user)
                return redirect('index')
             else:
                msg = "请登录邮箱验证该用户"
        else:
            msg = "用户名或密码错误"
    return render(request,'login.html',{'msg':msg})
    
def active_user(request):
    token = request.GET.get('token')
    try:
        username = Token(django_settings.SECRET_KEY).confirm_validate_token(token)
    except:
        # = models.Token(django_settings.SECRET_KEY).remove_validate_token(token)
        #users = models.User.objects.filter(username=username)
        #for user in users:
        #user.delete()
        return render(request, 'register.html', {'msg': u'对不起，验证链接已经过期，请重新注册'})
    try:
        user = User.objects.get(username=username)
    except user:
        return render(request, 'register.html', {'msg': u"对不起，您所验证的用户不存在，请重新注册"})
    user.is_authenticate = True
    user.save()
    message = u'验证成功，请进行登录操作'
    admin = User.objects.filter(username="admin").first()
    Chat.objects.create(content="欢迎来到coffee！", user=admin, toUser=user)
    return render(request, 'login.html', {'msg':message})

@csrf_exempt
def register(request):
    msg=''
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        user1 = User.objects.filter(email = email)
        user2 = User.objects.filter(username = username)
        if user1:
            msg = "邮箱已被注册"
        elif user2:
            msg = "用户名已存在"
        else:
            if pwd1 == pwd2:
                User.objects.create_user(username=username,email=email,password=pwd1)
                token = Token(django_settings.SECRET_KEY).generate_validate_token(username)
                message = "\n".join([u'{0},欢迎加入咖啡馆'.format(username), u'请访问该链接，完成用户验证:','/'.join(['http://127.0.0.1:8000/blog/activateLogin', '?token='+token])])
                send_mail(u'注册用户验证信息', message, 'sduwh_zlp@163.com', [email], fail_silently=False)
                msg = "请登录到注册邮箱中验证用户，有效期为1个小时"
            else:
                msg = "两次密码不相同"
    return render(request,'register.html',{'msg':msg})



@csrf_exempt
def Logout(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def news(request):
    if request.method == "GET":
        #当前页
        current_page = request.GET.get('p',1)
        current_page = int(current_page)

        #所有数据的个数
        total_num = News.objects.filter(newType=1).all().count()
        obj = PageHalper(total_count=total_num,current_page=current_page,base_url='/blog/news',per_page=5)

        pager = obj.pager_str()

        cls_list = News.objects.filter(newType=1).all().order_by("-ctime")[obj.db_start:obj.db_end]

        return render(request,'Hots.html',{'cls_list': cls_list, 'str_pager': pager})

@csrf_exempt
def learn(request):
    if request.method == "GET":
        #当前页
        current_page = request.GET.get('p',1)
        current_page = int(current_page)

        #所有数据的个数
        total_num = News.objects.filter(newType=2).all().count()
        obj = PageHalper(total_count=total_num,current_page=current_page,base_url='/blog/news',per_page=5)

        pager = obj.pager_str()

        cls_list = News.objects.filter(newType=2).all().order_by("-ctime")[obj.db_start:obj.db_end]
        return render(request, 'Education.html',{'cls_list':cls_list,'str_pager':pager})

@login_required
@csrf_exempt
def cafe(request):
    if request.method == "GET":
        user_id = request.user.id
        #当前页
        current_page = request.GET.get('p',1)
        current_page = int(current_page)

        #所有数据的个数
        total_num = News.objects.filter(user_id = user_id).count()
        obj = PageHalper(total_count=total_num,current_page=current_page,base_url='/blog/cafe',per_page=5)

        pager = obj.pager_str()

        cls_list = News.objects.filter(user_id = user_id,newType=3).all().order_by("-ctime")[obj.db_start:obj.db_end]
        return render(request, 'Cafe.html',{'cls_list':cls_list,'str_pager':pager})

@csrf_exempt
def about_us(request):
   return render(request, 'Aboutus.html')

@login_required
@csrf_exempt
def user_index(request):
    if request.method == "GET":
        user = request.user
        news = News.objects.filter(user=user).all()
        # myfans_ids = Fans.objects.only("fans_uid").filter(uid=user.id).all()
        myfans_ids = Fans.objects.values_list('fans_uid').filter(uid=user.id)
        myfans = User.objects.filter(id__in=myfans_ids).all()
        myfollower_ids = Follower.objects.values_list("follower_uid").filter(uid=user.id)
        myfollowers = User.objects.filter(id__in=myfollower_ids).all()
        admin = User.objects.filter(username="admin").first()
        myMsg = Chat.objects.filter(toUser=user,isRead=False).all().order_by("-id").all()
        countSys = Chat.objects.filter(user=admin,toUser=user,isRead=False).all().count()
        countAll = Chat.objects.filter(toUser=user,isRead=False).all().count()
        countPer = countAll - countSys
        if len(myMsg)>0:
            lastMsgId = myMsg[0].id
        else:
            lastMsgId = None
        teams = Team.objects.all().order_by('-ctime')
        collects = News.objects.filter(collect=user)
        context = {"news": news, "myfans": myfans, "myfollowers": myfollowers, "mycollect":collects,"myMsg":myMsg,"lastMsgId":lastMsgId, "teams":teams, 'countAll':countAll, 'countSys':countSys, 'countPer':countPer}
        return render(request, 'MyIndex.html',context=context)


@login_required
@csrf_exempt
def upload_avatar(request):
    if request.method == "POST":
        avatar = request.POST['img']
        data = avatar[23:]
        data = base64.b64decode(data)
        img_name = "avatar_user_"+str(request.user.id)+".jpg"
        path = os.path.join('static','upload',img_name)
        f = open(path,'wb')
        f.write(data)
        f.close()
        user = request.user
        user.user_img = path
        user.save()
        return HttpResponse("ok")
    return render(request,'EditMyInfo.html')



@login_required
@csrf_exempt
def edit(request):
    if request.method == "POST":
        title = request.POST.get('article_article')
        content = request.POST.get('content')
        summary = request.POST.get('article_summary')
        new_type = request.POST.get('new_type')
        new_tags = request.POST.get('new_tags')
        cc = News.objects.create(title=title, summary=summary,content = content ,url="null", user=request.user, newType=new_type)
        tag_item = []
        tag_item = new_tags.split(',')
        tag_item = tag_item[0:3]
        print(tag_item)
        for i in tag_item:
            had_tag = 0
            for j in Tags.objects.all():
                if i == j.tname:
                    tnew = j
                    had_tag = 1
                    break
            if had_tag == 0:
                tnew = Tags.objects.create(tname=i)     
            cc.tags.add(tnew)
            cc.save()
        return redirect('/blog/article_detial/?id=%d'%cc.id)
    else:
        return render(request,'edit.html')

@csrf_exempt
def uploadimg(request):
    if request.method == 'POST':
        file_obj = open("log.txt","w+")
        buf = request.FILES.get('imgFile', None)
        file_buff = buf.read()
        time_format=str(time.strftime("%Y-%m-%d-%H%M%S",time.localtime()))
        try:
            file_name = "img_"+time_format+".jpg"
            save_file("static/upload", file_name, file_buff)
            dict_tmp = {}
            dict_tmp["error"] = 0
            dict_tmp["url"] = "/static/upload/"+file_name
            return HttpResponse(json.dumps(dict_tmp))
        except (Exception):
            dict_tmp = {}
            dict_tmp["error"] = 1
            return HttpResponse(json.dumps(dict_tmp))

@csrf_exempt
def artice_detial(request):
    #点赞 and 收藏
    favor = 0
    collect = 0
    id = request.GET.get('id',1)

    article = News.objects.filter(id=id).first()
    article.views_count += 1
    article.save()
    is_user_f = article.favor.filter(id=request.user.id)
    is_user_c = article.collect.filter(id=request.user.id)
    if is_user_f:
        favor = 1
    if is_user_c:
        collect = 1

    comment = Comment.objects.filter(news=article).order_by("-ctime")
    comment = comment_list_helper(comment,request.user.id)

    context={'article':article,"favor":favor,"collect":collect,"comment":comment}
    return render(request,'article_detial.html',context=context)

@login_required
@csrf_exempt
def edit_my_info(request):
    if request.method == "POST":
        username = request.POST.get('nickname')

        profile = request.POST.get('profile')
        sex = request.POST.get('sex')
        data_of_birth = request.POST.get('birthday')
        occupation = request.POST.get('occupation')
        user = request.user
        if username is not "":
            user.username = username
        if profile is not "":
            user.profile = profile
        if sex is not "":
            user.sex = sex
        if data_of_birth is not "":
            user.date_of_birth = data_of_birth
        if occupation is not "":
            user.occupation = occupation
        user.save()
        return render(request,'MyIndex.html')
    return render(request, 'EditMyInfo.html')

@login_required
@csrf_exempt
def favorChange(request):
    if request.method == "POST":
        id = request.POST['id']
        id=id[3:]
        data = request.POST['data']
        article = News.objects.filter(id = id).first()
        if data == "1":
            article.favor_count += 1
            article.favor.add(request.user)
        if data == "0":
            article.favor_count -= 1
            article.favor.remove(request.user)
        article.save()
        return HttpResponse("ok")
    return HttpResponse("error")

@login_required
@csrf_exempt
def collectChange(request):
    if request.method == "POST":
        id = request.POST['id']
        id=id[3:]
        artice = News.objects.filter(id = id).first()
        data = request.POST["data"]
        if(data == "1"):
            artice.collect.add(request.user)
        if(data == "0"):
            artice.collect.remove(request.user)
        artice.save()
        return HttpResponse("ok")
    return HttpResponse("error")

@login_required
@csrf_exempt
def commentFavorChange(request):
    if request.method == "POST":
        id = request.POST["id"]
        comment = Comment.objects.filter(id = id).first()
        data = request.POST["data"]
        if data == "1":
            comment.favor_count += 1
            comment.favor.add(request.user)
        else:
            comment.favor_count -= 1
            comment.favor.remove(request.user)
        comment.save()
        return HttpResponse("ok")
    return HttpResponse("error")

@login_required
@csrf_exempt
def upComment(request):
    if request.method == "POST":
        id = request.POST['id']
        id = id[3:]
        new = News.objects.filter(id = id).first()
        new.comment_count +=1
        new.save()
        Comment.objects.create(news=new,user=request.user,content=request.POST['data'])
        return HttpResponse("ok")
    return HttpResponse("error")

@login_required
@csrf_exempt
def upCommentReply(request):
    if request.method == "POST":
        id = request.POST["id"]
        id = id[3:]
        coment_id = request.POST['comment_id']
        new = News.objects.filter(id = id).first()
        new.comment_count += 1
        new.save()
        coment = Comment.objects.filter(id=coment_id).first()

        if(coment.parent_comment):
            Comment.objects.create(news=new,user=request.user,content=request.POST['data'],parent_comment=coment.parent_comment)
        else:
            Comment.objects.create(news=new,user=request.user,content=request.POST['data'],parent_comment=coment)
        return HttpResponse("ok")
    return HttpResponse("error")
@login_required
@csrf_exempt
def OtherIndex(request):
    id = request.GET.get('id')
    user = User.objects.filter(id=id).first()
    news = News.objects.filter(user=user).all()
    follow = Follower.objects.filter(uid=request.user.id,follower_uid=id)
    is_follow = 0
    if follow:
        is_follow = 1
    context = {"user": user, "news": news, "is_follow": is_follow}
    return render(request, 'OthersIndex.html', context=context)

@login_required
@csrf_exempt
def changeFocus(request):
    if request.method == "GET":
        touid = request.GET.get("id")
        data = request.GET.get("data")
        uid = request.user.id
        follow = Follower.objects.filter(uid=uid,follower_uid=touid).first()
        fans = Fans.objects.filter(uid = touid,fans_uid=uid).first()
        if data == "1":
            if not follow:
                Follower.objects.create(uid=uid,follower_uid=touid)
            if not fans:
                Fans.objects.create(uid=touid,fans_uid=uid)
        else:
            if follow:
                Follower.objects.filter(uid=uid, follower_uid=touid).delete()
            if fans:
                Fans.objects.filter(uid=touid,fans_uid=uid).delete()
        return redirect('/blog/otherIndex/?id=%s' % touid)
    return HttpResponse("error")

@csrf_exempt
def search(request):
    users = []
    news = []
    data = request.GET.get("search")
    if data:
        msg_status = '搜索结果'
        users = User.objects.filter(username__icontains=data).all()
        news = News.objects.filter(title__icontains=data).all()
    else:
        msg_status = '请输入搜索内容'

    context = {"msg": msg_status, "users": users, "news": news}
    return render(request, 'SearchData.html',context=context)

@login_required
@csrf_exempt
def coffeeEdit(request):
    return render(request,'coffeeEdit.html')

@login_required
@csrf_exempt
def getUser(request):
    if request.method=="GET":
        user = request.user
        toUsers = User.objects.filter(id=user.id).all()[:]
        jsonUsers = serializers.serialize("json",toUsers)[1:-1]

        return HttpResponse(jsonUsers)
    return HttpResponse("error")

@login_required
@csrf_exempt
def activities(request):
    msg=''
    team_state = 0
    if request.method == "POST":
        user = request.user.id
        t_id = request.POST.get('team_id')
        join = Team.objects.filter(id=t_id).first()
        if join.nownum < join.maxnum:
                for i in join.teammate.all():
                    if i.id == user:
                        team_state = 1
                if team_state == 0:
                    join.teammate.add(User.objects.filter(id=user).first())
                    join.nownum = join.nownum + 1
                    join.save()
                else:
                    msg='您已经在该队伍中了~'
        else:
            msg='队伍人数已满！'
    teams = Team.objects.all().order_by("-ctime")
    
    context = {"teams": teams, "msg": msg}
    return render(request, 'Match.html',context = context)


@login_required
@csrf_exempt
def createteam(request):
    msg = ""
    if request.method == "POST":
        name = request.POST.get('team_name')
        detail = request.POST.get('team_detail')
        maxnum = request.POST.get('team_num')
        team_ex = Team.objects.filter(name = name,captain=request.user)
        if team_ex:
            msg = "*您已经创建过同名队伍啦~"
        else:
            Team.objects.create(name=name, detail=detail, captain=request.user, maxnum=maxnum ,nownum=1)
            ct = Team.objects.filter(name=name).first()
            ct.teammate.add(request.user)
            ct.save()
            return redirect('/blog/activities')
    return render(request,'createteam.html',{'msg': msg})
    
@csrf_exempt
def forget(request):
    msg = ""
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        user1 = User.objects.get(email=email)
        user2 = User.objects.get(username=username)
        if user1 and user2:
            if(user1.email == user2.email and user1.username == user2.username):
                code = random_codeStr()
                user1.re_code = code;
                user1.is_used = False;
                user1.re_data = datetime.now() + timedelta(3)
                user1.save()
                message = "\n".join([u'{0},咖啡馆账号重置密码'.format(username), u'请访问该链接，重置密码:',
                                     '/'.join(['http://127.0.0.1:8000/blog/reset', '?code=' + code])])
                send_mail(u'注册用户验证信息', message, 'sduwh_zlp@163.com', [email], fail_silently=False)
                msg = "已发送验证邮件"
            else:
                msg = "邮箱和用户名不匹配"
        elif user1 or user2:
            msg = "邮箱和用户名不匹配"
        else:
            msg = "邮箱并未注册"
    return render(request, 'forgetpassword.html', {'msg': msg})

@csrf_exempt
def reset(request):
    msg = ""
    code = request.GET.get('code')
    if request.method == "POST":
        code = request.POST.get('code')
        try:
            user = User.objects.get(re_code=code)
            new_password = request.POST.get('pass')
            if user:
                if(user.is_used == False):
                    now_time = datetime.now()
                    now_time = now_time.strftime('%Y%m%d %H%M%S')
                    gq_time = user.re_data.strftime('%Y%m%d %H%M%S')
                    if now_time <= gq_time:
                        user.is_used = True;
                        user.re_code = ""
                        user.re_data = datetime.now()
                        user.set_password(new_password)
                        user.save();
                        msg = "修改成功"
                        return render(request, 'resetpasswordsucess.html', {'msg': msg})
                    else:
                        msg = "链接已失效，请重新申请！"
                else:
                    msg = "链接已被使用，请重新申请！"
        except:
            msg = "该链接未被申请！"
            return render(request, 'resetpassword.html', {'msg': msg})
    return render(request, 'resetpassword.html', {'msg': msg,'code':code})

@login_required
@csrf_exempt
def teamzone(request):
    if request.method == "GET":
        team_id = request.GET.get('id',1)
        this_team = Team.objects.filter(id = team_id).first()
        if request.user in this_team.teammate.all():
            td = Team_dialogue.objects.filter(relate_team = this_team).all().order_by("-ctime")
            context = {'this_team': this_team, 'td': td}
            return render(request, 'TeamZone.html',context = context)
    elif request.method == "POST":
            team_id = request.POST.get('team_id')
            new_talk = request.POST.get('new_talk')
            new_num = request.POST.get('new_num')
            print(new_num)
            new_cap = request.POST.get('new_cap')
            new_captain = User.objects.filter(id = new_cap).first()
            print(new_cap)
            this_team = Team.objects.filter(id = team_id).first()
            if new_talk:
                this_team.captain_talk = new_talk
            this_team.maxnum = new_num
            if new_cap:
                this_team.captain = new_captain
            this_team.save()
            if request.user in this_team.teammate.all():
                td = Team_dialogue.objects.filter(relate_team = this_team).all().order_by("-ctime")
                context = {'this_team': this_team, 'td': td}
                return render(request, 'TeamZone.html',context = context)
    return render(request, 'home.html')

@login_required
@csrf_exempt
def dialogue(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        dialogue_content = request.POST.get('dialogue_content')
        this_team = Team.objects.filter(id = team_id).first()
        dc = Team_dialogue.objects.create(relate_team = this_team,content = dialogue_content,user = request.user)
        td = Team_dialogue.objects.filter(relate_team = this_team).all()
        id = this_team.id
        return redirect('/blog/teamzone/?id=%d' % id)