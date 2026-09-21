from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "email", "password", "confirm_password"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].strip().lower()
        user.username = email
        user.email = email
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Your password"}))

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("email") or not cleaned.get("password"):
            return cleaned
        email = cleaned["email"].strip().lower()
        user = authenticate(username=email, password=cleaned["password"])
        if user is None:
            raise forms.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        cleaned["user"] = user
        return cleaned
