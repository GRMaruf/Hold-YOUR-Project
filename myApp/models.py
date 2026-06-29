from django.db import models
from django.contrib.auth.models import AbstractUser
from myApp.validators import *
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

class UserModel(AbstractUser):
    pass

class Project(models.Model):
    posted_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField("Project Name", max_length=50)
    short_note = models.CharField(max_length=256)
    # task_details = models.TextField(blank=True)  # use simple CK-Editor (simple but full page - heading, bold, horizontal bar, text align, list)
    task_details = CKEditor5Field(
        "Task Details",
        config_name="default",
        blank=True,
    )
    project = models.FileField(upload_to='projects/', validators=[validate_file_size,], null=True, blank=True)

    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
def delete_project(sender, instance, **kwargs):
    if instance.project:
        instance.project.delete(save=False)