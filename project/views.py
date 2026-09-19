from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Project, ProjectMember
from .serializers import ProjectCreateSerializer, ProjectSerializer, ProjectMemberViewSerializer, ProjectMemberAddSerializer, ProjectMemberRoleChangeSerializer
from .permissions import IsOwner, IsAdminOrOwner, IsProjectMemberOfProject

from accounts.models import User

# Create your views here.
class ProjectListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset = Project.objects.filter(projectmember__user=request.user)
        serializer = ProjectSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ProjectCreateSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        project = serializer.save(owner=request.user)
        ProjectMember.objects.create(project=project,user=request.user,role=ProjectMember.Role.OWNER)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT","PATCH","DELETE"]:
            return [IsOwner(),IsAuthenticated()]
        elif self.request.method == "GET":
            return [IsAuthenticated(), IsProjectMemberOfProject()]
        return super().get_permissions()

    def get(self,request,id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request,project)
        queryset = Project.objects.filter(projectmember__user=request.user, id=id)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request,project)
        serializer = ProjectCreateSerializer(project, data=request.data,partial=False,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def patch(self,request,id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request,project)
        serializer = ProjectCreateSerializer(instance=project, data=request.data,partial=True,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request, id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectMemberListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrOwner(), IsAuthenticated()]
        elif self.request.method == "GET":
            return [IsAuthenticated(), IsProjectMemberOfProject()]
        return super().get_permissions()

    def get(self,request,id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        queryset = ProjectMember.objects.filter(project=project)
        serializer = ProjectMemberViewSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        user = get_object_or_404(User, id=request.data['user'])
        if Project.objects.filter(projectmember__user=user, id=id).exists():
            return Response({'Message':'User is Already Added in the Project. So, Cannot be Added Again'},status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectMemberAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectMemberDetailView(APIView):

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsAdminOrOwner()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), IsOwner()]
        elif self.request.method == "GET":
            return [IsAuthenticated(), IsProjectMemberOfProject()]
        return super().get_permissions()

    def get(self, request, id, mem_id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        member = get_object_or_404(ProjectMember, id=mem_id, project=id)
        serializer = ProjectMemberViewSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id, mem_id):
        project = get_object_or_404(Project, id=id)
        member = get_object_or_404(ProjectMember, id=mem_id, project=id)
        self.check_object_permissions(request, project)
        if (member.role == ProjectMember.Role.OWNER and request.data.get('role') in [ProjectMember.Role.MEMBER,ProjectMember.Role.ADMIN]):
            return Response({'Message': 'Cannot Change the Owner role'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectMemberRoleChangeSerializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, id, mem_id):
        project = get_object_or_404(Project, id=id)
        member = get_object_or_404(ProjectMember, id=mem_id, project=id)
        self.check_object_permissions(request, project)
        if member.role == ProjectMember.Role.OWNER:
            return Response({'Message':'Cannot Delete the Owner'},status=status.HTTP_400_BAD_REQUEST)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



