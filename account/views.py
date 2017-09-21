from django.views.generic import CreateView,FormView,TemplateView
from account.forms  import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from account.models import Customer
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from django.conf import settings
from urllib.parse import urlparse

class SignUpview(CreateView):
    template_name = "signup.html"
    model = Customer
    form_class = SignUpForm
    success_url = '/home'

    def form_valid(self, form):
        valid = super(SignUpview, self).form_valid(form)
        return valid

class LoginView(FormView):
    template_name = 'login.html'
    model = Customer
    form_class = LoginForm

    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            print("sdsd")
            redirect_to = self.success_url

        netloc = urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False


    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(form)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)