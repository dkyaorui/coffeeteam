from django.conf.urls import url
from Chat import views

urlpatterns = [
    url(r'^dealChat/$',views.dealChat,name="dealChat"),
]