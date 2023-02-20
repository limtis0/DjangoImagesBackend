from django.urls import re_path
from images.routes import ImageRouting
from images.views import view_image

urlpatterns = [
    re_path(ImageRouting.static_image_url_regex_no_capture, view_image),
]
