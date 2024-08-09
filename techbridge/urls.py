from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    #第一引数はurlの後に付くもの、第2引数はviews.pyの中のprebaseという関数を実行、第３引数はこのpath自体の名前
    path('', views.prebase, name='prebase'),

    path('signin/', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]