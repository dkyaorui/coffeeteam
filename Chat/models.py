from django.db import models
from blog.models import User
from django.conf import settings

# Create your models here.

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=256, null=False)
    ctime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="uchat", on_delete=models.CASCADE)
    toUser = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="rechat",on_delete=models.CASCADE)
    isRead = models.BooleanField(default=False)
    