from rest_framework.permissions import BasePermission
from .models import ProjectMember, Project

class IsOwner(BasePermission):

    def has_object_permission(self,request,view,obj):
        return ( obj.owner == request.user )


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        return (obj.owner == request.user or ProjectMember.objects.filter(project=obj,user=request.user,role=ProjectMember.Role.ADMIN).exists())


class IsProjectMemberOfProject(BasePermission):

    message = "You do not have access to this project"

    def has_object_permission(self,request,view,obj):
        proj_id = view.kwargs.get('id')
        return Project.objects.filter(id=proj_id,projectmember__user=request.user).exists()

