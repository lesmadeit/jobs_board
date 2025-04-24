from django.urls import path, include, re_path
from .views import  profile, RegisterView, view_profile, profile_update
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomLoginView, CustomLogoutView, ResetPasswordView, ChangePasswordView

from accounts.forms import LoginForm


app_name = 'accounts'
urlpatterns = [
     
    
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('profile/create/', profile, name='profile'),
    path('profile/edit/', profile_update, name='profile_update'),
    path('profile/', view_profile, name='view_profile'),                                    

    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)