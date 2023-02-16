from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path("login",views.login,name='login'),
    path("logout",views.logout,name='logout'),
    path("signup",views.signup,name='signup'),
    path('camera',views.camera,name='camera'),
    path('emotion',views.emotion,name='emotion'),
    path('movie/<int:id>',views.movie,name='movie'),
    path('song/<int:id>',views.song,name='song'),
    path("try",views.try1,name='try1'),
]