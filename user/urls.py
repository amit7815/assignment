from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='homepage'),
    path('bloghome',views.blogHome,),
    path('detail/<int:id>',views.blogPost),
    path('signup',views.signup),
    path('logout',views.logout),
    path('login',views.login),
    path('createpost',views.create_post),
   
]