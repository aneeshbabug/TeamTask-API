from django.db import models
from accounts.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_project_per_owner"
            )
        ]

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    project =  models.ForeignKey(Project,on_delete=models.CASCADE)
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=10,choices=Role.choices,default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=["project","user"],
            name="unique_project_member"
         )
        ]

    def __str__(self):
        return f"{self.project.name}({self.user.username})"