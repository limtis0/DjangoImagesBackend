from typing import Dict, List
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ImageSerializer, ExpiringLinkSerializer
from hexOceanBackend.settings import DEBUG, API_URL_BASE
from users.models import TestUser
from images.models import Image, ExpiringLink
from users.permissions import Permissions

START_PAGE = 1
PAGE_SIZE = 30


class Message:
    INTERNAL_ERROR = 'Internal error'
    NOT_AUTHENTICATED = 'Not authenticated'
    INVALID_FORMAT = 'Invalid request. Supported formats: (jpg, png)'
    SUCCESS = 'Success'
    NOT_FOUND = 'Not found'
    NO_ACCESS = 'No access'


@api_view(['GET'])
def API_overview(request):
    return Response({
        'API Overview': f'GET: {API_URL_BASE}',
        'Upload Image': f'POST: {API_URL_BASE}upload',
        'Delete Image': f'DELETE: {API_URL_BASE}delete/<str:uuid>',
        'List Image': f'GET: {API_URL_BASE}list/<int:page>',
        'Find Image': f'GET: {API_URL_BASE}find/<str:title>',
        'Expiring Link': f'GET: {API_URL_BASE}expiring/<str:uuid>/<int:duration>'
    })


@api_view(['POST'])
def upload_image(request):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response(Message.NOT_AUTHENTICATED, status=401)
        request.user = TestUser()

    original_permission = Permissions.has_original_image_permission(request.user)
    serializer = ImageSerializer(data=request.data,
                                 context={'request': request, 'original_permission': original_permission})

    if not serializer.is_valid():
        return Response(Message.INVALID_FORMAT, status=400)

    serializer.save()

    return Response(serializer.data, status=200)


@api_view(['DELETE'])
def delete_image(request, uuid: str):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response(Message.NOT_AUTHENTICATED, status=401)
        request.user = TestUser()

    image = Image.objects.filter(uuid=uuid, user=request.user).first()

    if image is None:
        return Response(Message.NOT_FOUND, status=404)

    image.delete()
    return Response(Message.SUCCESS, status=200)


@api_view(['GET'])
def list_images(request, page: int):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response(Message.NOT_AUTHENTICATED, status=401)
        request.user = TestUser()

    paginator = Paginator(object_list=Image.objects.filter(user=request.user), per_page=PAGE_SIZE)
    current_page = paginator.page(max(START_PAGE, min(page, paginator.num_pages)))  # .clamp(start, end)

    data = {
        'pages':
            {
                'previous': (current_page.number - 1) if (current_page.has_previous()) else None,
                'current': current_page.number,
                'next': (current_page.number + 1) if (current_page.has_next()) else None,
            },
        'data': _get_serialized_images(current_page.object_list, request)
    }

    return Response(data, status=200)


@api_view(['GET'])
def find_images(request, title: str):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response(Message.NOT_AUTHENTICATED, status=401)
        request.user = TestUser()

    filtered = Image.objects.filter(user=request.user, title__contains=title)[:PAGE_SIZE]
    return Response(_get_serialized_images(filtered, request))


@api_view(['GET'])
def get_expiring_link(request, uuid: str, duration: int):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response(Message.NOT_AUTHENTICATED, status=401)
        request.user = TestUser()

    if not Permissions.has_expiring_image_permission(request.user):
        return Response(Message.NO_ACCESS, status=403)

    seconds = max(ExpiringLink.MIN_DURATION, min(ExpiringLink.MAX_DURATION, duration))  # .clamp(min, max)
    request.data['duration'] = seconds

    image = Image.objects.filter(user=request.user, uuid=uuid).first()
    if image is None:
        return Response(Message.NOT_FOUND, status=404)

    existing_link = ExpiringLink.objects.filter(image=image).first()

    if existing_link:
        serializer = ExpiringLinkSerializer(existing_link, data=request.data)
    else:
        serializer = ExpiringLinkSerializer(data=request.data, context={'image': image})

    if not serializer.is_valid():
        return Response(Message.INTERNAL_ERROR, status=500)

    serializer.save()

    return Response(serializer.data, status=200)


def _get_serialized_images(images, request) -> List[Dict]:
    original_permission = Permissions.has_original_image_permission(request.user)
    serialized_images = []

    for image in images:
        serializer = ImageSerializer(image,
                                     context={'original_permission': original_permission})
        serialized_images.append(serializer.data)

    return serialized_images
