import os

DOWNLOAD_MEDIA: bool = os.environ.get(
    'DOWNLOAD_MEDIA', 'true').lower() == 'true'
FREQ_MIN: int = int(os.environ.get('FREQ_MIN', '2'))
MIN_WORD_LENGTH: int = int(os.environ.get('MIN_WORD_LENGTH', '1'))
REQUIRES_DEFINITION: bool = os.environ.get(
    'REQUIRES_DEFINITION', 'true').lower() == 'true'
