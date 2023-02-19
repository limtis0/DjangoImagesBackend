import re
from typing import Dict
from images.models import Image
from django.contrib.auth.models import User

"""
Matches links that look like:
{STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/original/
{STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/thumbnail/300
{STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/expiring

Captures: 
Username to a group(1);
uuid to a group(2);
Image type to a group(3);
Additional numeric value (thumbnail size in pixels) to a group(4);
"""


class ImageRouting:
    _TYPE_ORIGINAL = 'original'
    _TYPE_THUMBNAIL = 'thumbnail'
    _TYPE_EXPIRING = 'expiring'

    _username_regex = r'[a-zA-Z0-9_@+.-]{1,150}'
    _uuid_regex = r'[2-9A-HJ-NP-Za-km-z]{22}'
    _image_type_regex = '|'.join([_TYPE_ORIGINAL, _TYPE_THUMBNAIL, _TYPE_EXPIRING])
    _thumbnail_size_regex = r'\d*'

    static_image_url_regex_no_capture = \
        rf'{_username_regex}/{_uuid_regex}/(?:{_image_type_regex})/?{_thumbnail_size_regex}'

    static_image_url_regex = \
        rf'({_username_regex})/({_uuid_regex})/({_image_type_regex})/?({_thumbnail_size_regex})'

    STATIC_IMAGE_URL_REGEX_COMPILED = re.compile(static_image_url_regex)

    def __init__(self, url):
        self.context = self._get_static_image_context_from_url(url)

    def _get_static_image_context_from_url(self, url: str) -> Dict[str, str]:
        data = self.STATIC_IMAGE_URL_REGEX_COMPILED.search(url)
        return {
            'username': data.group(1),
            'uuid': data.group(2),
            'type': data.group(3),
            'size': data.group(4),
        }

    def get_user(self) -> User:
        return User.objects.get(username=self.context['username'])

    def get_image(self) -> Image:
        return Image.objects.get(uuid=self.context['uuid'])

    def get_thumbnail_size(self) -> int:
        return int(self.context['size'])

    def is_original(self) -> bool:
        return self.context['type'] == self._TYPE_ORIGINAL

    def is_thumbnail(self) -> bool:
        return self.context['type'] == self._TYPE_THUMBNAIL

    def is_expiring(self) -> bool:
        return self.context['type'] == self._TYPE_EXPIRING
