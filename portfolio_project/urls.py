# imad/portfolio_project/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import your core views to use them for the dashboard
from core import views as core_views

# In portfolio_project/urls.py

urlpatterns = [
    # Dashboard & Login Routes
    path('dashboard/', core_views.dashboard_view, name='dashboard'),
    path('dashboard/login/', core_views.custom_login_view, name='dashboard_login'),
    path('dashboard/logout/', core_views.custom_logout_view, name='dashboard_logout'),

    # HTMX Partials
    path('htmx/load-personal-info/', core_views.load_personal_info, name='load-personal-info'),
    path('htmx/load-skills/', core_views.load_skills, name='load-skills'),
    path('htmx/load-experiences/', core_views.load_experiences, name='load-experiences'),
    path('htmx/load-projects/', core_views.load_projects, name='load-projects'),
    path('htmx/load-messages/', core_views.load_messages, name='load-messages'),
    path('htmx/check-new-messages/', core_views.check_new_messages, name='check-new-messages'),

    # Project CRUD
    path('projects/create/', core_views.create_project, name='create-project'),
    path('projects/<int:pk>/update/', core_views.update_project, name='update-project'),
    path('projects/<int:pk>/delete/', core_views.delete_project, name='delete-project'),

    # Skill CRUD
    path('skills/create/', core_views.create_skill, name='create-skill'), # <-- This line is crucial
    path('skills/<int:pk>/update/', core_views.update_skill, name='update-skill'),
    path('skills/<int:pk>/delete/', core_views.delete_skill, name='delete-skill'),

    # Personal Info CRUD
    path('personal-info/<int:pk>/update/', core_views.update_personal_info, name='update-personal-info'),

    # Public homepage
    path('', include('core.urls')),

    # 1. URLs for your new Custom Dashboard & Secure Login
    path('dashboard/', core_views.dashboard_view, name='dashboard'),
    path('dashboard/login/', core_views.custom_login_view, name='dashboard_login'),
    path('dashboard/logout/', core_views.custom_logout_view, name='dashboard_logout'),

    # 2. URLs for the HTMX partials (dynamic content loading)
    path('htmx/load-personal-info/', core_views.load_personal_info, name='load-personal-info'),
    path('htmx/load-skills/', core_views.load_skills, name='load-skills'),
    path('htmx/load-experiences/', core_views.load_experiences, name='load-experiences'),
    path('htmx/load-projects/', core_views.load_projects, name='load-projects'),
    path('htmx/load-messages/', core_views.load_messages, name='load-messages'),
    path('htmx/check-new-messages/', core_views.check_new_messages, name='check-new-messages'),

    # 3. URLs for the Project CRUD actions
    path('projects/create/', core_views.create_project, name='create-project'),
    path('projects/<int:pk>/update/', core_views.update_project, name='update-project'),
    path('projects/<int:pk>/delete/', core_views.delete_project, name='delete-project'),

    # 4. URLs for the Skill CRUD actions
    path('skills/create/', core_views.create_skill, name='create-skill'),
    path('skills/<int:pk>/update/', core_views.update_skill, name='update-skill'),
    path('skills/<int:pk>/delete/', core_views.delete_skill, name='delete-skill'),

    # 5. URL for the Personal Info CRUD action
    path('personal-info/<int:pk>/update/', core_views.update_personal_info, name='update-personal-info'),

    # 6. URL for your public-facing homepage (includes the simple core/urls.py)
    path('', include('core.urls')),
       path('experiences/create/', core_views.create_experience, name='create-experience'),
    path('experiences/<int:pk>/update/', core_views.update_experience, name='update-experience'),
    path('experiences/<int:pk>/delete/', core_views.delete_experience, name='delete-experience'),

    path('', include('core.urls')),
    # In portfolio_project/urls.py, inside urlpatterns
path('htmx/load-admins/', core_views.load_admins, name='load-admins'),
  path('messages/<int:pk>/delete/', core_views.delete_message, name='delete-message'),

    path('', include('core.urls')),
    path('admins/create/', core_views.create_admin, name='create-admin'),
    path('admins/<int:pk>/update/', core_views.update_admin, name='update-admin'),
    path('admins/<int:pk>/delete/', core_views.delete_admin, name='delete-admin'),

    path('', include('core.urls')),
]

# This is a helper for serving media files (like profile pictures) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)