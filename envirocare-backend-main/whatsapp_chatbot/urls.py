from django.urls import path
from . import views

app_name = 'whatsapp_chatbot'

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
] 