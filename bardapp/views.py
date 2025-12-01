from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

def index(request):
    
    return render (request, 'bardapp/index.html')
    

def members(request):
    
    return render (request, 'bardapp/members.html')
    


def events(request):
    
    return render (request, 'bardapp/events.html')