import os

DOWNLOAD_MEDIA: bool = os.environ.get(
    'DOWNLOAD_MEDIA', 'true').lower() == 'true'
