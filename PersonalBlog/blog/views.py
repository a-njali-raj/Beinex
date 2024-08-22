from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .models import User

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


