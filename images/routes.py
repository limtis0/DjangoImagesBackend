import re
from typing import Dict
from hexOceanBackend.settings import IMAGE_URL_BASE


class ImageRouting:
    _TYPE_ORIGINAL = 'original'
    _TYPE_THUMBNAIL = 'thumbnail'
    _TYPE_EXPIRING = 'expiring'

    """
    :var static_image_url_regex
    
    Matches URLs that look like:
    {STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/original/
    {STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/thumbnail/300
    {STATIC_URL}/userName123@.-+/iAmAShortUuid23456789A/expiring

    Captures: 
    username - group(1);
    uuid to a group(2);
    image type (original/thumbnail/expiring) - group(3);
    Thumbnail size in pixels (optional) - group(4);
    """
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
            'size': int(data.group(4)) if data.group(4).isdecimal() else 0,
        }

    def is_original(self) -> bool:
        return self.context['type'] == self._TYPE_ORIGINAL

    def is_thumbnail(self) -> bool:
        return self.context['type'] == self._TYPE_THUMBNAIL

    def is_expiring(self) -> bool:
        return self.context['type'] == self._TYPE_EXPIRING

    @classmethod
    def get_thumbnail_url(cls, username: str, uuid: str, thumbnail_size: int) -> str:
        return f'{IMAGE_URL_BASE}{username}/{uuid}/{cls._TYPE_THUMBNAIL}/{thumbnail_size}'

    @classmethod
    def get_original_media_url(cls, username: str, uuid: str) -> str:
        return f'{IMAGE_URL_BASE}{username}/{uuid}/{cls._TYPE_ORIGINAL}'

    @classmethod
    def get_expiring_media_url(cls, username: str, expiring_uuid: str):
        return f'{IMAGE_URL_BASE}{username}/{expiring_uuid}/{cls._TYPE_EXPIRING}'
