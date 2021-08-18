import random

from django.conf import settings

from .models import Tweets,Profile
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.utils.http import is_safe_url
from .forms import TweetForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
# Create your views here.
from django.contrib.auth.models import User
ALLOWED_HOSTS = settings.ALLOWED_HOSTS



def home_view(request,*args,**kwargs):
    # print(request.user)
    try:
        pro_obj = Profile.objects.filter(user__username=request.user)
        allUsers = User.objects.all()
        if pro_obj.count() == 0:
            pro_obj = Profile()
            pro_obj.user =  User.objects.filter(username=request.user)[0]
            pro_obj.save()
            context = {
        "allUsers" : allUsers,
        "allFollower" :pro_obj.follower.all()
        }
        else:
            follower_list = []
            for name in allUsers:
                if name not in pro_obj[0].follower.all():
                    follower_list.append(name)
            context = {
            "allUsers" : follower_list,
            "allFollower" :pro_obj[0].follower.all()
            }
    except:
        context = {}
        pass

    
    return render(request,"home.html",context,status=200)

def tweet_create(request,*args,**kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if next_url != None and is_safe_url(next_url,allowed_hosts=ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request,"components/form.html",context={"form":form})

def tweet_list_view(request,*args,**kwargs):
    
    if (request.user.is_authenticated):
        querySet = Tweets.objects.filter(user = request.user)
        tweets_list = [{"id":x.id,"content":x.content,"likes":random.randint(0,17)} for x in querySet]
        data = {
            "response":tweets_list
        }
        return JsonResponse(data)
    else:
        return redirect("/")

def tweet_detail_view(request,tweet_id,*args,**kwargs):
    data = {
    }
    status = 200
    try:
        obj = Tweets.objects.filter(id = tweet_id)
        
        data = obj.values()[0]
        print(data)
    except:
        data['Messsage'] = "Not Found!!"
        status = 404
    return JsonResponse(data,status=status)


def login_view(request):
    form =  AuthenticationForm(request,data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request,user_)
        return redirect("/")
    context = {"form":form}
    return render(request,"components/auth/login.html",context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
    context = {
        "form":None
    }
    return render(request,"components/auth/logout.html",context)


def registration_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        login(request,user)
        return redirect("/")
    context = {"form":form }
    return render(request,"components/auth/registration.html",context)

def follow_button(request,follow_user,*args,**kwargs):
    curr_user = request.user
    obj_curr_user = User.objects.filter(username=curr_user)
    
    obj_follow_user = User.objects.filter(username=follow_user)
    
    pro_obj = Profile.objects.filter(user__username=curr_user)
    
    
    # print(pro_obj_curr[0].follower.all())
    # #print(obj_curr_user[0],obj_follow_user[0],pro_obj.count())
    if (pro_obj.count() == 0):
        pro_obj = Profile()
        pro_obj.user = obj_curr_user[0]
        #print(pro_obj.user)
        pro_obj[0].save()
    
    pro_obj[0].follower.add(obj_follow_user[0])
    print(pro_obj[0].follower.all())
    pro_obj[0].save()
    
    return JsonResponse({"data":"success"})
    
def follow_tweet_view(request):
    data = {}
    if (request.user.is_authenticated):
        profile = Profile.objects.filter(user__username=request.user)
        if(profile.count() != 0):
            follower = profile[0].follower.all()
            print(follower)
            if(len(follower) != 0):
                data= {}
                data["response"] = []
                for follow in follower:
                    #print(follow)
                    new_data = {}
                    if follow != request.user:
                        querySet = Tweets.objects.filter(user = follow)
                        tweets_list = [{"id":x.id,"content":x.content,"likes":random.randint(0,17)} for x in querySet]
                        new_data["response"]  = tweets_list
                        for keys,values in new_data.items():
                            for value in values:
                                data[keys].append(value)
            #print(data)
    
    return JsonResponse(data)