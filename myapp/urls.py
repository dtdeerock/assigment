from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('user_chat/', views.user_chat, name='user_chat'),
]
