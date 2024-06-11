from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authapp.models import ShopUser

class ShopUserCheckForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        plaintext_password = self.cleaned_data.get('password1')
        if plaintext_password:
            user.plaintext_password = plaintext_password
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

