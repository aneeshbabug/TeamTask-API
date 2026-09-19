from rest_framework import serializers

from .models import Project, ProjectMember

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner',]

    def validate(self, attrs):
        owner = self.context['request'].user
        name = attrs.get('name')

        if Project.objects.filter(owner=owner, name=name).exists():
            raise serializers.ValidationError({
                'name': 'You already have a project with this name.'
            })

        return attrs

class ProjectMemberViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id','user','username','role']

class ProjectMemberAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectMember
        fields = ['user','role']
        read_only_field = ['project']

    def validate_role(self, value):
        if value == ProjectMember.Role.OWNER:
            raise serializers.ValidationError(
                "Cannot assign the owner role."
            )
        return value

class ProjectMemberRoleChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectMember
        fields = ['role']

    def validate_role(self, value):
        if value == ProjectMember.Role.OWNER:
            raise serializers.ValidationError(
                "Cannot change a member's role to owner."
            )
        return value
