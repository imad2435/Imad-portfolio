# imad/core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

# Import all necessary models and forms
from .models import PersonalInfo, Skill, Project, Experience, ContactMessage
from .forms import (
    ContactForm, ProjectForm, SkillForm, PersonalInfoForm, ExperienceForm,
    AdminCreationForm, AdminChangeForm
)

# ==============================================================================
#  PUBLIC-FACING VIEW
# ==============================================================================
def home(request):
    """Handles the public homepage and contact form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save(); return redirect('/#contact-form')
    else:
        form = ContactForm()
    context = {'info': PersonalInfo.objects.first(), 'skills': Skill.objects.all(), 'work_experiences': Experience.objects.filter(category='work'),'education_experiences': Experience.objects.filter(category='education'), 'projects': Project.objects.all(), 'form': form}
    return render(request, 'core/index.html', context)

# ==============================================================================
#  CUSTOM DASHBOARD & AUTH VIEWS
# ==============================================================================
def custom_login_view(request):
    """A custom, secure login view that only allows staff members to log in."""
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None and user.is_staff:
                login(request, user); return redirect('dashboard')
            else: messages.error(request, "Invalid credentials or not an admin user.")
        else: messages.error(request, "Invalid credentials.")
    return render(request, 'core/login.html', {'form': AuthenticationForm()})

@login_required(login_url='/dashboard/login/')
def dashboard_view(request):
    """The main view for our custom dashboard."""
    info = PersonalInfo.objects.first()
    if messages_qs := ContactMessage.objects.all():
        request.session['last_message_timestamp'] = messages_qs.first().sent_at.isoformat()
    return render(request, 'core/dashboard.html', {'info': info})

def custom_logout_view(request):
    """Logs the user out and redirects to the homepage."""
    logout(request); return redirect('core:home')

# ==============================================================================
#  HTMX PARTIAL VIEWS (FOR DISPLAYING CONTENT)
# ==============================================================================
@login_required
def load_personal_info(request): return render(request, 'core/partials/personal_info_card.html', {'info': PersonalInfo.objects.first()})
@login_required
def load_skills(request): return render(request, 'core/partials/skills_list.html', {'skills': Skill.objects.all()})
@login_required
def load_experiences(request):
    context = {'work_experiences': Experience.objects.filter(category='work'), 'education_experiences': Experience.objects.filter(category='education')}
    return render(request, 'core/partials/experiences_list.html', context)
@login_required
def load_projects(request): return render(request, 'core/partials/projects_table.html', {'projects': Project.objects.all()})
@login_required
def load_messages(request):
    if messages_qs := ContactMessage.objects.all(): request.session['last_message_timestamp'] = messages_qs.first().sent_at.isoformat()
    return render(request, 'core/partials/messages_list.html', {'messages': messages_qs})
@login_required
def load_admins(request): return render(request, 'core/partials/admins_list.html', {'admins': User.objects.filter(is_staff=True)})
def check_new_messages(request):
    last_seen_timestamp = request.session.get('last_message_timestamp')
    if not last_seen_timestamp: return HttpResponse(status=204)
    if ContactMessage.objects.filter(sent_at__gt=last_seen_timestamp).exists():
        response = HttpResponse(status=200); response['HX-Trigger'] = 'newMessage'; return response
    return HttpResponse(status=204)

# ==============================================================================
#  CRUD VIEWS
# ==============================================================================
# --- PERSONAL INFO ---
@login_required
def update_personal_info(request, pk):
    personal_info = get_object_or_404(PersonalInfo, pk=pk)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=personal_info)
        if form.is_valid():
            form.save()
            # On success, return the updated info card directly to the target div
            return render(request, 'core/partials/personal_info_card.html', {'info': personal_info})
    else:
        form = PersonalInfoForm(instance=personal_info)
    # For a GET request or invalid form, show the form in the modal
    return render(request, 'core/partials/personal_info_form.html', {'form': form})

# --- PROJECTS ---
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES);
        if form.is_valid(): form.save(); return render(request, 'core/partials/projects_table.html', {'projects': Project.objects.all()})
    else: form = ProjectForm()
    return render(request, 'core/partials/project_form.html', {'form': form})
@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid(): form.save(); return render(request, 'core/partials/projects_table.html', {'projects': Project.objects.all()})
    else: form = ProjectForm(instance=project)
    return render(request, 'core/partials/project_form.html', {'form': form, 'project': project})
@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST': project.delete(); return render(request, 'core/partials/projects_table.html', {'projects': Project.objects.all()})
    return render(request, 'core/partials/project_delete_confirm.html', {'project': project})

# --- SKILLS ---
@login_required
def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST);
        if form.is_valid(): form.save(); return render(request, 'core/partials/skills_list.html', {'skills': Skill.objects.all()})
    else: form = SkillForm()
    return render(request, 'core/partials/skill_form.html', {'form': form})
@login_required
def update_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill);
        if form.is_valid(): form.save(); return render(request, 'core/partials/skills_list.html', {'skills': Skill.objects.all()})
    else: form = SkillForm(instance=skill)
    return render(request, 'core/partials/skill_form.html', {'form': form, 'skill': skill})
@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST': skill.delete(); return render(request, 'core/partials/skills_list.html', {'skills': Skill.objects.all()})
    return render(request, 'core/partials/skill_delete_confirm.html', {'skill': skill})

# In core/views.py

# --- EXPERIENCE CRUD VIEWS ---

@login_required
def create_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            # On success, send back an empty response with a trigger
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'experiences-changed'
            return response
    else:
        form = ExperienceForm()
    return render(request, 'core/partials/experience_form.html', {'form': form})

@login_required
def update_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            # On success, send back an empty response with a trigger
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'experiences-changed'
            return response
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'core/partials/experience_form.html', {'form': form})

@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        experience.delete()
        # On success, send back an empty response with a trigger
        response = HttpResponse(status=204)
        response['HX-Trigger'] = 'experiences-changed'
        return response
    
    return render(request, 'core/partials/experience_delete_confirm.html', {'experience': experience})
# --- ADMIN USERS ---
@login_required
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid(): form.save(); return render(request, 'core/partials/admins_list.html', {'admins': User.objects.filter(is_staff=True)})
    else: form = AdminCreationForm()
    return render(request, 'core/partials/admin_form.html', {'form': form})
@login_required
def update_admin(request, pk):
    admin_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminChangeForm(request.POST, instance=admin_user);
        if form.is_valid(): form.save(); return render(request, 'core/partials/admins_list.html', {'admins': User.objects.filter(is_staff=True)})
    else: form = AdminChangeForm(instance=admin_user)
    return render(request, 'core/partials/admin_form.html', {'form': form})
@login_required
def delete_admin(request, pk):
    admin_user = get_object_or_404(User, pk=pk)
    if request.user.pk == admin_user.pk:
        messages.error(request, "You cannot delete your own account.")
        return render(request, 'core/partials/admins_list.html', {'admins': User.objects.filter(is_staff=True)})
    if request.method == 'POST':
        admin_user.delete(); return render(request, 'core/partials/admins_list.html', {'admins': User.objects.filter(is_staff=True)})
    return render(request, 'core/partials/admin_delete_confirm.html', {'admin_user': admin_user})

# --- CONTACT MESSAGES ---
@login_required
def delete_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete(); return render(request, 'core/partials/messages_list.html', {'messages': ContactMessage.objects.all()})
    return render(request, 'core/partials/message_delete_confirm.html', {'message': message})