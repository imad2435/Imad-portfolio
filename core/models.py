# imad/core/models.py

from django.db import models

# Model for your main personal information
class PersonalInfo(models.Model):
    name = models.CharField(max_length=100, default="Your Name")
    title = models.CharField(max_length=100, help_text="e.g., Full-Stack Developer")
    bio = models.TextField(blank=True, help_text="A short biography about yourself.")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True, help_text="Upload your CV/Resume.")
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Personal Info"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and PersonalInfo.objects.exists():
            return
        super(PersonalInfo, self).save(*args, **kwargs)

# Model for your skills
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Model for each project
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    technologies = models.ManyToManyField(Skill, related_name="projects")
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Projects with lower numbers appear first.")

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

# Model for your work or education experience
class Experience(models.Model):
    CATEGORY_CHOICES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
    ]
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='work')
    title = models.CharField(max_length=200, help_text="e.g., Software Engineer or B.S. in Computer Science")
    company = models.CharField(max_length=200, help_text="e.g., Google or University of California")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current.")
    description = models.TextField(help_text="Use bullet points or a short paragraph.")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"

# Model for contact form messages (WITH CORRECT INDENTATION)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"