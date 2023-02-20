import shortuuid
from rest_framework import serializers
from images.models import Image, ExpiringLink


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']

    def to_representation(self, instance: Image):
        data = {
            'title': instance.title,
            'uuid': instance.uuid,
            'thumbnails': instance.get_available_thumbnails()
        }
        if self.context['original_permission']:
            data['original'] = instance.get_original_media_url()

        return data

    def create(self, validated_data):
        instance = Image.objects.create(title=validated_data['title'],
                                        image=validated_data['image'],
                                        user=self.context['request'].user)
        return instance


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['duration']

    def to_representation(self, instance: ExpiringLink):
        return {
            'title': instance.image.title,
            'image_uuid': instance.image.uuid,
            'duration': instance.duration,
            'valid_until': instance.valid_until,
            'url': instance.get_expiring_media_url(),
        }

    def create(self, validated_data):
        instance = ExpiringLink.objects.create(**validated_data,
                                               image=self.context['image'],
                                               uuid=shortuuid.uuid())
        return instance

    def update(self, instance: ExpiringLink, validated_data):
        instance.duration = validated_data['duration']
        instance.uuid = shortuuid.uuid()
        instance.save()
        return instance
