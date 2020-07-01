from django.shortcuts import render, reverse,get_object_or_404,redirect
from .models import Blog
from django.http import Http404
from .blog_form import Blog_form,BlogForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
# Create your views here.
def home(request):
    blog = Blog.objects.all().order_by('-timestamp')
    return render (request,"home.html",{"blogs":blog})


# class based views

class BlogListView(ListView):
    model = Blog
    template_name = "home.html"
    context_object_name = "blogs"
    ordering = ['-timestamp']
    paginate_by = 2



def view_blog(request,slug):
    b = get_object_or_404(Blog, slug = slug)
    l = [tag[0] for tag in Blog.TAGS]
    i = l.index(b.tags)
    tags= Blog.TAGS[i][1]
    return render(request,'blog.html', {'title':'User Blog','blog':b,'tags':tags})





@login_required
def create_blog(request):
    if request.method=='POST':
        form = BlogForm(request.POST or None,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user.profile
            instance.save()
            messages.success(request,message="succesfully created a Post")
            return redirect("home")
        else:
            #messages.error(request,messages="error in post creation")
            return render(request, "blog_form.html", {'form': form})
    form = BlogForm()
    return render(request,"blog_form.html",{'form':form})


@login_required
def edit_blog(request,slug = None):
    blog = get_object_or_404(Blog,slug=slug)
    if request.user == blog.author.user:
        form = BlogForm(data= request.POST or None, files=request.FILES or None,instance=blog)
        if form.is_valid():
            b = form.save(commit=False)
            b.save()
            return redirect("home")
        return render(request,"blog_form.html",{"form":form,"blog":blog})
    else:
        return Http404()





