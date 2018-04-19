from django.urls import path
from django.conf.urls import url
from blog import views
urlpatterns = [
    url('to_login/',views.to_login,name='to_login'),
    url('to_register/',views.to_register,name='to_register'),
    url('login/',views.Login,name='login'),
    url('register/',views.register,name='register'),
    url('logout/',views.Logout,name='logout'),
    url('news/',views.news, name='news'),
    url('learn/',views.learn,name='learn'),
    url('activities/',views.activities,name='activities'),
    url('cafe/',views.cafe,name='cafe'),
    url('about_us/',views.about_us,name='about_us'),
    url('user/index/',views.user_index,name='user_index'),
    url('user/upload_avatar/',views.upload_avatar, name='upload_avatar'),
    url('article_detial/',views.artice_detial,name="article_detial"),
    url(r'^user/edit_my_info/', views.edit_my_info, name="edit_my_info"),
    url(r'^favorChange/',views.favorChange,name="favorup"),
    url(r'^collectChange/',views.collectChange,name="collectChange"),
    url(r'^upComment/',views.upComment,name="upComment"),
    url(r'^upCommentReply/', views.upCommentReply, name="upComment"),
    url(r'^commentFavorChange',views.commentFavorChange,name="commentFavorChange"),
    url(r'^otherIndex',views.OtherIndex,name='otherIndex'),
    url(r'^changeFocus',views.changeFocus,name='changeFocus'),
    url(r'^search/',views.search, name='search'),
    url(r'^coffeeEdit/',views.coffeeEdit,name='coffeeEdit'),
    url(r'^getUser/',views.getUser,name="getUser"),
	url(r'^forget/', views.forget, name='forget'),#忘记密码
    url(r'^reset/', views.reset, name='reset'),
    url(r'^activateLogin/',views.active_user,name='active_user'),
    url(r'^teamzone/',views.teamzone,name='teamzone'),
    url(r'^dialogue/',views.dialogue,name='dialogue'),
]
