from django.urls import path
from core import views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='users registration'),
    path('login', views.UserLoginView.as_view(), name='user login'),
    path('profile', views.RetrieveUpdateDestroyView.as_view(), name='user profile'),
    path('update_password', views.UpdatePasswordView.as_view(), name='update password'),
]
