from django import forms
from account.models import Customer
from django.contrib.auth import password_validation, authenticate


class SignUpForm(forms.models.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password']

    def save(self, commit=True):  # 저장하는 부분 오버라이딩
        user = super(SignUpForm, self).save(commit=False)  # 본인의 부모를 호출해서 저장하겠다.
        if commit:
            user.save()
        return user

class LoginForm(forms.models.ModelForm):
    class Meta:
        model = Customer
        fields = ("username", "password",)

        widgets = {
            'username' : forms.fields.TextInput(attrs={
                'placeholder' : '가입된 ID를 입력하세요',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '비밀번호를 입력하세요',
            })
        }

        error_messages = {
            'text' : {"required", "ID 또는 비밀번호를 확인해주세요."}
        }


    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("ID 또는 비밀번호가 틀렸습니다.")
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