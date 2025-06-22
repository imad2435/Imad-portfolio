# imad/core/admin.py

from django.contrib import admin
from .models import PersonalInfo, Skill, Project, Experience

# This class customizes how the Project model appears in the admin panel
class ProjectAdmin(admin.ModelAdmin):
    # Columns to display in the project list view
    list_display = ('title', 'display_order', 'live_link')
    
    # Add a search bar to search by these fields
    search_fields = ('title', 'description')
    
    # Use a much nicer interface for selecting skills (many-to-many fields)
    filter_horizontal = ('technologies',)

# This class customizes the Experience model's appearance
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'start_date', 'end_date')
    list_filter = ('company', 'category') # Allow filtering by company or category

# --- Register your models with the admin site ---

# Basic registration for simple models
admin.site.register(PersonalInfo)
admin.site.register(Skill)

# Register Project and Experience with their custom admin classes
admin.site.register(Project, ProjectAdmin)
admin.site.register(Experience, ExperienceAdmin)

# Optional: Change the title of the admin page
admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to the Portfolio Management Area"
# At the top with the other imports
from .models import PersonalInfo, Skill, Project, Experience, ContactMessage

# At the bottom with the other registrations
admin.site.register(ContactMessage)