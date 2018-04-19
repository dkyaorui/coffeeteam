from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
import os
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.conf import settings as django_settings
import re

class MyUserManager(BaseUserManager):
    def create_user(self, email,username,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(editable=True,null=True)
    user_img = models.CharField(max_length=128,null=False,default=os.path.join("static","upload","1.jpg"))
    username = models.CharField(default="",max_length=125,unique=True)
    profile = models.CharField(default="这个人很神秘",max_length=500)
    sex = models.CharField(max_length=2,default="未知")
    occupation = models.CharField(max_length=20,default="007？")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_authenticate = models.BooleanField(default = False)
    re_code = models.CharField(max_length=20,null = True)
    is_used = models.BooleanField(default=True)
    re_data = models.DateField(null = True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=10,default="",unique=True)
	

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,default="",unique=False)
    summary = models.CharField(max_length=128,null=True)
    content = models.CharField(max_length=10000,null=True)
    url = models.CharField(max_length=128,default="")
    ctime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='id',related_name='new',on_delete=models.CASCADE)
    new_type_choices = [
        (1,"热点动态"),
        (2,"创新教育"),
        (3,"咖啡馆"),
    ]
    newType = models.IntegerField(choices=new_type_choices)
    favor_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    favor = models.ManyToManyField(to="User",related_name="fnew")
    collect = models.ManyToManyField(to="User",related_name="cnew")
    tags = models.ManyToManyField(to="Tags",related_name="ts")

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    news = models.ForeignKey(to="News",to_field="id",on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field="id",on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    device = models.CharField(max_length=16,null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(to='self',null=True,related_name='pc',on_delete=models.CASCADE)
    favor_count = models.IntegerField(default=0)
    favor = models.ManyToManyField(to="User",related_name="fc")

class Fans(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(null=False)
    fans_uid = models.IntegerField(null=False)

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(null=False)
    follower_uid = models.IntegerField(null=False)

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=125,unique=False)
    ctime = models.DateTimeField(auto_now_add=True)
    detail = models.CharField(default="",max_length=200)
    maxnum = models.IntegerField(null=False)
    nownum = models.IntegerField(null=False)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='id',on_delete=models.CASCADE)
    captain_talk = models.CharField(max_length=200,default="无")
    teammate = models.ManyToManyField(to="User",related_name="tm")

class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(security_key.encode(encoding='utf-8'))
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token,salt=self.salt,max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)

class Modify_pwdForm(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(null=False,max_length=50)
    r_password = models.CharField(null=False,max_length=50)

class Team_dialogue(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    ctime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='User',on_delete=models.CASCADE)
    relate_team = models.ForeignKey(to='Team',on_delete=models.CASCADE)