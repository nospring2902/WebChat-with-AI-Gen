from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    main_language = forms.CharField(max_length=100, required=True, help_text='Ngôn ngữ chính của bạn.')

    class Meta:
        model = User
        fields = ('username', 'main_language', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        user_profile = UserProfile.objects.create(user=user, main_language=self.cleaned_data['main_language'])
        return user
