from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ImageInputSerializer, ImageOutputSerializer
from hexOceanBackend.settings import DEBUG
from users.models import TestUser
from images.models import Image
from users.permissions import Permissions
from django.db.models.query import QuerySet

START_PAGE = 1
PAGE_SIZE = 30


@api_view(['GET'])
def API_overview(request):
    return Response({
        'API Overview': 'GET: /api/',
        'Upload Image': 'POST: /api/upload',
        'Delete Image': 'DELETE: /api/delete/<str:uuid>',
        'List Image': 'GET: /api/list/<int:page>',
        'Find Image': 'GET: /api/find/<str:title>',
    })


@api_view(['POST'])
def upload_image(request):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response('Not authenticated', status=401)
        request.user = TestUser.get()

    serializer = ImageInputSerializer(data=request.data, context={'request': request})
    return serializer.upload()


@api_view(['DELETE'])
def delete_image(request, uuid: str):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response('Not authenticated', status=401)
        request.user = TestUser.get()

    image = Image.objects.filter(uuid=uuid).first()

    if image is None:
        return Response('Image not found', status=404)

    if request.user != image.user:
        return Response('Forbidden', status=403)

    image.delete()
    return Response('Deleted successfully', status=200)


@api_view(['GET'])
def list_images(request, page: int):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response('You are not authenticated', status=401)
        request.user = TestUser.get()

    paginator = Paginator(object_list=Image.objects.filter(user=request.user), per_page=PAGE_SIZE)
    current_page = paginator.page(max(START_PAGE, min(page, paginator.num_pages)))  # .clamp(START_PAGE, MAX_PAGE)

    data = {
        'pages':
            {
                'previous': (current_page.number - 1) if (current_page.has_previous()) else None,
                'current': current_page.number,
                'next': (current_page.number + 1) if (current_page.has_next()) else None,
            },
        'data': _get_serialized_output(request, current_page.object_list)
    }

    return Response(data, status=200)


@api_view(['GET'])
def find_images(request, title: str):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response('You are not authenticated', status=401)
        request.user = TestUser.get()

    filtered = Image.objects.filter(user=request.user, title__contains=title)
    return Response(_get_serialized_output(request, filtered))


def _get_serialized_output(request, images: QuerySet[Image]):
    # Performance: avoiding multiple permission lookups
    original_image_permission = Permissions.has_original_image_permission(request.user)
    return ImageOutputSerializer.to_representation(images,
                                                   original_image_permission,
                                                   many=True)
