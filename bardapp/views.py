from django.shortcuts import render


# Create your views here.

posts =[
    {
        'author': 'Blaise Hala',
        'title': 'Blog Post',
        'content':'FirstPosted',
        'dateposted': 'August 27,2018'

    },


     {
        'author': 'Blaise Hala',
        'title': 'Blog Post',
        'content':'FirstPosted',
        'dateposted': 'August 27,2018'

    },


     {
        'author': 'Blaise Hala',
        'title': 'Blog Post',
        'content':'FirstPosted',
        'dateposted': 'August 27,2018'

    }

]




def index(request):
    
    return render (request, 'bardapp/index.html')
    

def members(request):
    context = {
             'posts': posts 
        }
    
    return render(request, 'bardapp/members.html', context)
    


def events(request):
    
    return render (request, 'bardapp/events.html',{'title':'events'})