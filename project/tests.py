from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Project, ProjectMember

from tasks.models import Task
from project.serializers import ProjectMemberRoleChangeSerializer
from project.models import ProjectMember


User = get_user_model()


class ProjectTests(APITestCase):

    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="OwnerPassword123"
        )

        self.member = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="MemberPassword123"
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="AdminPassword123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="OtherPassword123"
        )

        # Create project
        self.project = Project.objects.create(
            name="Test Project",
            description="Test project description",
            owner=self.owner
        )

        # Create project members
        self.owner_membership = ProjectMember.objects.create(
            project=self.project,
            user=self.owner,
            role=ProjectMember.Role.OWNER
        )

        self.member_membership = ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role=ProjectMember.Role.MEMBER
        )

        self.admin_membership = ProjectMember.objects.create(
            project=self.project,
            user=self.admin,
            role=ProjectMember.Role.ADMIN
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

    # ---------------------------------------------------------
    # PROJECT LIST
    # ---------------------------------------------------------

    def test_unauthenticated_user_cannot_access_projects(self):
        url = reverse("project-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_list_projects(self):
        self.authenticate(self.owner)

        url = reverse("project-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Project")

    # ---------------------------------------------------------
    # PROJECT CREATE
    # ---------------------------------------------------------

    def test_owner_can_create_project(self):
        self.authenticate(self.owner)

        url = reverse("project-list")

        data = {
            "name": "New Project",
            "description": "New project description"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Project.objects.filter(
                name="New Project",
                owner=self.owner
            ).exists()
        )

    def test_project_creator_is_automatically_owner(self):
        self.authenticate(self.owner)

        url = reverse("project-list")

        data = {
            "name": "Owner Project",
            "description": "Project created by owner"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        project = Project.objects.get(name="Owner Project")

        membership = ProjectMember.objects.get(
            project=project,
            user=self.owner
        )

        self.assertEqual(
            membership.role,
            ProjectMember.Role.OWNER
        )

    def test_same_owner_cannot_create_duplicate_project_name(self):
        self.authenticate(self.owner)

        url = reverse("project-list")

        data = {
            "name": "Test Project",
            "description": "Duplicate project"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_different_owner_can_create_same_project_name(self):
        self.authenticate(self.other_user)

        url = reverse("project-list")

        data = {
            "name": "Test Project",
            "description": "Same name but different owner"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    # ---------------------------------------------------------
    # PROJECT DETAIL
    # ---------------------------------------------------------

    def test_project_member_can_view_project(self):
        self.authenticate(self.member)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data[0]["name"],
            "Test Project"
        )

    def test_non_member_cannot_view_project(self):
        self.authenticate(self.other_user)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_project_owner_can_update_project(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        data = {
            "name": "Updated Project",
            "description": "Updated description"
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.name,
            "Updated Project"
        )

    def test_project_member_cannot_update_project(self):
        self.authenticate(self.member)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        data = {
            "name": "Hacked Project"
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_project_owner_can_delete_project(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Project.objects.filter(id=self.project.id).exists()
        )

    def test_project_member_cannot_delete_project(self):
        self.authenticate(self.member)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # ---------------------------------------------------------
    # PROJECT MEMBERS - LIST
    # ---------------------------------------------------------

    def test_project_member_can_view_members(self):
        self.authenticate(self.member)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            3
        )

    def test_non_member_cannot_view_project_members(self):
        self.authenticate(self.other_user)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # ---------------------------------------------------------
    # ADD MEMBERS
    # ---------------------------------------------------------

    def test_owner_can_add_member(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        data = {
            "user": self.other_user.id,
            "role": ProjectMember.Role.MEMBER
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            ProjectMember.objects.filter(
                project=self.project,
                user=self.other_user
            ).exists()
        )

    def test_admin_can_add_member(self):
        self.authenticate(self.admin)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        data = {
            "user": self.other_user.id,
            "role": ProjectMember.Role.MEMBER
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_regular_member_cannot_add_member(self):
        self.authenticate(self.member)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        data = {
            "user": self.other_user.id,
            "role": ProjectMember.Role.MEMBER
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_cannot_add_existing_member_again(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        data = {
            "user": self.member.id,
            "role": ProjectMember.Role.MEMBER
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cannot_assign_owner_role_to_new_member(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        data = {
            "user": self.other_user.id,
            "role": ProjectMember.Role.OWNER
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    # ---------------------------------------------------------
    # MEMBER DETAIL
    # ---------------------------------------------------------

    def test_project_member_can_view_member_detail(self):
        self.authenticate(self.member)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.member_membership.id
            }
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "member"
        )

    def test_admin_can_change_member_role(self):
        self.authenticate(self.admin)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.member_membership.id
            }
        )

        data = {
            "role": ProjectMember.Role.ADMIN
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.member_membership.refresh_from_db()

        self.assertEqual(
            self.member_membership.role,
            ProjectMember.Role.ADMIN
        )

    def test_regular_member_cannot_change_member_role(self):
        self.authenticate(self.member)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.member_membership.id
            }
        )

        data = {
            "role": ProjectMember.Role.ADMIN
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_cannot_change_owner_role(self):
        self.authenticate(self.admin)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.owner_membership.id
            }
        )

        data = {
            "role": ProjectMember.Role.ADMIN
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    # ---------------------------------------------------------
    # DELETE MEMBER
    # ---------------------------------------------------------

    def test_owner_can_delete_member(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.member_membership.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            ProjectMember.objects.filter(
                id=self.member_membership.id
            ).exists()
        )

    def test_admin_cannot_delete_member(self):
        self.authenticate(self.admin)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.member_membership.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_cannot_delete_project_owner(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.owner_membership.id
            }
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_project_member_get_tasks_when_no_tasks_exist(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_project_owner_can_put_project(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-detail",
            kwargs={"id": self.project.id}
        )

        data = {
            "name": "Fully Updated Project",
            "description": "Fully updated description"
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.name,
            "Fully Updated Project"
        )

        self.assertEqual(
            self.project.description,
            "Fully updated description"
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_member_str(self):
        self.assertEqual(
            str(self.member_membership),
            "Test Project(member)"
        )

    def test_project_member_role_change_serializer_valid_role(self):
        serializer = ProjectMemberRoleChangeSerializer(
            data={"role": ProjectMember.Role.ADMIN}
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["role"],
            ProjectMember.Role.ADMIN
        )

    def test_project_member_get_project_detail(self):
        self.authenticate(self.member)

        url = reverse("project-detail", kwargs={"id": self.project.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.project.name)

    def test_add_existing_project_member(self):
        self.authenticate(self.owner)

        url = reverse(
            "project-members",
            kwargs={"id": self.project.id}
        )

        response = self.client.post(
            url,
            {
                "user": self.member.id,
                "role": ProjectMember.Role.MEMBER
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["Message"],
            "User is Already Added in the Project. So, Cannot be Added Again"
        )

    def test_cannot_change_owner_role(self):
        self.authenticate(self.admin)

        url = reverse(
            "project-member-detail",
            kwargs={
                "id": self.project.id,
                "mem_id": self.owner_membership.id
            }
        )

        response = self.client.patch(
            url,
            {"role": ProjectMember.Role.ADMIN},
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["Message"],
            "Cannot Change the Owner role"
        )

    def test_project_member_role_change_serializer_valid_role(self):
        serializer = ProjectMemberRoleChangeSerializer(
            data={"role": ProjectMember.Role.ADMIN}
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["role"],
            ProjectMember.Role.ADMIN
        )