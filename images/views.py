from django.http import HttpResponse
from django.shortcuts import render

from images.models import Image, ExpiringLink
from images.routes import ImageRouting
from django.contrib.auth.models import User
from users.permissions import Permissions
from pathlib import Path
from hexOceanBackend.settings import STATIC_URL

IMAGE_TEMPLATE = 'image.html'


def view_image(request):
    url = request.build_absolute_uri()
    image_routing = ImageRouting(url)

    user = User.objects.filter(username=image_routing.context['username']).first()
    if user is None:
        return HttpResponse('User not found', status=404)

    if image_routing.is_expiring():
        return _resolve_expiring(user, image_routing, request)

    image = Image.objects.filter(uuid=image_routing.context['uuid']).first()
    if image is None:
        return HttpResponse('Image not found', status=404)

    if image_routing.is_thumbnail():
        return _resolve_thumbnail(user, image_routing, image, request)

    if image_routing.is_original():
        return _resolve_original(user, image, request)


def _render_image(request, image_path):
    return render(request, IMAGE_TEMPLATE, {'image': _relative_to_static(image_path)})


# Return directory path without first folder (static/)
def _relative_to_static(path: Path):
    first_dir = path.parts[0]
    if first_dir in STATIC_URL:
        return path.relative_to(first_dir)
    return path


def _resolve_expiring(user: User, image_routing: ImageRouting, request):
    if not Permissions.has_expiring_image_permission(user):
        return HttpResponse('No access', status=403)

    expiring_link = ExpiringLink.objects.filter(uuid=image_routing.context['uuid']).first()
    if expiring_link is None:
        return HttpResponse('Image not found (NoObjCreated)', status=404)

    if not expiring_link.is_valid():
        expiring_link.delete()
        return HttpResponse('Image not found (invalid)', status=404)

    image_path = expiring_link.image.get_file_path()
    return _render_image(request, image_path)


def _resolve_thumbnail(user: User, image_routing: ImageRouting, image: Image, request):
    size = image_routing.context['size']
    if size in Permissions.iter_allowed_thumbnail_sizes(user):
        image_path = image.get_thumbnail_file_path(size)
        return render(request, IMAGE_TEMPLATE, {'image': _relative_to_static(image_path)})
    return HttpResponse('Size not allowed', status=403)


def _resolve_original(user: User, image: Image, request):
    if Permissions.has_original_image_permission(user):
        image_path = image.get_file_path()
        return render(request, IMAGE_TEMPLATE, {'image': _relative_to_static(image_path)})
    return HttpResponse('No access', status=403)
