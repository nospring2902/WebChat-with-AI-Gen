from django.shortcuts import render

def prebase(request):
    return render(request, 'prebase.html')