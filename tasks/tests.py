from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from project.models import Project, ProjectMember

from .models import Task
from .pagination import StandardResultPagination


class TaskAPITests(APITestCase):

    def setUp(self):
        # Users
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@test.com",
            password="password123"
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password123"
        )

        self.member = User.objects.create_user(
            username="member",
            email="member@test.com",
            password="password123"
        )

        self.assigned_user = User.objects.create_user(
            username="assigned",
            email="assigned@test.com",
            password="password123"
        )

        self.non_member = User.objects.create_user(
            username="nonmember",
            email="nonmember@test.com",
            password="password123"
        )

        # Project
        self.project = Project.objects.create(
            name="Test Project",
            description="Test project description",
            owner=self.owner
        )

        # Project members
        ProjectMember.objects.create(
            project=self.project,
            user=self.owner,
            role=ProjectMember.Role.OWNER
        )

        ProjectMember.objects.create(
            project=self.project,
            user=self.admin,
            role=ProjectMember.Role.ADMIN
        )

        ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role=ProjectMember.Role.MEMBER
        )

        ProjectMember.objects.create(
            project=self.project,
            user=self.assigned_user,
            role=ProjectMember.Role.MEMBER
        )

        # Task
        self.task = Task.objects.create(
            title="Test Task",
            description="Test task description",
            project=self.project,
            created_by=self.owner,
            assigned_to=self.assigned_user,
            status=Task.Status.TODO,
            priority=Task.Priority.MEDIUM,
            due_date=timezone.now() + timedelta(days=7)
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

    # ---------------------------------------------------------
    # TASK LIST
    # ---------------------------------------------------------

    def test_unauthenticated_user_cannot_list_tasks(self):
        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_project_member_can_list_tasks(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_non_member_cannot_see_project_tasks(self):
        self.authenticate(self.non_member)

        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"Message": "No Tasks Found"}
        )

    # ---------------------------------------------------------
    # TASK CREATION
    # ---------------------------------------------------------

    def test_project_member_can_create_task(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        data = {
            "title": "New Task",
            "description": "New task description",
            "project": self.project.id,
            "priority": Task.Priority.HIGH,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)

        task = Task.objects.get(title="New Task")

        self.assertEqual(task.project, self.project)
        self.assertEqual(task.created_by, self.member)
        self.assertEqual(task.status, Task.Status.TODO)

    def test_non_member_cannot_create_task(self):
        self.authenticate(self.non_member)

        url = reverse("task-list")

        data = {
            "title": "Unauthorized Task",
            "description": "Should not be created",
            "project": self.project.id,
            "priority": Task.Priority.HIGH,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 403)

    def test_task_can_be_created_without_assigned_user(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        data = {
            "title": "Unassigned Task",
            "description": "No user assigned",
            "project": self.project.id,
            "assigned_to": None,
            "priority": Task.Priority.LOW,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)

        task = Task.objects.get(title="Unassigned Task")

        self.assertIsNone(task.assigned_to)

    def test_task_cannot_be_assigned_to_non_member(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        data = {
            "title": "Invalid Assigned Task",
            "description": "Assigned to non-member",
            "project": self.project.id,
            "assigned_to": self.non_member.id,
            "priority": Task.Priority.MEDIUM,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 403)

    def test_task_gets_todo_status_on_creation(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        data = {
            "title": "Todo Task",
            "description": "Testing default status",
            "project": self.project.id,
            "priority": Task.Priority.LOW,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)

        task = Task.objects.get(title="Todo Task")

        self.assertEqual(task.status, Task.Status.TODO)

    # ---------------------------------------------------------
    # SPECIFIC TASK
    # ---------------------------------------------------------

    def test_project_member_can_view_specific_task(self):
        self.authenticate(self.member)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.task.id)

    def test_non_member_cannot_view_specific_task(self):
        self.authenticate(self.non_member)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_specific_task_returns_404_for_invalid_id(self):
        self.authenticate(self.member)

        url = reverse(
            "specific-task",
            kwargs={"id": 999999}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # PUT
    # ---------------------------------------------------------

    def test_task_creator_can_put_task(self):
        self.authenticate(self.owner)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "assigned_to": self.member.id,
            "priority": Task.Priority.HIGH,
            "due_date": (
                timezone.now() + timedelta(days=10)
            ).isoformat(),
            "status": Task.Status.IN_PROGRESS
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(
            self.task.status,
            Task.Status.IN_PROGRESS
        )

    def test_non_creator_cannot_put_task(self):
        self.authenticate(self.member)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        data = {
            "title": "Unauthorized Update",
            "description": "Should fail",
            "assigned_to": self.member.id,
            "priority": Task.Priority.HIGH,
            "due_date": (
                timezone.now() + timedelta(days=10)
            ).isoformat(),
            "status": Task.Status.COMPLETED
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # PATCH
    # ---------------------------------------------------------

    def test_task_creator_can_patch_task(self):
        self.authenticate(self.owner)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        data = {
            "status": Task.Status.COMPLETED
        }

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            Task.Status.COMPLETED
        )

    def test_assigned_user_can_patch_task(self):
        self.authenticate(self.assigned_user)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        data = {
            "status": Task.Status.IN_PROGRESS
        }

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            Task.Status.IN_PROGRESS
        )

    def test_unrelated_member_cannot_patch_task(self):
        self.authenticate(self.member)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        data = {
            "status": Task.Status.COMPLETED
        }

        response = self.client.patch(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def test_task_creator_can_delete_task(self):
        self.authenticate(self.owner)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_project_admin_can_delete_task(self):
        self.authenticate(self.admin)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Task.objects.filter(id=self.task.id).exists()
        )

    def test_project_owner_can_delete_task(self):
        self.authenticate(self.owner)

        task = Task.objects.create(
            title="Owner Delete Task",
            description="Owner deletion",
            project=self.project,
            created_by=self.member,
            assigned_to=self.assigned_user,
            status=Task.Status.TODO,
            priority=Task.Priority.LOW,
            due_date=timezone.now() + timedelta(days=5)
        )

        url = reverse(
            "specific-task",
            kwargs={"id": task.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )

    def test_regular_member_cannot_delete_task(self):
        self.authenticate(self.member)

        url = reverse(
            "specific-task",
            kwargs={"id": self.task.id}
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # PROJECT-SPECIFIC TASKS
    # ---------------------------------------------------------

    def test_project_member_can_list_project_tasks(self):
        self.authenticate(self.member)

        url = reverse(
            "project-task-list",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_project_task_cannot_be_assigned_to_non_member(self):
        self.authenticate(self.member)

        url = reverse(
            "project-task-list",
            kwargs={"id": self.project.id}
        )

        data = {
            "title": "Invalid Project Task",
            "description": "Assigned to non-member",
            "assigned_to": self.non_member.id,
            "priority": Task.Priority.MEDIUM,
            "due_date": (
                    timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_non_member_cannot_list_project_tasks(self):
        self.authenticate(self.non_member)

        url = reverse(
            "project-task-list",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_project_member_can_create_project_task(self):
        self.authenticate(self.member)

        url = reverse(
            "project-task-list",
            kwargs={"id": self.project.id}
        )

        data = {
            "title": "Project Task",
            "description": "Created through project endpoint",
            "priority": Task.Priority.MEDIUM,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        task = Task.objects.get(title="Project Task")

        self.assertEqual(task.project, self.project)
        self.assertEqual(task.created_by, self.member)
        self.assertEqual(task.status, Task.Status.TODO)

    def test_project_task_can_be_assigned_to_member(self):
        self.authenticate(self.member)

        url = reverse(
            "project-task-list",
            kwargs={"id": self.project.id}
        )

        data = {
            "title": "Assigned Project Task",
            "description": "Assigned to member",
            "assigned_to": self.assigned_user.id,
            "priority": Task.Priority.HIGH,
            "due_date": (
                timezone.now() + timedelta(days=5)
            ).isoformat()
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        task = Task.objects.get(
            title="Assigned Project Task"
        )

        self.assertEqual(
            task.assigned_to,
            self.assigned_user
        )

    # ---------------------------------------------------------
    # FILTERING / SEARCH / ORDERING
    # ---------------------------------------------------------

    def test_filter_tasks_by_status(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(
            url,
            {"status": Task.Status.TODO}
        )

        self.assertEqual(response.status_code, 200)

    def test_filter_tasks_by_priority(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(
            url,
            {"priority": Task.Priority.MEDIUM}
        )

        self.assertEqual(response.status_code, 200)

    def test_search_tasks_by_title(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(
            url,
            {"search": "Test Task"}
        )

        self.assertEqual(response.status_code, 200)

    def test_order_tasks_by_due_date(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(
            url,
            {"ordering": "due_date"}
        )

        self.assertEqual(response.status_code, 200)

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.project.name}({self.task.title})"
        )

    def test_task_list_no_tasks_found(self):
        self.authenticate(self.member)

        Task.objects.all().delete()

        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"Message": "No Tasks Found"}
        )