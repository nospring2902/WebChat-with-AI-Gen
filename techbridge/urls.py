from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.prebase, name='prebase'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
]