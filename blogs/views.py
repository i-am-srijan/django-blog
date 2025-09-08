from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from blogs.models import Blog,Category

# Create your views here.
def post_by_category(request, category_id):
    #fatch the post that belong to the category with the id category_id
    posts = Blog.objects.filter(status='Published', category_id=category_id)
    try:
        category = Category.objects.get(pk=category_id)
    except:
        # redirect to homepage
        return redirect('home')
    
    #if you want page not found or error use this and also you need this create html on which error code like 404.html
    #and write in html like <p>page not found </P> or you can design this page and also need to setings  on project like blog_main
    
    # category = get_object_or_404(Category, pk=category_id)
    context ={
        'posts':posts,
        'category':category,
    }

    return render(request, 'posts_by_category.html', context)