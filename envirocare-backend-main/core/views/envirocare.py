from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.envirocare import Complaint, Comment, Task
from django.db.models import Count
from django.utils import timezone

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def task_statistics(request):
    """Get statistics about tasks by their status"""
    try:
        # Get counts for each task status
        stats = Task.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Initialize response with zero counts
        response_data = {
            'tasks_pending': 0,
            'tasks_in_progress': 0,
            'tasks_completed': 0,
            'total_tasks': 0
        }
        
        # Update counts based on the query results
        for stat in stats:
            status_key = f'tasks_{stat["status"].lower()}'
            if status_key in response_data:
                response_data[status_key] = stat['count']
        
        # Calculate total tasks
        response_data['total_tasks'] = sum(response_data.values())
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 