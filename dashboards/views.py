from django.shortcuts import render, redirect
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogPostForm, EditUserForm

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User
from .forms import AddUserForm
# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context={
        'category_count': category_count,
        'blog_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context) 

def categories(request):
    return render(request, 'dashboard/categories.html')

def add_category(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()
    context={
        'form': form,
    }
    return render(request, 'dashboard/add_category.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
        
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts': posts,
    }
    return render(request,'dashboard/posts.html', context)

# def add_post(request):
#      if request.method =='POST':
#          form = BlogPostForm(request.POST, request.FILES)
#          if form.is_valid():
#              post = form.save(commit=False) # temporarily saving the form
#              post.author = request.user
#              post.save()
#              title = form.cleaned_data['title']
#              post.slug = slugify(title) + '-' + str(post.id)
#              post.save()
#              return redirect('posts')
#          else:
#               print(form.error)
#      form = BlogPostForm()
#      context = {
#          'form': form,
#      }
#      return render(request, 'dashboard/add_post.html', context)


def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Generate base slug from title
            title = form.cleaned_data['title']
            base_slug = slugify(title)
            unique_slug = base_slug
            counter = 1

            # Loop to ensure slug uniqueness
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            post.slug = unique_slug
            post.save()

            return redirect('posts')
        else:
            print(form.errors)  # ✅ fixed typo here
    else:
        form = BlogPostForm()

    context = {'form': form}
    return render(request, 'dashboard/add_post.html', context)


def edit_post(request,pk):
    post = get_object_or_404(Blog, pk=pk)
    form = BlogPostForm(instance=post)
    if request.method =='POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context ={
        'form':form,
        'post':post,
    }
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')

def users(request):
    users = User.objects.all()
    context ={
        'users': users,
    }
    return render(request, 'dashboard/users.html', context)


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    form = AddUserForm()
    context={
        'form':form,
    }
    return render(request, 'dashboard/add_user.html', context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method =="POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    context={
        'form': form,
    }
    return render(request, 'dashboard/edit_user.html', context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')