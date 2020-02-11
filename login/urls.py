from django.urls import path
from django.contrib.auth.views import *
from django.urls import reverse_lazy
from . import views
from .forms import LoginForm


"""
    for templates
    login:<name>

"""
app_name = 'login'

urlpatterns = [
    path('', LoginView.as_view(authentication_form=LoginForm), name="connect"),
    path('logout/', LogoutView.as_view(), name="disconnect"),
    path('join/', views.Join.as_view(), name="join"),
    path('mypage/', views.mypage, name="mypage"),

    # Change the first and last name.
    path('change-profile/', views.UpdateProfile.as_view(), name="update"),

    # Change the password.
    path('change-password/',
         PasswordChangeView.as_view(
            success_url=reverse_lazy('login:password_change_done')),
         name="change_pwd"),

    path('change-password/done/',
         PasswordChangeDoneView.as_view(), name="password_change_done"),

    # Receive an email to get a new password.
    path('reset-password/',
         PasswordResetView.as_view(
            success_url=reverse_lazy('login:password_reset_done')),
         name="password_reset"),

    path('reset-password/done/',
         PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('login:password_reset_complete')
         ),
         name="password_reset_confirm"),

    path('reset/done/',
         PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]
