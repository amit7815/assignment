from django.shortcuts import render, redirect
from user.forms.authforms import CustomerCreationForm,CustomerLoginForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from .models import Post, User
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'user/home.html')

def signup(request):
    ''' create user '''
    if request.method == "GET":
        form = CustomerCreationForm()
        context = {
            'form':form
        }
        return render(request, 'user/signup.html',context = context)
    else:
        form = CustomerCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.username = form.cleaned_data['Username']
            user.save()
            messages.success(request,"Your account is created")
            return redirect('/login')
           
        context = {
            'form':form
            }
        return render(request, 'user/signup.html',context = context)


def login(request):
    ''' Login User '''
    if request.method == 'GET':
        form = CustomerLoginForm()
        return render(request, 'user/login.html',context = {'form':form})
    else:
        form = CustomerLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password= password)
            if user:
                loginUser(request, user)   # it will save user in session
                messages.success(request,"Login sucessfull")
                return redirect('homepage')
            else:
                pass
        else:
            return render(request, 'user/login.html',context = {'form':form})
        


def logout(request):
    # request.session.clear() # this will clear the session or logout we can also use logout fn for this
    logoutUser(request)
    messages.success(request,"Logout Successfull")
    return redirect('/login')


def blogHome(request):
    ''' Home page for post '''
    allPosts=Post.objects.all()
    print(request.user.username)
    context={"allPosts":allPosts}
    return render(request,"user/blogHome.html",context)

def blogPost(request,id):
    ''' detail page for a post '''
    post=Post.objects.filter(id=id)[0]
    context={"post":post}
    print(post)
    return render(request,"user/blogPost.html",context)


def create_post(request):
    ''' view for creating post '''
    if request.method == 'POST':
        user = request.user
        text = request.POST['text']
        ins = Post(user=user, text = text)
        messages.success(request,"Your Post is created sucessfully")
        ins.save()
        return redirect('homepage')
    else:
        return render(request, 'user/createPost.html')
