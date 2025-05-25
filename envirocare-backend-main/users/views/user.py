from rest_framework import viewsets, permissions, views, response
from ..serializers.user import CustomUserSerializer
from ..models import CustomUser
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import JsonResponse
from configs.rest_framework_configs import CustomPagination


class CustomUserViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    model = CustomUser
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "email","is_staff"]
    http_method_names = ['get', 'post', 'patch']
    pagination_class = CustomPagination

class CustomRegisterUserViewset(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    model = CustomUser
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "email","is_staff"]
    http_method_names = ['post']
    pagination_class = CustomPagination



class GetUserData(views.APIView):
    """Gets logged in user data"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        
        data = CustomUserSerializer(user).data

        return JsonResponse(status=200, data=data)
    
# def verify_email(request):
#     user_id = request.GET.get("uid")

#     try:
#         user_qs = CustomUser.objects.filter(id=user_id)
#     except Exception as e:
#         user_qs = None
#     context = {
#         "status":True
#         }
#     if user_qs is None or user_qs.exists() is False:
#         context["status"] = False
#         context["message"] = "Failed to verify email. The user whose email you are trying to verify does not exist."
#     else:
#         user_qs.update(email_verified=True)
        
#     return TemplateResponse(request, "email_verified.html", context)

        