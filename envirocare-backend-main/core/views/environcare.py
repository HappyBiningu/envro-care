from configs.rest_framework_configs import CustomPagination
from rest_framework import viewsets, permissions
from ..models.envirocare import Organisation, Complaint, Comment, Task
from ..serializers.envirocare import OrganisationSerializer, ComplaintSerializer, CommentSerializer, TaskSerializer

class OrganisationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    model = Organisation
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    pagination_class = CustomPagination
    
class ComplaintViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    model = Complaint
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    pagination_class = CustomPagination
    
class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    
class TaskViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    filterset_fields = ['status']
    
    