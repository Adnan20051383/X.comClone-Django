from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput

from auth_user.models import Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt'}), max_length=50,
        required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt'}), required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt'}), required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt'}), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'image'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'prompt'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'prompt'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class': 'prompt'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'prompt'}))
    address = forms.CharField(widget=TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ('image', 'first_name', 'last_name', 'bio', 'phone_number', 'address')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Display current image info if it exists
        if self.instance and self.instance.image:
            self.fields['image'].help_text = f"Current file: {self.instance.image.url}"

    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        if not self.cleaned_data['image'] and self.instance.image:
            profile.image = self.instance.image  # Use existing image if no new file is uploaded
        if commit:
            profile.save()
        return profile
