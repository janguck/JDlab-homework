#from account.models import UserInformation
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


class SignUpFormView(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','is_active']
        widgets = {
            'username': forms.TextInput(attrs = {'placeholder': 'username 입력하세요'}),
            'password': forms.TextInput(attrs={'placeholder': 'password 입력하세요 ','type': 'password',
}),
        }
    def __init__(self, *args, **kwargs):
        super(SignUpFormView, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['is_active'].help_text = '체크안하면 로그인 못합니다.'

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': ("틀렸습니다."
                          "다시하세요."),
        'inactive': ("This account is inactive"),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
            )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
                )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache