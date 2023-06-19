from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.db.models import Q


def index(request):
    if request.user.is_authenticated:
        user = request.user
        blog_posts = BlogPost.objects.filter(Q(author=user, privacy='private') | Q(
            privacy='public')).order_by('-publication_date')
        return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts})
    else:
        return redirect('blog:login')


def user_logout(request):
    logout(request)
    return redirect('blog:index')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/blog")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/blog/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def blog_list(request):
    blog_posts = BlogPost.objects.filter(
        privacy='public').order_by('-publication_date')
    return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts})


def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog_post': blog_post})


@login_required
def blog_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        privacy = request.POST['privacy']

        author = request.user
        BlogPost.objects.create(
            title=title, content=content, author=author, privacy=privacy)
        return redirect('/blog')
    return render(request, 'blog/blog_create.html')


def blog_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        privacy = request.POST['privacy']
        brief_text = request.POST['brief_text']
        image = request.FILES['image'] if 'image' in request.FILES else None
        author = request.user
        BlogPost.objects.create(title=title, content=content, author=author,
                                brief_text=brief_text, privacy=privacy, image=image)
        return redirect('/blog')

    return render(request, 'blog/blog_create.html')
