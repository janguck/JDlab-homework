from django.views.generic import CreateView
from account.forms import SignUpFormView, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import FormView, RedirectView,ListView
from django.contrib.auth import login as auth_login, logout as auth_logout

class SignUpView(CreateView):

    template_name = "signup.html"
    form_class = SignUpFormView
    success_url = '/home'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        existing_user = User.objects.get(username=username,password=password)
        login(self.request,existing_user)
        return valid

class LogOutView(RedirectView):

    url = '/home'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)

class LoginView(FormView):

    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = '/home'

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)

class SionBackend(object):

    def authenticate(self, username=None, password=None):
        if username is None:
            return None
        try:
            existing_user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return None
        return existing_user

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            return None

class UserListView(ListView):

    model = User
    template_name = "my_profile.html"
    context_object_name = "users"