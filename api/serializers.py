from typing import Dict, List, Union

import shortuuid
from rest_framework import serializers
from rest_framework.response import Response
from images.models import Image, ExpiringLink
from django.db.models.query import QuerySet
from users.permissions import Permissions


class ImageInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']

    def upload(self):
        if not self.is_valid():
            return Response('Provided image can not be uploaded. Supported formats: (jpg, png)', status=400)

        image = self.save(user=self.context['request'].user)

        output = ImageOutputSerializer.to_representation(image, Permissions.has_original_image_permission(image.user))
        return Response(output, status=200)


class ImageOutputSerializer:
    @classmethod
    def to_representation(cls, data: Union[Image, QuerySet[Image]],
                          original_permission, many=False) -> Union[Dict, List[Dict]]:
        if many:
            return [cls._image_to_output_dict(image, original_permission) for image in data]
        return cls._image_to_output_dict(data, original_permission)

    @staticmethod
    def _image_to_output_dict(image: Image, original_permission: bool):
        data = {
            'title': image.title,
            'uuid': image.uuid,
            'thumbnails': image.get_available_thumbnails()
        }

        if original_permission:
            data['original'] = image.get_original_media_url()

        return data


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['duration']

    def to_representation(self, instance: ExpiringLink):
        return {
            'title': instance.image.title,
            'image_uuid': instance.image.uuid,
            'duration': self.validated_data['duration'],
            'valid_until': instance.valid_until,
            'url': instance.get_expiring_media_url(),
        }

    def create(self, validated_data):
        instance = ExpiringLink(**validated_data, image=self.context['image'], uuid=shortuuid.uuid())
        instance.save()
        return instance

    def update(self, instance: ExpiringLink, validated_data):
        instance.uuid = shortuuid.uuid()
        instance.save()
        return instance
