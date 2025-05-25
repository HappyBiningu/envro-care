from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views.environcare import OrganisationViewSet, ComplaintViewSet, CommentViewSet, TaskViewSet
from .views.envirocare import (task_statistics
)

router = SimpleRouter(trailing_slash=False)
router.register('organisations', OrganisationViewSet, basename='organisations')
router.register('complaints', ComplaintViewSet, basename='complaints')
router.register('comments', CommentViewSet, basename='comments')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)), 
    path('tasks/statistics/', task_statistics, name='task-statistics'),
]
