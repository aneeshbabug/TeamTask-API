from rest_framework.permissions import BasePermission
from project.models import Project, ProjectMember

class IsProjectMemberOfProject(BasePermission):

    message = "You do not have access to this project"

    def has_object_permission(self,request,view,obj):
        return Project.objects.filter(id=obj.id,projectmember__user=request.user).exists()

class IsAssignedUserProjectMember(BasePermission):

    message = "Assigned User does not have access to this project"

    def has_object_permission(self,request,view,obj):
        return Project.objects.filter(id=obj.id,projectmember__user=request.data.get('assigned_to')).exists()

class IsCreatorOfProject(BasePermission):

    message = "Only Creator of this task can access this"

    def has_object_permission(self,request,view,obj):
        return obj.created_by == request.user

class IsCreatorOrAssignedOfProject(BasePermission):

    message = "You do not have access. Only Creator or Assigned User allowed"

    def has_object_permission(self,request,view,obj):
        return (obj.created_by == request.user or obj.assigned_to == request.user)

class IsCreatorOrProjectAdmin(BasePermission):

    message = "You do not have access. Only Creator or Project Owner/Admin allowed"

    def has_object_permission(self, request, view, obj):
        return (obj.created_by == request.user or ProjectMember.objects.filter(project=obj.project,role=ProjectMember.Role.ADMIN,user=request.user).exists() or Project.objects.filter(id=obj.project.id,owner=request.user).exists())