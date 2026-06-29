### Learning Outcomes

 - Activate Navbar Tabs
 - Using Natural Time in Templates
 - Calculate Length and Pluralize it in Templates
 - Implementing CKEditor Attach to a Form
 - Use Signals To Avoid Orphanated Media Files

# Activate Navbar Tabs
```css
{% url 'my_projects' as my_projects_url %}

<li class="nav-item">
    <a class="nav-link {% if request.path == my_projects_url %}active{% endif %}"
       href="{{ my_projects_url }}">
        Projects
    </a>
</li>
```
Alternative (Better):
```css
<li class="nav-item">
    <a class="nav-link {% if request.resolver_match.url_name == 'my_projects' %}active{% endif %}"
       href="{% url 'my_projects' %}">
        Projects
    </a>
</li>
```

# Using Natural Time in Templates
```css
{% load humanize %}
<div class="small text-secondary mb-4">
  <i class="bi bi-clock-history"></i>
  {{ x.updated_at|naturaltime }}
</div>
```
```python
INSTALLED_APPS = [
    ...
    "django.contrib.humanize",
]
```
Output =  "4 seconds ago"

# Calculate Length and Pluralize it in Templates
```css
<span class="badge bg-success fs-6">
    {{ projects|length }} Project{{ projects|pluralize }}
</span>
```

# Implementing CKEditor Attach to a Form
**Install**
```bash
pip install django-ckeditor-5
```
**Configure settings.py**
```python
INSTALLED_APPS = [
    ...
    "django_ckeditor_5",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "outdent",
            "indent",
            "|",
            "link",
            "codeBlock", # else "blockQuote" for quotetions
            "insertTable",
            "horizontalLine",
            "|",
            "alignment",
            "|",
            "undo",
            "redo",
        ]
    }
}
```
**Add URLs in Project Folder**
```python
from django.urls import path, include

urlpatterns = [
    ...
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]
```
**Configure models.py**
```python
from django_ckeditor_5.fields import CKEditor5Field

task_details = CKEditor5Field(
    "Task Details",
    config_name="default",
    blank=True,
)
```
**You Can Only Add New Class, But Can Not Replace It.**
```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("posted_by",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()
```
**But,** you must include {{ form.media }} before or after the form:
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}

    {{ form.media }}

    {{ form.as_p }}

    <button type="submit" class="btn btn-success">
        Save
    </button>
</form>
```

## Use Signals To Avoid Orphanated Media Files
Use **pre-save** and **post-delete** signals
```python
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Project


@receiver(pre_save, sender=Project)
def delete_old_project_file(sender, instance, **kwargs):
    if not instance.pk:
        # New object, nothing to delete
        return

    try:
        old_instance = Project.objects.get(pk=instance.pk)
    except Project.DoesNotExist:
        return

    old_file = old_instance.project
    new_file = instance.project

    # File replaced or cleared
    if (
        old_file
        and old_file != new_file
        and not Project.objects.filter(project=old_file.name).exclude(pk=instance.pk).exists()
    ):
        old_file.delete(save=False)


@receiver(post_delete, sender=Project)
def delete_project_file(sender, instance, **kwargs):
    if instance.project:
        instance.project.delete(save=False)
```
