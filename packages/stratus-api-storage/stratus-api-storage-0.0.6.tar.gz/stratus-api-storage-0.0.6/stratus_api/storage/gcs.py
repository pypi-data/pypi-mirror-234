client = None


def create_storage_client():
    """ Convenience function to create a storage client or pull the client from cache
    :return: an authenticated storage client
    """
    from google.cloud.storage import Client
    from stratus_api.core.settings import get_app_settings
    app_settings = get_app_settings()
    global client
    if not client:
        client = Client(project=app_settings['project_id'])
    return client


def download_from_storage(bucket_name: str, file_path: str, job_id: str = None, propagate_exceptions=True,
                          retries=3, backoff=False) -> str:
    """ Convenience function to download a file from GCS to local disk. Assumes Read access to the bucket/file
    :param bucket_name: name of GCS bucket
    :param file_path: file location within the bucket
    :param job_id: optional job_id parameter to append to the local filename
    :param propagate_exceptions:
    :param retries:
    :param backoff:
    :return: returns internal location of the file
    """
    from stratus_api.storage.utilities import manage_retries
    from stratus_api.storage import STORAGE_UPLOAD_FOLDER
    from functools import partial
    from requests import ConnectionError
    import os
    storage_client = create_storage_client()
    bucket = storage_client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(file_path)
    filename = file_path.split('/')[-1]
    if job_id:
        filename = '{0}_{1}'.format(job_id, filename)
    internal_path = os.path.join(STORAGE_UPLOAD_FOLDER, filename)
    partial_function = partial(blob.download_to_filename, filename=internal_path)
    manage_retries(partial_function=partial_function, handled_exceptions=(ConnectionError,),
                   propagate_exceptions=propagate_exceptions, retries=retries, backoff=backoff)
    return internal_path


def get_filenames_by_pattern(bucket_name, file_path, propagate_exceptions=False):
    """ Get a list of files in GCS with support for * patterns
    :param bucket_name: GCS bucket name
    :param file_path: file pattern
    :param propagate_exceptions: backwards compatible flag to raise access permission issues
    :return: list of file uris in the bucket.
    """
    from google.cloud.exceptions import Forbidden
    import re
    storage_client = create_storage_client()
    pattern = re.compile(file_path.replace('.', '\.').replace('*', '.+'))
    files = list()
    try:
        bucket = storage_client.bucket(bucket_name=bucket_name)
        blobs = bucket.list_blobs(prefix=file_path.split('*')[0])
        files = list(set([i.name for i in blobs if pattern.match(i.name)]))
    except Forbidden as exc:
        if propagate_exceptions:
            raise exc
    return files


def upload_file_to_gcs(local_path, file_path, bucket_name=None, propagate_exceptions=True, retries=3, backoff=False):
    """ Upload a local file to GCS
    :param local_path:
    :param bucket_name:
    :param file_path:
    :param propagate_exceptions:
    :param retries:
    :param backoff:
    :return:
    """
    from stratus_api.storage.utilities import manage_retries
    from functools import partial
    from requests import ConnectionError
    from stratus_api.core.settings import get_app_settings
    app_settings = get_app_settings()
    if not bucket_name:
        bucket_name = app_settings['bucket_name']
    client = create_storage_client()
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=file_path)
    partial_function = partial(blob.upload_from_filename, filename=local_path)
    manage_retries(partial_function=partial_function, handled_exceptions=(ConnectionError,),
                   propagate_exceptions=propagate_exceptions, retries=retries, backoff=backoff)
    return file_path


def delete_file_from_gcs(bucket_name, file_path, propagate_exceptions=True, retries=3, backoff=False):
    """ Delete a file from GCS
    :param bucket_name:
    :param file_path:
    :param propagate_exceptions:
    :param retries:
    :param backoff:
    :return:
    """
    from stratus_api.storage.utilities import manage_retries
    from functools import partial
    from requests import ConnectionError
    client = create_storage_client()
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=file_path)
    partial_function = partial(blob.delete)
    manage_retries(partial_function=partial_function, handled_exceptions=(ConnectionError,),
                   propagate_exceptions=propagate_exceptions, retries=retries, backoff=backoff)
    return file_path


def check_file_exist_in_gcs(bucket_name, file_path):
    client = create_storage_client()
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name=file_path)
    return blob.exists()
