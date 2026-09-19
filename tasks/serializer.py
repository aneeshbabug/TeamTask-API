from rest_framework import serializers
from .models import Task

class TaskAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title','description','project','assigned_to','priority','due_date']
        read_only_fields = ['project','created_by','status','assigned_to']

class TaskViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status','description','priority','due_date']

class TaskPUTSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title','description','assigned_to','priority','due_date','status']

class ProjectTaskAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title','description','assigned_to','priority','due_date']
        read_only_fields = ['project','created_by','status','assigned_to']