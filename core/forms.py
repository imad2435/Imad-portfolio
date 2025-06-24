# imad_portfolio/core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ContactMessage, Project, Skill, PersonalInfo, Experience

# --- PUBLIC CONTACT FORM ---
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 text-base outline-none text-apex-white py-3 px-4 leading-8', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 text-base outline-none text-apex-white py-3 px-4 leading-8', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 h-40 text-base outline-none text-apex-white py-3 px-4 resize-none leading-6', 'placeholder': 'Your Message'}),
        }

# --- DASHBOARD FORMS ---
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'bio': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'rows': 5}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'github_url': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'technologies': forms.SelectMultiple(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600', 'size': 5}),
            'github_link': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'live_link': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'})}

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'company': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'start_date': forms.DateInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600', 'rows': 5}),
        }

class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User; fields = ('username', 'email', 'is_staff', 'is_superuser')
        widgets = {'username': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),'is_staff': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),'is_superuser': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'})}

class AdminChangeForm(forms.ModelForm):
    class Meta:
        model = User; fields = ('username', 'email', 'is_staff', 'is_superuser')
        widgets = {'username': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),'is_staff': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),'is_superuser': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'})}