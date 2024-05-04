from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('login/', views.LogInView.as_view(), name ='login'),
    path('register/', views.RegisterView.as_view(), name ='register'),
]