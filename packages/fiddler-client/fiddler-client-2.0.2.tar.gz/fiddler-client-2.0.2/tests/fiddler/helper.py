from typing import Dict, List


def get_base_api_response_body(
    data: dict,
    created_at: str = '',
    updated_at: str = '',
):
    response = {
        'api_version': '2.0',
        'kind': 'NORMAL',
        'data': {
            'created_at': created_at,
            'updated_at': updated_at,
        },
    }
    response['data'].update(data)
    return response


def get_base_paginated_api_response_body(
    items: List[Dict],
    page_size: int = 50,
    item_count: int = 5,
    total: int = 5,
    page_count: int = 1,
    page_index: int = 1,
    offset: int = 0,
):
    return {
        'api_version': '2.0.0',
        'kind': 'PAGINATED',
        'data': {
            'page_size': page_size,
            'item_count': item_count,
            'total': total,
            'page_count': page_count,
            'page_index': page_index,
            'offset': offset,
            'items': items,
        },
    }


def get_404_error_response():
    return {
        'api_version': '2.0.0',
        'error': {
            'code': 404,
            'message': 'Object not found for the given filter',
            'errors': [
                {
                    'reason': 'ObjectNotFound',
                    'message': 'Object not found for the given filter',
                    'help': '',
                }
            ],
        },
    }


def get_ingestion_job_response(name: str, job_uuid: str = 'absdsre'):
    return {
        'data': {
            'status': 202,
            'job_uuid': job_uuid,
            'files': ['tmp401__9nq.csv'],
            'message': 'Successfully received the baseline data. Please allow time for the dataset ingestion to complete in the Fiddler platform.',
        },
        'api_version': '2.0',
        'kind': 'NORMAL',
    }
