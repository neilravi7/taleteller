from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register', views.UserCreationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(template_name='account/login.html', next_page="post:home"), name='logout'),
    path('dashboard/', views.AuthorDashboardView.as_view(), name='dashboard'),
    path('user/profile', views.AuthorProfile.as_view(), name="update_profile"),
]