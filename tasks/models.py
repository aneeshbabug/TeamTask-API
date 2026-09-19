from django.db import models
from project.models import Project
from accounts.models import User

# Create your models here.
class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'TODO','Todo'
        IN_PROGRESS = 'IN_PROGRESS','In_Progress'
        COMPLETED = 'COMPLETED','Completed'

    class Priority(models.TextChoices):
        LOW = 'LOW','Low'
        MEDIUM = 'MEDIUM','Medium'
        HIGH = 'HIGH','High'

    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_by")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,default=None,null=True,blank=True,related_name="assigned_to")
    status = models.CharField(max_length=20,choices=Status.choices,null=False,blank=False)
    priority = models.CharField(max_length=10,choices=Priority.choices,null=False,blank=False)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name}({self.title})"


