import shortuuid
from rest_framework import serializers
from rest_framework.response import Response
from images.models import Image


class ImageInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'user', 'uuid', 'image']
        extra_kwargs = {
            'user': {'read_only': True},
            'uuid': {'read_only': True},
        }

    def upload(self):
        if not self.is_valid(raise_exception=True):
            return Response('Provided image can not be uploaded. Supported formats: (jpg, png)', status=400)

        image = self.save(
            user=self.context['request'].user,
            uuid=shortuuid.uuid()
        )

        output = ImageOutputSerializer(image, context={'api': {f'{image.uuid}': image}})
        return Response(output.data, status=200)


class ImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'uuid']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Performance: avoiding queries by using a dictionary of Images passed via context
        image = self.context['api'][data['uuid']]

        data['thumbnails'] = image.get_available_thumbnails()

        return data

    def get_image(self):
        return Image.objects.get(uuid=self.data['uuid'])
