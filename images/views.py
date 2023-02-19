from django.http import HttpResponse
from django.shortcuts import render

from images.models import Image
from images.routes import ImageRouting
from django.contrib.auth.models import User
from users.permissions import Permissions

IMAGE_TEMPLATE = 'image.html'


def view_image(request):
    url = request.build_absolute_uri()
    image_route = ImageRouting(url)

    user = User.objects.filter(username=image_route.context['username']).first()
    if user is None:
        return HttpResponse('User is not found', status=404)

    if image_route.is_expiring():
        if Permissions.EXPIRING_IMAGE_PERMISSION_CODENAME in user.get_all_permissions():
            pass  # TODO: Make a render
        return HttpResponse(status=403)

    image = Image.objects.filter(uuid=image_route.context['uuid']).first()
    if image is None:
        return HttpResponse('Image not found', status=404)

    if image_route.is_thumbnail():
        size = image_route.context['size']
        if size in Permissions.iter_allowed_thumbnail_sizes(user):
            image_path = image.get_thumbnail_file_path(size)
            return render(request, IMAGE_TEMPLATE, {'image': _relative_to_static(image_path)})
        return HttpResponse('Thumbnail size not allowed', status=403)

    if image_route.is_original():
        if Permissions.has_original_image_permission(user):
            image_path = image.get_file_path()
            return render(request, IMAGE_TEMPLATE, {'image': _relative_to_static(image_path)})
        return HttpResponse('No access', status=403)


# Return directory path without first folder (static/)
def _relative_to_static(path):
    return path.relative_to(*path.parts[:1])
