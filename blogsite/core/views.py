from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileForm, BlogPostForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import BlogPost
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


# Create your views here.


def home_view(request):
     return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, request.FILES)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)  # auto login
            return redirect('main')  # replace 'home' with your homepage URL name
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    
    return render(request, 'core/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('main')  # redirect to main or profile page after update
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/profile.html', context)


@login_required
def main_view(request):
    user = request.user
    query = request.GET.get('q', '')

    # Get the full queryset first, then filter it if query exists
    posts_qs = BlogPost.objects.all().order_by('-created_at')
    if query:
        posts_qs = posts_qs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Then paginate the filtered queryset
    paginator = Paginator(posts_qs, 3)  # 3 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)  # This is a Page object, no filtering here!

    profile_pic_url = None
    if hasattr(user, 'profile') and user.profile.profile_pic:
        profile_pic_url = user.profile.profile_pic.url

    form = BlogPostForm()

    return render(request, 'core/main.html', {
        'user': user,
        'form': form,
        'posts': posts_page,
        'profile_pic_url': profile_pic_url,
        'search_query': query,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('view_posts')
    else:
        form = BlogPostForm()
    return render(request, 'core/create_post.html', {'form': form})

def view_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/view_posts.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'core/post_detail.html', {'post': post})

@login_required
def main_view(request):
    user = request.user
    query = request.GET.get('q', '')

    # Start with the full queryset
    posts_list = BlogPost.objects.all().order_by('-created_at')

    # Apply search filter BEFORE pagination
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Paginate the filtered queryset
    paginator = Paginator(posts_list, 3)  # Show 3 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  # Safe paginated page object

    profile_pic_url = None
    if hasattr(user, 'profile') and user.profile.profile_pic:
        profile_pic_url = user.profile.profile_pic.url

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = user
            blog.save()
            return redirect('main')
    else:
        form = BlogPostForm()

    return render(request, 'core/main.html', {
        'user': user,
        'form': form,
        'posts': posts,
        'profile_pic_url': profile_pic_url,
        'search_query': query,
    })


@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'core/edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('main')
    
    return render(request, 'core/delete_post_confirm.html', {'post': post})