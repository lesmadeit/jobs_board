from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from .token import account_activation_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm




class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'accounts/register.html'


    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')
        
        #else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # User activation
            current_site = get_current_site(request)
            subject = 'Please activate your account'
            message = render_to_string('shop/accounts/email_activate/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.content_subtype = 'html'  # Set email as HTML
            send_email.send()


            messages.success(request, 'Please check your email to activate your account.')
            return redirect('/account/register/?command=verification&email=' + to_email)      
            
        
        return render(request, self.template_name, {'form': form})



# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message_name = 'accounts/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_message = "Succesfully Changed Your Password"
    success_url = reverse_lazy('jobsapp-home')



class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/logout.html')
    


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensures profile exists

    if not created:
        return redirect('accounts:view_profile')
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            return redirect('accounts:view_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile_update(request):
    """
    Allow a user to update their profile.
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            return redirect('accounts:view_profile')  # Redirect back to profile view
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)

    return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request):
    """
    Display the user's profile with an edit button.
    """
    profile = get_object_or_404(Profile, user=request.user)
    
    return render(request, 'accounts/view_profile.html', {'profile': profile})




