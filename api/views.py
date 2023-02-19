from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import ImageInputSerializer


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
        return Response(status=401)

    serializer = ImageInputSerializer(data=request.data, context={'request': request})
    return serializer.upload()


@api_view(['DELETE'])
def delete_image(request, uuid: str):
    if not request.user.is_authenticated:
        return Response(status=401)


@api_view(['GET'])
def list_images(request, page: int):
    if not request.user.is_authenticated:
        return Response(status=401)


@api_view(['GET'])
def find_images(request, name: str):
    if not request.user.is_authenticated:
        return Response(status=401)
