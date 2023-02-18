from django.urls import path
from images import views

urlpatterns = [
    path(r'', views.API_overview, name='API Overview'),
    path(r'list/<int:page>', views.list_images, name='List images'),
]
