from django import forms
from django.contrib.auth.forms import( UserCreationForm, PasswordChangeForm as AuthPasswordForm)

from .models import User

class SignupForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'gender']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email:
			qs = User.objects.filter(email=email)
			if qs.exists():
				raise forms.ValidationError("이미 등록된 이메일 입니다.")
		return email

class ProfileForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['avatar', 'last_name', 'first_name', 'gender', 'phone_number', 'website_url', 'bio']

class PasswordChangeForm(AuthPasswordForm):
	def clean_new_password2(self):
		old_password = self.cleaned_data.get('old_password')
		# new_password2 = super().clean_new_password2()
		# if old_password == new_password2:
		# 	raise forms.ValidationError("암호가 같습니다.")
		new_password1 = self.cleaned_data.get('new_password')
		if old_password and new_password1:
			if old_password == new_password1:
				raise forms.ValidationError("기존 암호와 같습니다. 다시 입력하세요.")
		return new_password1
