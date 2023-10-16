import math
import os
from typing import no_type_check, Dict, Optional
from urllib.parse import urljoin

from tqdm import trange

from fiddler.constants import (
    CONTENT_TYPE_OCTET_STREAM_HEADER,
    MULTI_PART_CHUNK_SIZE,
    MULTI_PART_UPLOAD_SIZE_THRESHOLD,
    UploadType,
)
from fiddler.libs.http_client import RequestClient
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import APIResponseHandler

logger = get_logger(__name__)

UPLOAD_ID_KEY = 'upload_id'
UPLOAD_TYPE_KEY = 'upload_type'
RESOURCE_IDENT_KEY = 'resource_identifier'
FILE_NAME_KEY = 'file_name'
MULTIPART_UPLOAD_KEY = 'multipart_upload'
NUM_ROWS_KEY = 'num_rows'
NUM_COLS_KEY = 'num_cols'
IS_UPDATE = 'is_update'


@no_type_check
def multipart_upload(
    client: RequestClient,
    organization_name: str,
    project_name: str,
    identifier: str,
    upload_type: UploadType,
    file_path: str,
    file_name: str,
    chunk_size: Optional[int] = MULTI_PART_CHUNK_SIZE,  # bytes
) -> Dict[str, str]:
    """
    Perform multipart upload for datasets/events ingestion
    """
    base_url = f'datasets/{organization_name}:{project_name}/'
    UPLOAD_INITIALIZE_URL = urljoin(base_url, 'initialize')
    UPLOAD_URL = urljoin(base_url, 'upload')
    UPLOAD_COMPLETE_URL = urljoin(base_url, 'complete')

    if not os.path.exists(file_path):
        raise ValueError(
            f'File {file_path} not found. Please check if the entered path is correct.'
        )
    file_size = os.path.getsize(file_path)

    if file_size < MULTI_PART_UPLOAD_SIZE_THRESHOLD:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            response = client.put(
                url=UPLOAD_URL,
                params={
                    UPLOAD_TYPE_KEY: upload_type,
                    MULTIPART_UPLOAD_KEY: False,
                    RESOURCE_IDENT_KEY: identifier,
                    FILE_NAME_KEY: file_name,
                },
                data=file_data,
                headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
            )
    else:
        with open(file_path, 'rb') as f:
            # from header
            num_cols = len(f.readline().split(b','))
            # from rest of the file
            num_rows = sum(1 for _ in f)

        # Step 1: Initialize upload
        response = client.post(
            url=UPLOAD_INITIALIZE_URL,
            data={
                RESOURCE_IDENT_KEY: identifier,
                FILE_NAME_KEY: file_name,
                UPLOAD_TYPE_KEY: upload_type,
                NUM_COLS_KEY: num_cols,
                NUM_ROWS_KEY: num_rows,
            },
        )
        response_data = APIResponseHandler(response).get_data()
        upload_id = response_data.get(UPLOAD_ID_KEY)
        file_name = response_data.get(FILE_NAME_KEY)

        parts = []
        total_chunks = math.ceil(file_size / chunk_size)

        # Step 2: Chunk and upload
        logger.info('Beginning chunk upload')
        with open(file_path, 'rb') as f:
            for part_no in trange(1, total_chunks + 1, desc=file_name):
                file_data = f.read(chunk_size)
                if not file_data:
                    # continue, rather than break so that the progress bar completes.
                    # This will incur at max only one extra iteration.
                    continue
                response = client.put(
                    url=UPLOAD_URL,
                    params={
                        UPLOAD_TYPE_KEY: upload_type,
                        MULTIPART_UPLOAD_KEY: True,
                        RESOURCE_IDENT_KEY: identifier,
                        FILE_NAME_KEY: file_name,
                        UPLOAD_ID_KEY: upload_id,
                        'part_number': part_no,
                    },
                    data=file_data,
                    headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
                )
                resp_data = APIResponseHandler(response).get_data()
                parts.append(
                    {
                        'ETag': resp_data.get('info').get('ETag'),
                        'PartNumber': resp_data.get('info').get('PartNumber'),
                    }
                )
                logger.info(f'Chunk uploaded: {part_no}/{total_chunks}')

        # Step 3: Complete the upload
        response = client.post(
            url=UPLOAD_COMPLETE_URL,
            params={
                UPLOAD_TYPE_KEY: upload_type,
                RESOURCE_IDENT_KEY: identifier,
                FILE_NAME_KEY: file_name,
                UPLOAD_ID_KEY: upload_id,
            },
            data={'parts': parts},
        )
    logger.info('File successfully uploaded to blob store')
    return APIResponseHandler(response).get_data()
