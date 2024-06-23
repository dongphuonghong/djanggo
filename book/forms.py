from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import BorrowedBook
class BorrowedBookForm(forms.ModelForm):    
    class Meta:
        model = BorrowedBook
        fields = ['borrowed_date', 'return_date']
class CreationFormUser(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")    
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email already exists")
        return cleaned_data   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Using email as the username
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
class emailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)
    def clean(self):    
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')    
        try:    
            user = User.objects.get(email=email)
        except User.DoesNotExist:   
            raise forms.ValidationError(_("The email or password you entered is incorrect, please try again"))
        if not user.check_password(password):   
            raise forms.ValidationError(_("The email or password you entered is incorrect, please try again"))
        self.confirm_login_allowed(user)
        self.user_cache = user  
        return self.cleaned_data