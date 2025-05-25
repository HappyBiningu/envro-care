from rest_framework import serializers
from ..models.envirocare import Organisation, Complaint, Comment, Task

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    
    class Meta:
        model = Complaint
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'