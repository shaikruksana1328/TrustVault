
from django.urls import path
from . import views

urlpatterns = [
    path('activity/', views.activity_logs_view, name='activity_logs'),
]
