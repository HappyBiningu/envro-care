# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from ..models import Notification
# from ..serializers.notifications import NotificationSerializer
# from configs.rest_framework_configs import CustomPagination


# class NotificationViewSet(ModelViewSet):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]
#     filterset_fields = ["user", "seen"]
#     pagination_class = CustomPagination