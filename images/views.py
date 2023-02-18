from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def API_overview(request):
    return Response({
        'API Overview': 'GET: /api/',
        'Upload image': 'POST: /api/upload',
        'Delete image': 'DELETE: /api/delete/<str:uuid>',
        'List images': 'GET: /api/list/<int:page>',
        'Find images': 'GET: /api/find/<str:name>',
    })


@api_view(['POST'])
def upload_image(request):
    if not request.user.is_authenticated:
        return Response(status=401)


@api_view(['DELETE'])
def delete_image(request, uuid: str):
    if not request.user.is_authenticated:
        return Response(status=401)


@api_view(['GET'])
def list_images(request, page: int):
    if not request.user.is_authenticated:
        return Response(status=401)


@api_view(['GET'])
def find_image(request, name: str):
    if not request.user.is_authenticated:
        return Response(status=401)