from django.shortcuts import render
from .models import Post

# Create your views here.


def index(request):
    
    return render (request, 'bardapp/index.html')
    

def members(request):
    context = {
             'posts': Post.objects.all() 
        }
    
    return render(request, 'bardapp/members.html', context)
    


def events(request):
    
    return render (request, 'bardapp/events.html',{'title':'events'})