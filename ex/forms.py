from django import forms
from django.db.models import fields
from .models import User, Tip

class RegisterForm(forms.Form):
	username = forms.CharField(required=True, max_length=150)
	password = forms.CharField(
		required=True,
		min_length=8,
		max_length=128,
		widget=forms.PasswordInput(render_value=False)
	)
	password_confirmation = forms.CharField(
		required=True,
		min_length=8,
		max_length=128,
		widget=forms.PasswordInput(render_value=False)
	)

	def clean(self):
		cleaned_data = super().clean()

		username = cleaned_data.get("username")
		if User.objects.filter(username=username):
			raise forms.ValidationError(
                "Such username already exist. Please try another username"
            )

		password = cleaned_data.get("password")
		password_confirmation = cleaned_data.get("password_confirmation")
		if password and password_confirmation:
			if password != password_confirmation:
				raise forms.ValidationError(
                    "Password confirmation failed. Please try again"
                )
		return cleaned_data


class LoginForm(forms.Form):
	username = forms.CharField(required=True, max_length=32)
	password = forms.CharField(
		required=True,
		max_length=256,
		widget=forms.PasswordInput()
	)

	def clean(self):
		cleaned_data = super().clean()

		username = cleaned_data.get("username")
		password = cleaned_data.get("password")
		users = User.objects.filter(username=username)
		if len(users) == 0:
			raise forms.ValidationError(
                "Wrong username"
            )
		if not users[0].check_password(password):
			raise forms.ValidationError(
                "Wrong password"
            )
		return cleaned_data

class TipForm(forms.ModelForm):
	class Meta:
		model = Tip
		fields = {'content'}
