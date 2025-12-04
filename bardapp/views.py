from django.shortcuts import render
from .models import Poster

# Create your views here.


def index(request):
    
    return render (request, 'bardapp/index.html')
    

def members(request):
    context = {
             'posts': Poster.objects.all() 
        }
    
    return render(request, 'bardapp/members.html', context)
    


def events(request):
    
    return render (request, 'bardapp/events.html',{'title':'events'})



def memberbenefits(request):
    """Display payment instructions page"""
    return render (request, 'bardapp/memberbenefits.html')