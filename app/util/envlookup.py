import os

DOWNLOAD_MEDIA: bool = os.environ.get(
    'DOWNLOAD_MEDIA', 'true').lower() == 'true'
FREQ_MIN: int = int(os.environ.get('FREQ_MIN', '2'))
