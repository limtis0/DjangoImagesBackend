import shortuuid
from rest_framework import serializers
from rest_framework.response import Response
from images.models import Image


class ImageInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image', 'user', 'uuid']
        extra_kwargs = {
            'user': {'read_only': True},
            'uuid': {'read_only': True},
        }

    def upload(self):
        if not self.is_valid(raise_exception=True):
            return Response('Provided image can not be uploaded. Supported formats: (jpg, png)', status=401)

        self.save(
            user=self.context['request'].user,
            uuid=shortuuid.uuid()
        )

        return Response('OK', status=200)


class ImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
