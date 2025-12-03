from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm,UserUpdateForm, AlumniProfileUpdateForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from . models import AlumniProfile, Post, Event, Comment
from django.db.models import Count, Q
from django.utils import timezone





def register(request):

    if request.user.is_authenticated:
        return redirect ('memeber_dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form.request = request  # Pass request to form for rate limiting
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'please correct the errors below')
                             
    else:
        form = UserRegisterForm()
    return render (request, 'users/register.html', {'form':form})





def user_login_view(request):

    if request.user.is_authenticated:
        return redirect ('memeber_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('member_dashboard')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


@login_required
def user_logout_view(request):
    """Handle user logout with confirmation"""
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
        return redirect('index')
    
    # Show confirmation page for GET requests
    return render(request, 'users/logout.html')




def payment_instructions(request):
    """Display payment instructions page"""
    return render (request, 'users/payment_instructions.html')




@login_required
def member_dashboard(request):
    """Main member platform dashboard"""
    
    # Get or create user profile
    profile, created = AlumniProfile.objects.get_or_create(user=request.user)
    
    # Get recent posts for feed
    posts = Post.objects.all().select_related('author', 'author__alumniprofile').prefetch_related('likes', 'comments')[:20]
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    
    # Get statistics
    total_alumni = AlumniProfile.objects.count()
    total_events = Event.objects.count()
    user_connections = 0  # You can implement connections later
    
    # Recent activity
    recent_jobs = Post.objects.filter(post_type='job').order_by('-created_at')[:3]
    
    context = {
        'profile': profile,
        'posts': posts,
        'upcoming_events': upcoming_events,
        'total_alumni': total_alumni,
        'total_events': total_events,
        'user_connections': user_connections,
        'recent_jobs': recent_jobs,
    }
    
    return render(request, 'users/dashboard.html', context)


@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'update')
        
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content,
                post_type=post_type
            )
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Post content cannot be empty.')
    
    return redirect('member_dashboard')


@login_required
def like_post(request, post_id):
    """Like/unlike a post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return redirect('member_dashboard')


@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('comment')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment added!')
    
    return redirect('member_dashboard')


@login_required
def alumni_directory(request):
    """Browse alumni directory"""
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    
    alumni = AlumniProfile.objects.select_related('user').all()
    
    if search_query:
        alumni = alumni.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(current_company__icontains=search_query)
        )
    
    if year_filter:
        alumni = alumni.filter(year_graduated=year_filter)
    
    context = {
        'alumni': alumni,
        'search_query': search_query,
        'year_filter': year_filter,
    }
    
    return render(request, 'users/directory.html', context)


@login_required
def event_list(request):
    """List all upcoming events"""
    upcoming = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    past = Event.objects.filter(date__lt=timezone.now()).order_by('-date')[:10]
    
    context = {
        'upcoming_events': upcoming,
        'past_events': past,
    }
    
    return render(request, 'users/events.html', context)


@login_required
def rsvp_event(request, event_id):
    """RSVP to an event"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
        messages.success(request, f'You have cancelled your RSVP for {event.title}')
    else:
        if not event.is_full():
            event.attendees.add(request.user)
            messages.success(request, f'You have RSVP\'d for {event.title}!')
        else:
            messages.error(request, 'This event is full.')
    
    return redirect('event_list')

@login_required
def profile_edit(request):
    """Edit user profile"""
    
    # Get or create profile
    profile, created = AlumniProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = AlumniProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = AlumniProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    
    return render(request, 'users/profile_edit.html', context)


@login_required
def profile_view(request, username):
    """View a user's profile"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(AlumniProfile, user=user)
    
    # Get user's recent posts
    recent_posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Get user's upcoming events
    upcoming_events = Event.objects.filter(attendees=user, date__gte=timezone.now()).order_by('date')[:3]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'recent_posts': recent_posts,
        'upcoming_events': upcoming_events,
        'is_own_profile': request.user == user,
    }
    
    return render(request, 'users/profile_view.html', context)



# username = form.cleaned_data.get('username')