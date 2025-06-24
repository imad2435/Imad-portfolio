# imad/core/views.py

# --- Django and Python Imports ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

# --- Local Imports: Models and Forms ---
from .models import PersonalInfo, Skill, Project, Experience, ContactMessage
from .forms import (
    ContactForm, ProjectForm, SkillForm, PersonalInfoForm, ExperienceForm,
    AdminCreationForm, AdminChangeForm
)


# ==============================================================================
#  HELPER FUNCTION FOR HTMX TRIGGERS
# ==============================================================================

def create_htmx_trigger_response(trigger_name):
    """Creates a standard HttpResponse that just triggers an HTMX event."""
    response = HttpResponse(status=204) # 204 No Content is ideal for this
    response['HX-Trigger'] = trigger_name
    return response


# ==============================================================================
#  PUBLIC-FACING VIEW
# ==============================================================================

def home(request):
    """
    Handles the public homepage and the contact form submission.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # On successful form submission, we can add a success message if needed
            messages.success(request, "Thank you for your message! I'll get back to you soon.")
            return redirect('/#contact-form')
    else:
        form = ContactForm()

    context = {
        'info': PersonalInfo.objects.first(),
        'skills': Skill.objects.all(),
        'work_experiences': Experience.objects.filter(category='work'),
        'education_experiences': Experience.objects.filter(category='education'),
        'projects': Project.objects.all(),
        'form': form,
    }
    return render(request, 'core/index.html', context)


# ==============================================================================
#  CUSTOM DASHBOARD & AUTHENTICATION VIEWS
# ==============================================================================

def custom_login_view(request):
    """
    A custom, secure login view that only allows staff members to log in.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials or not an admin user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html', {'form': AuthenticationForm()})

@login_required(login_url='/dashboard/login/')
def dashboard_view(request):
    """
    The main view for the custom dashboard. It loads the initial shell.
    """
    info = PersonalInfo.objects.first()
    # Set the timestamp for real-time message notifications
    if messages_qs := ContactMessage.objects.all():
        request.session['last_message_timestamp'] = messages_qs.first().sent_at.isoformat()
    return render(request, 'core/dashboard.html', {'info': info})

def custom_logout_view(request):
    """
    Logs the user out and redirects to the homepage.
    """
    logout(request)
    return redirect('core:home')


# ==============================================================================
#  HTMX PARTIAL VIEWS (FOR LOADING CONTENT INTO THE DASHBOARD)
# ==============================================================================

@login_required
def load_personal_info(request):
    return render(request, 'core/partials/personal_info_card.html', {'info': PersonalInfo.objects.first()})

@login_required
def load_skills(request):
    return render(request, 'core/partials/skills_list.html', {'skills': Skill.objects.all()})

@login_required
def load_experiences(request):
    context = {
        'work_experiences': Experience.objects.filter(category='work'),
        'education_experiences': Experience.objects.filter(category='education')
    }
    return render(request, 'core/partials/experiences_list.html', context)

@login_required
def load_projects(request):
    return render(request, 'core/partials/projects_table.html', {'projects': Project.objects.all()})

@login_required
def load_messages(request):
    messages_qs = ContactMessage.objects.all()
    if messages_qs:
        request.session['last_message_timestamp'] = messages_qs.first().sent_at.isoformat()
    return render(request, 'core/partials/messages_list.html', {'messages': messages_qs})

@login_required
def load_admins(request):
    # Exclude the current user from the deletable list for safety, can be handled in template
    admins = User.objects.filter(is_staff=True)
    return render(request, 'core/partials/admins_list.html', {'admins': admins})

def check_new_messages(request):
    """HTMX polling view to check for new messages and send a real-time notification."""
    last_seen_timestamp = request.session.get('last_message_timestamp')
    if not last_seen_timestamp: return HttpResponse(status=204) # No content, do nothing
    
    # Check if a newer message exists
    if ContactMessage.objects.filter(sent_at__gt=last_seen_timestamp).exists():
        response = HttpResponse(status=200) # OK
        # Trigger both a general new message alert and the specific messages list reload
        response['HX-Trigger'] = 'newMessage, messages-changed'
        return response
    
    return HttpResponse(status=204) # No content, do nothing


# ==============================================================================
#  CRUD (CREATE, UPDATE, DELETE) VIEWS
# ==============================================================================

# --- Personal Info ---
@login_required
def update_personal_info(request, pk):
    info = get_object_or_404(PersonalInfo, pk=pk)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            # For this specific view, we directly return the updated card and also trigger
            # a reload event for the nav link in dashboard.html.
            response = render(request, 'core/partials/personal_info_card.html', {'info': info})
            response['HX-Trigger'] = 'info-updated'
            return response
    else:
        form = PersonalInfoForm(instance=info)
    return render(request, 'core/partials/personal_info_form.html', {'form': form, 'info': info})

# --- Projects ---
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('projects-changed')
    else:
        form = ProjectForm()
    return render(request, 'core/partials/project_form.html', {'form': form})

@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('projects-changed')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/partials/project_form.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return create_htmx_trigger_response('projects-changed')
    return render(request, 'core/partials/project_delete_confirm.html', {'project': project})

# --- Skills ---
@login_required
def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            # On success, close the modal and trigger a refresh of the skills list
            return create_htmx_trigger_response('skills-changed')
        else: # If form is invalid, re-render the form with errors
            return render(request, 'core/partials/skill_form.html', {'form': form})
    form = SkillForm()
    return render(request, 'core/partials/skill_form.html', {'form': form})

@login_required
def update_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('skills-changed')
        else:
            return render(request, 'core/partials/skill_form.html', {'form': form, 'skill': skill})
    form = SkillForm(instance=skill)
    return render(request, 'core/partials/skill_form.html', {'form': form, 'skill': skill})

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        return create_htmx_trigger_response('skills-changed')
    return render(request, 'core/partials/skill_delete_confirm.html', {'skill': skill})

# --- Experiences ---
@login_required
def create_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('experiences-changed')
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
            return create_htmx_trigger_response('experiences-changed')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'core/partials/experience_form.html', {'form': form, 'experience': experience})

@login_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        experience.delete()
        return create_htmx_trigger_response('experiences-changed')
    return render(request, 'core/partials/experience_delete_confirm.html', {'experience': experience})

# --- Admin Users ---
@login_required
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('admins-changed')
    else:
        form = AdminCreationForm()
    return render(request, 'core/partials/admin_form.html', {'form': form})

@login_required
def update_admin(request, pk):
    admin_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminChangeForm(request.POST, instance=admin_user)
        if form.is_valid():
            form.save()
            return create_htmx_trigger_response('admins-changed')
    else:
        form = AdminChangeForm(instance=admin_user)
    return render(request, 'core/partials/admin_form.html', {'form': form, 'admin_user': admin_user})

@login_required
def delete_admin(request, pk):
    admin_user = get_object_or_404(User, pk=pk)
    if request.user.pk == admin_user.pk:
        messages.error(request, "You cannot delete your own account.")
        admins = User.objects.filter(is_staff=True)
        return render(request, 'core/partials/admins_list.html', {'admins': admins})

    if request.method == 'POST':
        admin_user.delete()
        return create_htmx_trigger_response('admins-changed')
        
    return render(request, 'core/partials/admin_delete_confirm.html', {'admin_user': admin_user})

# --- Contact Messages ---
@login_required
def delete_message(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        return create_htmx_trigger_response('messages-changed')
    return render(request, 'core/partials/message_delete_confirm.html', {'message': message})