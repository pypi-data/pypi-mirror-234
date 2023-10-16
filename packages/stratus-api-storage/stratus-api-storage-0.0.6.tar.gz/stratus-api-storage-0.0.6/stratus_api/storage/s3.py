from stratus_api.storage import STORAGE_UPLOAD_FOLDER


def get_list_of_files_by_pattern(aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str,
                                 bucket_name: str, file_pattern: str, propagate_exceptions=False) -> list:
    """
    Get list of file paths in S3 bucket that match a wildcard string
    :param aws_access_key_id: access key for your AWS account
    :param aws_secret_access_key: secret key for your AWS account
    :param aws_session_token: session token for your AWS account and this is only needed when you are using temporary
    credentials
    :param bucket_name: S3 bucket name
    :param file_pattern: file pattern (wildcard string)
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return: list of file paths in S3 bucket that match the wildcard string
    """
    from botocore.exceptions import ClientError
    from logging import getLogger
    import boto3
    import re
    logger = getLogger()
    list_of_matched_files = list()
    try:
        client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)
        pattern = re.compile(file_pattern.replace('.', '\.').replace('*', '.+'))
        contents = client.list_objects(Bucket=bucket_name)['Contents']
        list_of_matched_files = list(set([content['Key'] for content in contents if pattern.match(content['Key'])]))
    except ClientError as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception
    return list_of_matched_files


def download_remote_file(aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str, bucket_name: str,
                         remote_file_path: str, local_dir_path: str = STORAGE_UPLOAD_FOLDER,
                         propagate_exceptions=False):
    """
    Download a remote file to local path. Assumes Read access to the file
    :param aws_access_key_id: access key for your AWS account
    :param aws_secret_access_key: secret key for your AWS account
    :param aws_session_token: session token for your AWS account and this is only needed when you are using temporary
    credentials
    :param bucket_name: S3 bucket name
    :param remote_file_path: path to the file in S3 bucket to download from
    :param local_dir_path: (optional) path to the directory to download to
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return:
    """
    from botocore.exceptions import ClientError
    from logging import getLogger
    import boto3
    import os
    logger = getLogger()
    try:
        client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)
        file_name = remote_file_path.split('/')[-1]
        local_file_path = os.path.join(local_dir_path, file_name)
        client.download_file(Bucket=bucket_name, Key=remote_file_path, Filename=local_file_path)
    except ClientError as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception


def upload_local_file(aws_access_key_id: str, aws_secret_access_key: str, aws_session_token: str, bucket_name: str,
                      local_file_path: str, remote_dir_path: str = None, propagate_exceptions=False):
    """
    Upload a local file to remote path. Assumes Write access to the remote location
    :param aws_access_key_id: access key for your AWS account
    :param aws_secret_access_key: secret key for your AWS account
    :param aws_session_token: session token for your AWS account and this is only needed when you are using temporary
    credentials
    :param bucket_name: S3 bucket name
    :param remote_dir_path: path to the directory in S3 bucket to upload to
    :param local_file_path: path to the file to upload
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return:
    """
    from botocore.client import ClientError
    from logging import getLogger
    import boto3
    import os
    logger = getLogger()
    try:
        client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)
        try:
            client.head_bucket(Bucket=bucket_name)
        except ClientError:
            # The bucket does not exist
            client.create_bucket(Bucket=bucket_name)
        file_name = local_file_path.split('/')[-1]
        remote_file_path = os.path.join(remote_dir_path, file_name) if remote_dir_path else file_name
        client.upload_file(Filename=local_file_path, Bucket=bucket_name, Key=remote_file_path)
    except ClientError as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception
