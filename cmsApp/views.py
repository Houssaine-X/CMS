from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Post
from .forms import PostForm
from django.http import JsonResponse, HttpResponseForbidden
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeview(request):
    if request.user.is_authenticated:  # Check if user is logged in
        posts = Post.objects.filter(author=request.user)  # Filter posts by author
    else:
        return HttpResponseForbidden()
    context = {'posts': posts}
    return render(request, 'home.html', context)


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = '/posts/'
    # Redirect URL on successful creation


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Pre-populate with existing data
        if form.is_valid():
            post = form.save()
            print('Post updated successfully')
    else:
        form = PostForm(instance=post)  # Create form with existing data
    return render(request, 'home.html', {'form': form})


def delete_post(request, pk):
    if request.method == 'DELETE':
        post = Post.objects.filter(pk=pk).first()
        if post:
            post.delete()
            print('Post deleted successfully')
            return JsonResponse({'message': 'Post deleted successfully'})

        else:
            return JsonResponse({'error': 'Post not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def loginp(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@never_cache
def logout_view(request):
    logout(request)
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return HttpResponseForbidden()  # Deny access with a 403 Forbidden response


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request, 'index.html', context)
