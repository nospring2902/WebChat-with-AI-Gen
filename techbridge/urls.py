from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),

    #第一引数はurlの後に付くもの、第2引数はviews.pyの中のprebaseという関数を実行、第３引数はこのpath自体の名前
    path('', views.prebase, name='prebase'),

    path('signin/', views.signin, name='signin'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('signup/', views.signup, name='signup'),
    
    path('logout/', LogoutView.as_view(next_page='prebase'), name='logout'),
    
    path('create_groupchat/', views.create_groupchat, name='create_groupchat'),

    path('delete_group<int:group_id>/', views.delete_group, name='delete_group'),
    
    path('chat/<int:group_id>/', views.chat_view, name='chat'),

    path('thread/<int:thread_id>/', views.thread_view, name='thread'), 
    path('update_summary/<int:thread_id>/', views.update_summary, name='update_summary'),
    path('explanation/<int:message_id>/', views.explanation, name='explanation'),
    # path('translate/', views.translate_text, name='translate_text'),
]