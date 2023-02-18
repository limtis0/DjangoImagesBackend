from rest_framework import serializers
from images.models import Image


class ImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'width', 'height']


class ImageInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title']
