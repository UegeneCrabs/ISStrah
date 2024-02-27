from django.contrib.auth.views import LogoutView
from django.urls import path

from ISStrah import settings
from main import views
from main.views import LoginUser

urlpatterns = [
    path('', views.main_layout, name='main_layout'),
    path('register/', views.register_client, name='register_client'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
