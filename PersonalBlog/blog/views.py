from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

from .models import User,Post,Like

# Create your views here.
def index(request):
    return render(request,'index.html')

@never_cache
def loginn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            
            if user.is_superuser:
                messages.success(request, "Login successful.")
                return redirect("admin")
            
            messages.success(request, "Login successful.")
            return redirect("user")
            
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
    
    response = render(request, "login.html")
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response


@never_cache
def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.success(request, "registration successful.")
        return redirect('login')
    
    else:
        return render(request,'signup.html')
    
    
@never_cache
@login_required(login_url='login')
def user(request):
    posts = Post.objects.filter(is_available=True).order_by('-created_at')
    for post in posts:
        if post.tag:
            post.split_tags = post.tag.split(",")
        else:
            post.split_tags = []
        
        
        post.comments_list = post.comments.all()  
    
    return render(request, 'user.html', {'posts': posts})

@never_cache
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect("login")


@never_cache
@login_required(login_url='login')
def addpost(request):
    return render(request,'addpost.html')


@never_cache
@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')
        author = request.user  

        post = Post(
            title=title,
            content=content,
            tag=tags,
            image=image,
            author=author
        )
        
        try:
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('myprofile')
        except Exception as e:
            messages.error(request, f'There was an error creating your post. {str(e)}')
    
    return render(request, 'addpost.html')


@never_cache
@login_required(login_url='login')
def myprofile(request):
    user = request.user
    posts = Post.objects.filter(author=user,is_available=True).order_by('-created_at')
    posts_with_tags = []
    for post in posts:
        post_tags = post.tag.split(",") if post.tag else []
        posts_with_tags.append({
            'post': post,
            'tags': post_tags
        })

    followers_count = user.followed_by.count()  
    following_count = user.follows.count()  
    posts_count = posts.count()  

    context = {
        'user': user,
        'posts_with_tags': posts_with_tags,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts_count, 
    }
    return render(request, 'myprofile.html', context)



@never_cache
@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')
        post.title = title
        post.content = content
        post.tag = tags
        if image:
            post.image = image
        post.save()
        return redirect('myprofile')

    return render(request, 'editpost.html', {'post': post})


@never_cache
@login_required(login_url='login')
def delete_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.is_available = False
        post.save()
        return redirect('myprofile')
    
@never_cache
@login_required(login_url='login')
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        if 'remove_profile_pic' in request.POST:
            user.profile_pic.delete(save=False)  
            user.profile_pic = None 

        elif 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            user.profile_pic = profile_pic

        user.username = username
        user.email = email
        user.bio = bio
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('myprofile')  

    return render(request, 'updateprofile.html', {'user': user})

@never_cache
@login_required(login_url='login')
def search_results(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(tag__icontains=query,is_available=True) | Post.objects.filter(author__username__icontains=query,is_available=True)
    users = User.objects.filter(username__icontains=query)

    
    for post in posts:
        if post.tag:  
            post.split_tags = post.tag.split(',')
        else:
            post.split_tags = []  
    return render(request, 'search_results.html', {'posts': posts, 'users': users, 'query': query})

@never_cache
@login_required(login_url='login')
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    tags = [tag.strip() for tag in post.tag.split(",")] if post.tag else []

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            form = CommentForm()  
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'tags': tags,
    }
    return render(request, 'post_detail.html', context)

@never_cache
@login_required(login_url='login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).exists()
        
        if liked:
            Like.objects.filter(post=post, user=request.user).delete()
            liked = False
        else:
           
            Like.objects.create(post=post, user=request.user)
            liked = True
            
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
        })
    
    
    return HttpResponseRedirect(reverse('login'))


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

@never_cache
@login_required(login_url='login')
def follow_toggle(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        if request.user in user_to_follow.followed_by.all():
            user_to_follow.followed_by.remove(request.user)
            followed = False
        else:
            user_to_follow.followed_by.add(request.user)
            followed = True
        return JsonResponse({'followed': followed})
    return JsonResponse({'error': 'Cannot follow yourself'}, status=400)


@never_cache
@login_required(login_url='login')
def user_list_view(request, username, list_type):
    user = get_object_or_404(User, username=username)
    if list_type == 'following':
        users_list = user.follows.all()
        title = f'{username}\'s Following'
    elif list_type == 'followers':
        users_list = user.followed_by.all()
        title = f'{username}\'s Followers'
    else:
        users_list = []
        title = 'User List'
    
    return render(request, 'user_list.html', {
        'users_list': users_list,
        'title': title,
        'list_type': list_type
    })
