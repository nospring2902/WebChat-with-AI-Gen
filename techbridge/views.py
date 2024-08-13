from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Group, GroupMember
from django.shortcuts import render
from django.conf import settings
import requests

def translate_text(request):
    translated_text = ""
    if request.method == "POST":
        text_to_translate = request.POST.get('text_to_translate', '')
        
        if text_to_translate:
            # Gửi yêu cầu tới Google Translate API
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'auto',  # Tự động nhận dạng ngôn ngữ
                'tl': 'vi',    # Dịch sang tiếng Anh
                'dt': 't',
                'q': text_to_translate
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                translated_text = response.json()[0][0][0]
            else:
                translated_text = "Error translating text"
    
    return render(request, 'translate.html', {'translated_text': translated_text})

def prebase(request):
    return render(request, 'prebase.html')

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Điều hướng đến dashboard
        else:
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('Valid')
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Chuyển hướng tới trang chủ hoặc trang dashboard sau khi đăng ký thành công
        else:
            print(form.errors)
    else:  
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def dashboard(request):
    user_groups = Group.objects.filter(groupmember__user=request.user)
    return render(request, 'dashboard.html', {'groups': user_groups})
@login_required
def logout(request):
    return render(request, 'prebase.html')

@login_required
def create_groupchat(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        
        # Tạo nhóm mới
        group = Group.objects.create(group_name=group_name)
        # Thêm người dùng hiện tại vào nhóm
        GroupMember.objects.create(group=group, user=request.user)
        # Lấy danh sách user_id từ form (những người dùng khác)
        user_ids = request.POST.getlist('members')
        # Thêm các thành viên còn lại vào nhóm
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            GroupMember.objects.create(group=group, user=user)
        
        return redirect('dashboard')
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'create_groupchat.html', {'users': users})