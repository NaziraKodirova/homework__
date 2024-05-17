from django.urls import path
from users.views import (Login, Logout, Register, CustomUserUpdate,
                         ProfileUpdateView,ChangePasswordView
                         )

app_name = "users"

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('update_user/', CustomUserUpdate.as_view(), name='update_user'),
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

]
