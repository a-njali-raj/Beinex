from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


from .models import User,Post

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
    return render(request,'user.html')

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
def myprofile(request):
    user = request.user
    # Fetch the posts of the logged-in user
    posts = Post.objects.filter(author=user).order_by('-created_at') 
    
    # Example data for followers and following - you should have actual logic here
    followers_count = 0  # Replace with actual count if you have a followers model
    following_count = 0  # Replace with actual count if you have a following model

    context = {
        'user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'myprofile.html', context)