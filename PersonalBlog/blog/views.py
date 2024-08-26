from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
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
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']=user.username
            if user.is_superuser:
                messages.success(request, "Login successful.")
                return redirect("admin")
            elif user.is_staff:
                return redirect("staff_dashboard")
            
            messages.success(request, "Login successful.")
            return redirect("user")
            
        else:
            messages.error(
                request, "Invalid username or password"
            )  # Add an error message
            return redirect("login")  
    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
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
@login_required
def logout(request):
    auth.logout(request)
    return redirect("login")


@never_cache
@login_required
def addpost(request):
    return render(request,'addpost.html')


@never_cache
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')
        author = request.user  # Set the current user as the author
        
        # Create a new Post object
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


@login_required
@never_cache
def myprofile(request):
    user = request.user
    # Fetch the posts of the logged-in user
    posts = Post.objects.filter(author=user,is_available=True).order_by('-created_at')
    
    # Split the tags in the view and pass them to the context
    posts_with_tags = []
    for post in posts:
        post_tags = post.tag.split(",") if post.tag else []
        posts_with_tags.append({
            'post': post,
            'tags': post_tags
        })

    # Example data for followers and following - you should have actual logic here
    followers_count = 0  # Replace with actual count if you have a followers model
    following_count = 0  # Replace with actual count if you have a following model

    context = {
        'user': user,
        'posts_with_tags': posts_with_tags,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'myprofile.html', context)



@login_required
@never_cache
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')

        # Update the post
        post.title = title
        post.content = content
        post.tag = tags
        if image:
            post.image = image
        post.save()

        # Redirect to profile page
        return redirect('myprofile')

    return render(request, 'editpost.html', {'post': post})

@login_required
@never_cache
def delete_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.is_available = False
        post.save()
        return redirect('myprofile')
    
@login_required
@never_cache
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')

        # Handle profile picture
        if 'remove_profile_pic' in request.POST:
            user.profile_pic.delete(save=False)  # Delete the file
            user.profile_pic = None  # Set the profile_pic field to None

        elif 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            user.profile_pic = profile_pic

        user.username = username
        user.email = email
        user.bio = bio
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('myprofile')  # Redirect to the profile page or another page after update

    return render(request, 'updateprofile.html', {'user': user})

@login_required
@never_cache
def search_results(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(tag__icontains=query) | Post.objects.filter(author__username__icontains=query,is_available=True)
    users = User.objects.filter(username__icontains=query)

    # Preprocess tags
    for post in posts:
        if post.tag:  # Ensure the tag is not None
            post.split_tags = post.tag.split(',')
        else:
            post.split_tags = []  # Provide an empty list if no tags are present

    return render(request, 'search_results.html', {'posts': posts, 'users': users, 'query': query})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            form = CommentForm()  # Clear the form after submission
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'post_detail.html', context)

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Check if the user has already liked the post
        if Like.objects.filter(post=post, user=request.user).exists():
            # If the user has already liked the post, remove the like
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            # If the user hasn't liked the post yet, add the like
            Like.objects.create(post=post, user=request.user)
    
    # Redirect to the same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

