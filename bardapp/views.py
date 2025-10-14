from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Member, Event, NewsArticle, Donation, Newsletter, Gallery

def home(request):
    """Homepage View"""
    # Get featured news articles (latest 3)
    news_articles = NewsArticle.objects.filter(is_published=True)[:3]
    
    # Get upcoming events (latest 3)
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now(),
        is_active=True
    ).order_by('date')[:3]
    
    # Get statistics
    stats = {
        'total_members': Member.objects.filter(is_active_member=True).count(),
        'total_events': Event.objects.filter(date__gte=timezone.now()).count(),
        'countries': Member.objects.values('country').distinct().count(),
        'total_donations': Donation.objects.filter(is_verified=True).aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }
    
    # Get gallery images for carousel
    gallery_images = Gallery.objects.all()[:3]
    
    context = {
        'news_articles': news_articles,
        'upcoming_events': upcoming_events,
        'stats': stats,
        'gallery_images': gallery_images,
    }
    return render(request, 'bardapp/home.html', context)