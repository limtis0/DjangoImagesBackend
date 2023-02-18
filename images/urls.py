from django.urls import path
from images import views

urlpatterns = [
    path(r'', views.API_overview, name='API Overview'),
    path(r'upload', views.upload_image, name='Upload Image'),
    path(r'delete/<str:uuid>', views.delete_image, name='Delete Image'),
    path(r'list/<int:page>', views.list_images, name='List Images'),
    path(r'find/<str:name>', views.find_images, name='Find Images'),
]
