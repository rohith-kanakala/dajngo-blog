from django.shortcuts import render, redirect
from .user_forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Blog
from django.core.paginator import Paginator
# Create your views here.


def register(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') # form.cleaned_data['username']
            form.save()
            messages.success(request,"Added account !")
            return redirect ("login")
        return render(request, 'users/register.html', {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None , request.FILES or None, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"succcesfuuly updated")
    else:
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    return render(request,"users/profile.html",{"u_form":u_form,"p_form":p_form})


@login_required
def view_posts(request):
    blog_list = Blog.objects.filter(author=request.user.profile).order_by('-timestamp')
    paginator = Paginator(blog_list,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"Users/my_posts.html",{'page_obj': page_obj})
