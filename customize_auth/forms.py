from django import forms

from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=255, help_text='请输入正确的用户名')
    password = forms.CharField(label='密码', strip=False, widget=forms.PasswordInput, help_text='请输入密码')
    password_confirm = forms.CharField(label='确认密码', strip=False, widget=forms.PasswordInput,
                                       help_text='请输入一致的密码')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not username:
            raise forms.ValidationError('用户名不能为空')
        if User.objects.filter(name=username).exists():
            raise forms.ValidationError('用户名已存在')
        if not password:
            raise forms.ValidationError('密码不能为空')
        if not password_confirm:
            raise forms.ValidationError('确认密码不能为空')
        if password != password_confirm:
            raise forms.ValidationError('两次输入密码不一致')
        return dict(username=username, password=password, password_confirm=password_confirm)


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=255, help_text='请输入正确的用户名')
    password = forms.CharField(label='密码', strip=False, widget=forms.PasswordInput, help_text='请输入正确的密码')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username:
            raise forms.ValidationError('用户名不能为空')
        if not User.objects.filter(name=username).exists():
            raise forms.ValidationError('用户名或密码错误')
        if not password:
            raise forms.ValidationError('密码不能为空')
        user = User.objects.filter(name=username).first()
        if not user.verify_password(password):
            raise forms.ValidationError('用户名或密码错误')
        return dict(username=username, password=password)


class UserForm(forms.ModelForm):
    name = forms.CharField(label='昵称', max_length=255, help_text='请输入正确的昵称')

    class Meta:
        model = User
        fields = ['name', 'sex', 'description', 'email', 'phone_number', 'birthday']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'materialize-textarea'}),
            'email': forms.EmailInput(),
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

