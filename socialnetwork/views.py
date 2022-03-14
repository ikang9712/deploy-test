from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from socialnetwork.forms import LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import Post, Profile, Comment
import json

@login_required
def get_post_action(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    post_data = []
    comment_data = []
    for post_item in Post.objects.all():
        item_time = post_item.creation_time
        formatted_item_time = item_time.strftime("%m/%d/%Y %I:%M %p")
        my_item = {
            'id': post_item.id,
            'text': post_item.text,
            'user': post_item.user.username,
            'user_f': post_item.user.first_name,
            'user_l': post_item.user.last_name,
            'userID': post_item.user.id,
            'userUser': post_item.user,
            'creation_time': formatted_item_time,
        }
        post_data.append(my_item)
    for comment_item in Comment.objects.all():
        item_time = comment_item.creation_time
        formatted_item_time = item_time.strftime("%m/%d/%Y %I:%M %p")
        my_item = {
            'id': comment_item.id,
            'text': comment_item.text,
            'user': comment_item.user.username,
            'user_f': comment_item.user.first_name,
            'user_l': comment_item.user.last_name,
            'post': comment_item.post,
            'post_id': comment_item.post.id,
            'userID': comment_item.user.id,
            'creation_time': formatted_item_time,
        }
        comment_data.append(my_item)
    response_data = {
        'posts': post_data,
        'comments': comment_data,
    }
    response_json = json.dumps(response_data, default=str)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response

@login_required
def get_post_follower_action(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    post_data = []
    follower_post_ids = []
    comment_data = []
    for post_item in Post.objects.all():
        if post_item.user in request.user.profile.following.all():
            item_time = post_item.creation_time
            formatted_item_time = item_time.strftime("%m/%d/%Y %I:%M %p")
            my_item = {
                'id': post_item.id,
                'text': post_item.text,
                'user': post_item.user.username,
                'user_f': post_item.user.first_name,
                'user_l': post_item.user.last_name,
                'userID': post_item.user.id,
                'userUser': post_item.user,
                'creation_time': formatted_item_time,
            }
            post_data.append(my_item)
            follower_post_ids.append(post_item.id)
    for comment_item in Comment.objects.all():
        if comment_item.post.id in follower_post_ids:
            item_time = comment_item.creation_time
            formatted_item_time = item_time.strftime("%m/%d/%Y %I:%M %p")
            my_item = {
                'id': comment_item.id,
                'text': comment_item.text,
                'user': comment_item.user.username,
                'user_f': comment_item.user.first_name,
                'user_l': comment_item.user.last_name,
                'post': comment_item.post,
                'post_id': comment_item.post.id,
                'userID': comment_item.user.id,
                'creation_time': formatted_item_time,
            }
            comment_data.append(my_item)
    response_data = {
        'posts': post_data,
        'comments': comment_data,
    }
    response_json = json.dumps(response_data, default=str)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

@login_required
def add_post_action(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'item' in request.POST or not request.POST['item']:
        return _my_json_error_response("You must enter text to make a new post.", status=400)

    new_item = Post(text=request.POST['item'], user=request.user, creation_time= datetime.now())
    new_item.save()

    return get_post_action(request)

@login_required
def add_comment_action(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter text to make a new comment.", status=400)
    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("post id not identified.", status=400)

    item_post_id = request.POST['post_id']
    item_post = Post.objects.get(id = int(item_post_id))
    new_item = Comment(text=request.POST['comment_text'], 
                       user=request.user,
                       post=item_post,
                       creation_time= datetime.now())
    new_item.save()
    return get_post_action(request)

@login_required
def add_comment_follower_action(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter text to make a new comment.", status=400)
    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("post id not identified.", status=400)

    item_post_id = request.POST['post_id']
    item_post = Post.objects.get(id = int(item_post_id))
    new_item = Comment(text=request.POST['comment_text'], 
                       user=request.user,
                       post=item_post,
                       creation_time= datetime.now())
    new_item.save()
    return get_post_follower_action(request)


@login_required
def global_action(request):
    context = {'posts': Post.objects.all().order_by("-creation_time")}
    if request.method == 'GET':
        return render(request, 'socialnetwork/global.html',context)
    context['posts'] = Post.objects.all().order_by("-creation_time")
    return render(request, 'socialnetwork/global.html',context)

@login_required
def my_profile_action(request):
    # GET
    if request.method == 'GET':
        context = {'profile': request.user.profile,
                    'form': ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/profile.html',context)
    form = ProfileForm(request.POST, request.FILES)
    # invalid form
    if not form.is_valid():
        context = {'profile': request.user.profile, 'form': form }
        return render(request, "socialnetwork/profile.html", context)
    
    # valid form
    myprofile = request.user.profile
    pic = form.cleaned_data['picture']

    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
    myprofile.picture = form.cleaned_data['picture']
    myprofile.bio = form.cleaned_data['bio']
    myprofile.content_type = pic.content_type
    myprofile.save()
    context = {
        'profile': myprofile,
        'form': form,
    }
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def get_photo_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    print('Picture #{} fetched from db: {} (type={})'.format(user_id, user.profile.picture, type(user.profile.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not user.profile.picture:
        raise Http404

    return HttpResponse(user.profile.picture, content_type=user.profile.content_type)

@login_required
def other_profile_action(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    print("other_user profile entered")
    return render(request, 'socialnetwork/otherprofile.html',{'profile': other_user.profile})

@login_required
def follow_action(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    print("after follow")
    print(request.user.profile.following.all())
    return render(request, 'socialnetwork/otherprofile.html', {'profile': user_to_follow.profile})

@login_required
def unfollow_action(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    print("after unfollow")
    print(request.user.profile.following.all())
    return render(request, 'socialnetwork/otherprofile.html', {'profile': user_to_unfollow.profile})

@login_required
def follower_action(request):
    context = {'posts': Post.objects.all().order_by("-creation_time")}
    return render(request, 'socialnetwork/follower.html',context)

def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)
    
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password']) 
    login(request, new_user)
    return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_profile = Profile(user=new_user)
    new_profile.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))