"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from myapp.views import (home_view,
                        tweet_detail_view,
                        tweet_list_view,
                        tweet_create,
                        login_view,
                        logout_view,
                        registration_view,
                        follow_tweet_view,
                        follow_button)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name = 'home'),
    path('tweets/',tweet_list_view),
    path('tweets/<int:tweet_id>',tweet_detail_view),
    path('create-tweet/',tweet_create,name="tweet_create"),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name="logout"),
    path('registration/',registration_view,name='registration'),
    path('follow/',follow_tweet_view,name="follow"),
    path('follow_button/<str:follow_user>',follow_button,name='follow_button')
]
