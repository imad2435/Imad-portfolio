# imad_portfolio/portfolio_project/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    # --- DASHBOARD & AUTH ---
    path('dashboard/', core_views.dashboard_view, name='dashboard'),
    path('dashboard/login/', core_views.custom_login_view, name='dashboard_login'),
    path('dashboard/logout/', core_views.custom_logout_view, name='dashboard_logout'),

    # --- HTMX PARTIALS (Read-only views) ---
    path('htmx/load-personal-info/', core_views.load_personal_info, name='load-personal-info'),
    path('htmx/load-skills/', core_views.load_skills, name='load-skills'),
    path('htmx/load-experiences/', core_views.load_experiences, name='load-experiences'),
    path('htmx/load-projects/', core_views.load_projects, name='load-projects'),
    path('htmx/load-messages/', core_views.load_messages, name='load-messages'),
    path('htmx/load-admins/', core_views.load_admins, name='load-admins'),
    path('htmx/check-new-messages/', core_views.check_new_messages, name='check-new-messages'),

    # --- CRUD ACTIONS ---
    path('personal-info/<int:pk>/update/', core_views.update_personal_info, name='update-personal-info'),
    path('projects/create/', core_views.create_project, name='create-project'),
    path('projects/<int:pk>/update/', core_views.update_project, name='update-project'),
    path('projects/<int:pk>/delete/', core_views.delete_project, name='delete-project'),
    path('skills/create/', core_views.create_skill, name='create-skill'),
    path('skills/<int:pk>/update/', core_views.update_skill, name='update-skill'),
    path('skills/<int:pk>/delete/', core_views.delete_skill, name='delete-skill'),
    path('experiences/create/', core_views.create_experience, name='create-experience'),
    path('experiences/<int:pk>/update/', core_views.update_experience, name='update-experience'),
    path('experiences/<int:pk>/delete/', core_views.delete_experience, name='delete-experience'),
    path('messages/<int:pk>/delete/', core_views.delete_message, name='delete-message'),
    path('admins/create/', core_views.create_admin, name='create-admin'),
    path('admins/<int:pk>/update/', core_views.update_admin, name='update-admin'),
    path('admins/<int:pk>/delete/', core_views.delete_admin, name='delete-admin'),

    # --- PUBLIC HOMEPAGE ---
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)