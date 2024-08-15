from django.contrib import messages  # メッセージフレームワークをインポート
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from .models import Group, GroupMember, GroupMessage, GroupThread, UserProfile
from .aifunction import translate,summarize_text,word_explanation
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.conf import settings
import requests


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
    
@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('dashboard')

@login_required
def chat_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Kiểm tra xem người dùng có phải là thành viên của nhóm không
    if not GroupMember.objects.filter(group=group, user=request.user).exists():
        return redirect('dashboard')  # Nếu không phải là thành viên thì chuyển về dashboard
     
    threads = GroupThread.objects.filter(group=group).select_related('first_message')

    first_message_ids = [thread.first_message.id for thread in threads if thread.first_message]
    # Fetch all messages related to the first messages of the threads
    messages = GroupMessage.objects.filter(id__in=first_message_ids).select_related('sender').order_by('timestamp')
    user_profile = UserProfile.objects.get(user=request.user)
    main_language = user_profile.main_language
    if request.method == "POST":
        message_content = request.POST.get('message_content')
        if message_content:
            # Tạo thread mới trước
            thread = GroupThread.objects.create(group=group)
            
            if main_language=='ja':
                japanese=message_content
                english=translate(message_content,language='English')
                vietnamese=translate(message_content,language='Vietnamese')
            elif main_language=='en':
                english=message_content
                japanese=translate(message_content,language='Japanese')
                vietnamese=translate(message_content,language='Vietnamese')
            else:
                vietnamese=message_content
                japanese=translate(message_content,language='Japanese')
                english=translate(message_content,language='English')
            # Tạo tin nhắn mới và gán nó vào thread vừa tạo
            first_message = GroupMessage.objects.create(
                sender=request.user,
                message_content=message_content,
                japanese=japanese,
                english=english,
                vietnamese=vietnamese,
                thread=thread  # Gán thread cho tin nhắn
            )

            # Cập nhật tin nhắn đầu tiên cho thread
            thread.first_message = first_message
            thread.save()

            # Cập nhật tin nhắn mới nhất trong group
            group.latest_message_id = first_message
            group.save()

            return redirect('chat', group_id=group.id)  # Reload trang chat

    return render(request, 'chat.html', {
        'group': group,
        'messages': messages,
        'user_id': request.user.id, 
        'main_language': main_language
    })

@login_required
def thread_view(request, thread_id):
    thread = get_object_or_404(GroupThread, id=thread_id)
    first_message = thread.first_message
    messages = GroupMessage.objects.filter(thread=thread).order_by('timestamp')
    group = thread.group
    user_profile = UserProfile.objects.get(user=request.user)
    main_language = user_profile.main_language
    if request.method == "POST":
        message_content = request.POST.get('message_content')
        if main_language=='ja':
            japanese=message_content
            english=translate(message_content,language='English')
            vietnamese=translate(message_content,language='Vietnamese')
        elif main_language=='en':
            english=message_content
            japanese=translate(message_content,language='Japanese')
            vietnamese=translate(message_content,language='Vietnamese')
        else:
            vietnamese=message_content
            japanese=translate(message_content,language='Japanese')
            english=translate(message_content,language='English')
        if message_content:
            GroupMessage.objects.create(
                sender=request.user,
                thread=thread,
                message_content=message_content,
                japanese=japanese,
                english=english,
                vietnamese=vietnamese
            )
            return redirect('thread', thread_id=thread_id)

    return render(request, 'thread.html', {
        'thread': thread,
        'first_message': first_message,
        'messages': messages,
        'group': group,
        'main_language': main_language,
        'user_id':request.user.id
    })

@login_required
@csrf_exempt
def update_summary(request, thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(GroupThread, id=thread_id)
        messages = GroupMessage.objects.filter(thread=thread).order_by('timestamp')
        all_texts = '. '.join(message.message_content for message in messages)
        
        user_profile = UserProfile.objects.get(user=request.user)
        main_language = user_profile.main_language
        if main_language=='ja':
            language='Japanese'
        elif main_language=='en':
            language='English'
        elif main_language=='vi':
            language='Vietnamese'
        summary = summarize_text(all_texts, language)
        return JsonResponse({'summary': summary})
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def explanation(request, message_id):
    message = get_object_or_404(GroupMessage, id=message_id)
    paragraph = message.message_content
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.main_language == 'en':
        language = 'English'
    elif user_profile.main_language == 'ja':
        language = 'Japanese'
    elif user_profile.main_language == 'vi':
        language = 'Vietnamese'
    explanation = word_explanation(paragraph, language)
    return JsonResponse({'explanation': explanation})