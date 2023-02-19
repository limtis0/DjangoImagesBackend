from django.http import HttpResponse
from django.shortcuts import render
from images.routes import ImageRouting
from users.permissions import Permissions

IMAGE_TEMPLATE = 'image.html'


def view_image(request):
    url = request.build_absolute_uri()
    image_route = ImageRouting(url)

    user = image_route.get_user()
    if user is None:
        return HttpResponse('User is not found', status=404)

    image = image_route.get_image()
    if image is None:
        return HttpResponse('Image is not found', status=404)

    if image_route.is_thumbnail():
        size = image_route.get_thumbnail_size()
        if size in Permissions.iter_allowed_thumbnail_sizes(user):
            pass  # TODO: Make a render
        return HttpResponse('Thumbnail size is not allowed', status=403)

    if image_route.is_original():
        if Permissions.ORIGINAL_IMAGE_PERMISSION_CODENAME in user.get_all_permissions():
            return render(request, IMAGE_TEMPLATE, {'image': image.get_file_path()})
        return HttpResponse('Access to original image is not allowed')

    if image_route.is_expiring():
        if Permissions.EXPIRING_IMAGE_PERMISSION_CODENAME in user.get_all_permissions():
            pass  # TODO: Make a render
        return HttpResponse(status=403)
