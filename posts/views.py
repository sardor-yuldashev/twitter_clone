from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Post
from .models import User_data
from .forms import PostsForm
import random, string

def posts(request):
    # result
    template = 'posts.html'
    posts = Post.objects.all().order_by('-date')[:20]
    context = {'posts': posts, 'user_likes': [],}
    page = render(request, template, context)
    # if user is new, generate user_id and set cookie
    if request.COOKIES.get("user_id", None) == None:
        letters = string.ascii_lowercase
        user_id = ''.join(random.choice(letters) for i in range(20)) # 20 max length
        page.set_cookie("user_id", user_id)
        # user_data = User_data(user_id=user_id) # first time user no need
    else:
    # else, query likes data and pass in context
        user_id = request.COOKIES["user_id"]
        user_data = User_data.objects.filter(user_id=user_id)
        if len(user_data) > 0:
            likes = []
            for field in user_data:
                likes.append(field.liked_post_id)
            user_likes = list(set(likes).intersection(list((posts.values_list('id', flat=True)))))
            context['user_likes'] = user_likes
            page = render(request, template, context)
    return page


def post(request):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            body = request.POST['body']
            image = request.FILES.get('image', 'empty')
            new_post = Post(name=name, body=body) if image == 'empty' else Post(name=name, body=body, image=image)
            new_post.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())

def edit(request, post_id):
    post = Post.objects.get(id = post_id)
    context = {'post' : post}
    edit_page = render(request, 'edit.html', context)
    return edit_page

def save(request, post_id):
    if request.method == 'POST':
        form = PostsForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(id = post_id)
            post.name = request.POST['name']
            post.body = request.POST['body']
            if request.FILES.get('image', 'empty') != 'empty':
                post.image = request.FILES.get('image', 'empty')
            post.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())

def delete(request, post_id):
    post = Post.objects.get(id = post_id)
    post.delete()
    # also delete all fields in User_data with matching post_id's
    user_data = User_data.objects.filter(liked_post_id=post_id)
    if len(user_data) > 0:
        for post in user_data:
            post.delete()
    return HttpResponseRedirect('/')

def post_like(request, post_id):
    response = {"message": ""}
    status = 200 # increment
    
    user_id = request.COOKIES["user_id"]
    user_data = User_data.objects.filter(user_id=user_id)
    if len(user_data) > 0 and post_id in list(user_data.values_list('liked_post_id', flat=True)):
        # decrement like
        idx = list(user_data.values_list('liked_post_id', flat=True)).index(post_id)
        user_data[idx].delete()
        response["message"] = "decrement"
        post = Post.objects.get(id = post_id)
        post.like_count -= 1
        post.save()
        status = 201
    else:
        # increment like
        new_field = User_data(user_id=user_id, liked_post_id=post_id)
        new_field.save()
        response["message"] = "increment"
        post = Post.objects.get(id = post_id)
        post.like_count += 1
        post.save()
    json = JsonResponse(response, status=status)
    return json

def debug(request):
    for post in Post.objects.all():
        print(post.id)
    return HttpResponseRedirect('/')