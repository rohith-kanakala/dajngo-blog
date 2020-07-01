from django.urls import path
from .views import home,view_blog,create_blog, edit_blog, BlogListView

urlpatterns = [
    path('',BlogListView.as_view(),name ="home"),
    path('add/',create_blog, name = "add_blog"),
    path('blog/<str:slug>',view_blog, name = 'view_blog'),
    path('edit/<str:slug>',edit_blog, name = 'edit_blog'),

]