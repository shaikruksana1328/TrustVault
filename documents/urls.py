
from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list_view, name='document_list'),

    path('shared/', views.shared_documents_view, name='shared_documents'),

    path('access-management/', views.access_management_view, name='access_management'),

    path('upload/', views.upload_document_view, name='upload_document'),

    path(
        '<int:document_id>/download/',
        views.download_document_view,
        name='download_document'
    ),

    path(
        '<int:document_id>/share/',
        views.share_document_view,
        name='share_document'
    ),

    path(
        '<int:document_id>/revoke/<int:permission_id>/',
        views.revoke_permission_view,
        name='revoke_permission'
    ),

    path(
        '<int:document_id>/edit/',
        views.edit_document_view,
        name='edit_document'
    ),

    path(
        '<int:document_id>/delete/',
        views.delete_document_view,
        name='delete_document'
    ),
]
