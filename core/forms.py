# imad/core/forms.py

from django import forms
from .models import ContactMessage, Project, Skill

# ==============================================================================
# FORM FOR THE PUBLIC CONTACT SECTION
# ==============================================================================
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 text-base outline-none text-apex-white py-3 px-4 leading-8 transition-colors duration-200 ease-in-out',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 text-base outline-none text-apex-white py-3 px-4 leading-8 transition-colors duration-200 ease-in-out',
                'placeholder': 'Your Email'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-apex-dark rounded-lg border border-white/10 focus:border-apex-purple focus:ring-2 focus:ring-apex-purple/50 h-40 text-base outline-none text-apex-white py-3 px-4 resize-none leading-6 transition-colors duration-200 ease-in-out',
                'placeholder': 'Your Message'
            }),
        }


# ==============================================================================
# FORMS FOR THE CUSTOM ADMIN DASHBOARD
# ==============================================================================
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'technologies', 'github_link', 'live_link', 'display_order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'technologies': forms.SelectMultiple(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'size': 5}),
            'github_link': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'live_link': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'display_order': forms.NumberInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
        }
        # imad/core/forms.py

from django import forms
from .models import ContactMessage, Project, Skill, PersonalInfo # Add PersonalInfo

# ... your existing forms ...

# --- ADD THIS NEW FORM ---
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        # We include all fields to make them editable
        fields = ['name', 'title', 'bio', 'profile_image', 'cv', 'email', 'github_url', 'linkedin_url']

        # Add Tailwind CSS classes for the dashboard's dark theme
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
        # imad/core/forms.py

from django import forms
from .models import ContactMessage, Project, Skill, PersonalInfo, Experience # Add Experience

# ... your existing forms ...

# --- ADD THIS NEW FORM ---
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['category', 'title', 'company', 'start_date', 'end_date', 'description']

        # Add Tailwind CSS classes and specific input types for dates
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'company': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'start_date': forms.DateInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500', 'rows': 5}),
        }

        # At the top of forms.py, add these imports
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# ... your other forms ...

# ==============================================================================
# FORMS FOR MANAGING ADMIN USERS
# ==============================================================================

class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'is_staff', 'is_superuser')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),
        }

class AdminChangeForm(UserChangeForm):
    # We remove the password field to prevent it from being accidentally changed.
    # Password changes should be handled separately for security.
    password = None 
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'is_staff', 'is_superuser')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2 border border-gray-600'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-indigo-500 bg-gray-700 border-gray-600 rounded'}),
        }