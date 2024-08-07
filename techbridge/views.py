from django.shortcuts import render

def prebase(request):
    return render(request, 'prebase.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')