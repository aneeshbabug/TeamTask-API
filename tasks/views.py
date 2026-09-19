from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializer import TaskAddSerializer, TaskViewSerializer, TaskPatchSerializer, TaskPUTSerializer, ProjectTaskAddSerializer
from .permissions import IsProjectMemberOfProject, IsAssignedUserProjectMember, IsCreatorOfProject, IsCreatorOrAssignedOfProject, IsCreatorOrProjectAdmin
from .pagination import StandardResultPagination

from project.models import Project
from accounts.models import User

# Create your views here.

class TaskView(APIView):

    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'created_by']
    search_fields = ['title','description']
    ordering_fields = ['due_date','created_at']

    pagination_class = StandardResultPagination

    def get(self, request):
        queryset = (
            Task.objects
            .filter(
                project__projectmember__user=request.user
            )
            .distinct()
            .order_by('-created_at')
        )

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(
                request,
                queryset,
                self
            )

        if not queryset.exists():
            return Response(
                {'Message': 'No Tasks Found'},
                status=status.HTTP_200_OK
            )

        paginator = self.pagination_class()

        paginated_queryset = paginator.paginate_queryset(
            queryset,
            request,
            self
        )

        if paginated_queryset is not None:
            serializer = TaskViewSerializer(
                paginated_queryset,
                many=True
            )

            return paginator.get_paginated_response(
                serializer.data
            )

        serializer = TaskViewSerializer(
            queryset,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self,request):
        assigned_check = IsAssignedUserProjectMember()
        projectmem_check = IsProjectMemberOfProject()
        project = get_object_or_404(Project, id=request.data.get('project'))
        if not projectmem_check.has_object_permission(request, self, project):
            raise PermissionDenied(projectmem_check.message)
        assigned_to = request.data.get('assigned_to')
        assigned_user = None
        if assigned_to not in ["null", "None", None, "none", ""]:
            assigned_user = get_object_or_404(User, id=assigned_to)
            if not assigned_check.has_object_permission(request, self, project):
                raise PermissionDenied(assigned_check.message)
        serializer = TaskAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project,assigned_to=assigned_user,created_by=request.user,status=Task.Status.TODO)
        return Response({'Message':'Task created successfully'},status=status.HTTP_201_CREATED)

class SpecificTaskView(APIView):

    permission_classes = [IsAuthenticated, IsProjectMemberOfProject]

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        project = task.project
        self.check_object_permissions(request,project)
        serializer = TaskViewSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        task = get_object_or_404(Task, id=id)
        project = task.project
        self.check_object_permissions(request,project)
        iscreator = IsCreatorOfProject()
        if not iscreator.has_object_permission(request,self,task):
            raise PermissionDenied(iscreator.message)
        serializer = TaskPUTSerializer(task, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Message': 'Task fully updated successfully'}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        task = get_object_or_404(Task, id=id)
        project = task.project
        self.check_object_permissions(request, project)
        checkuser = IsCreatorOrAssignedOfProject()
        if not checkuser.has_object_permission(request,self,task):
            raise PermissionDenied(checkuser.message)
        serializer = TaskPatchSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Message': 'Task partially updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        project = task.project
        self.check_object_permissions(request, project)
        checkuser = IsCreatorOrProjectAdmin()
        if not checkuser.has_object_permission(request,self,task):
            raise PermissionDenied(checkuser.message)
        task.delete()
        return Response({'Message': 'Task deleted successfully'}, status=status.HTTP_200_OK)

class ProjectSpecificTaskView(APIView):

    permission_classes = [IsAuthenticated,IsProjectMemberOfProject]

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        queryset = Task.objects.filter(project=project)
        serializer = TaskViewSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        self.check_object_permissions(request, project)
        assigned_check = IsAssignedUserProjectMember()
        assigned_to = request.data.get('assigned_to')
        assigned_user = None
        if assigned_to not in ["null", "None", None, "none", ""]:
            assigned_user = get_object_or_404(User, id=assigned_to)
            if not assigned_check.has_object_permission(request, self, project):
                raise PermissionDenied(assigned_check.message)
        serializer = ProjectTaskAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, assigned_to=assigned_user, created_by=request.user, status=Task.Status.TODO)
        return Response({'Message': 'Task created successfully'}, status=status.HTTP_201_CREATED)



