from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ImageInputSerializer
from hexOceanBackend.settings import DEBUG
from users.models import TestUser
from images.models import Image


@api_view(['GET'])
def API_overview(request):
    return Response({
        'API Overview': 'GET: /api/',
        'Upload image': 'POST: /api/upload',
        'Delete image': 'DELETE: /api/delete/<str:uuid>',
        'List api': 'GET: /api/list/<int:page>',
        'Find api': 'GET: /api/find/<str:name>',
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


@api_view(['GET'])
def find_images(request, name: str):
    if not request.user.is_authenticated:
        if not DEBUG:
            return Response('You are not authenticated', status=401)
        request.user = TestUser.get()
