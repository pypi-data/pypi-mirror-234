import enum

DATASET_FIDDLER_ID = '__fiddler_id'
ONE_LINE_PRINT = '¡í€'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
TIMESTAMP_FORMAT_2 = 'ISO8601'

# Headers
CONTENT_TYPE_HEADER_KEY = 'Content-Type'
CONTENT_TYPE_OCTET_STREAM = 'application/octet-stream'
CONTENT_TYPE_OCTET_STREAM_HEADER = {CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_OCTET_STREAM}

# Multi-part upload
MULTI_PART_UPLOAD_SIZE_THRESHOLD = 5 * 1024 * 1024  # 5MB in bytes
MULTI_PART_CHUNK_SIZE = 100 * 1024 * 1024  # 100MB in bytes

# File processor
SUPPORTABLE_FILE_EXTENSIONS = ['.csv']
CSV_EXTENSION = 'csv'

# Version
CURRENT_API_VERSION = 'v2'
MIN_SERVER_VERSION = '23.4.0'

COMPAT_MAPPING = {
    'project_id': 'project_name',
    'model_id': 'model_name',
    'dataset_id': 'dataset_name',
    'baseline_id': 'baseline_name',
    'alert_id': 'alert_name',
    'update_event': 'is_update',
}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@enum.unique
class FiddlerTimestamp(str, enum.Enum):
    """Supported timestamp formats for events published to Fiddler"""

    EPOCH_MILLISECONDS = 'epoch milliseconds'
    EPOCH_SECONDS = 'epoch seconds'
    ISO_8601 = '%Y-%m-%d %H:%M:%S.%f'
    TIMEZONE = ISO_8601 + '%Z %z'
    INFER = 'infer'


@enum.unique
class FileType(str, enum.Enum):
    """Supported file types for ingestion"""

    CSV = '.csv'
    PARQUET = '.parquet'


@enum.unique
class ServerDeploymentMode(str, enum.Enum):
    F1 = 'f1'
    F2 = 'f2'


@enum.unique
class UploadType(str, enum.Enum):
    """To distinguish between dataset ingestion and event ingestion.
    Supposed to be only internally used.
    """

    DATASET = 'dataset'
    EVENT = 'event'


FIDDLER_CLIENT_VERSION_HEADER = 'X-Fiddler-Client-Version'
