from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from django import forms
from .models import PollOption


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class PollVoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll')
        super(PollVoteForm, self).__init__(*args, **kwargs)
        for option in poll.options.all():
            # Используем BooleanField для каждого варианта
            self.fields[f'option_{option.id}'] = forms.BooleanField(
                label=option.option_text,
                required=False,  # Если нужно, чтобы пользователь выбирал хотя бы один вариант, поставьте required=True
                widget=forms.CheckboxInput
            )