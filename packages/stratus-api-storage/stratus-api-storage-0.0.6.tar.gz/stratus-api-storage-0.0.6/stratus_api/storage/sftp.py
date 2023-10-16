from stratus_api.storage import STORAGE_UPLOAD_FOLDER
import paramiko


def connect_ssh_client_with_key(key_filename: str, hostname: str, username: str, password: str = None,
                                propagate_exceptions=False) -> paramiko.client:
    """
    connects with remote system using password if provided else key_file
    :param key_filename: path to openssh-private-key-file
    :param hostname: hostname
    :param username: username
    :param password: password
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues.
    :return: connected SSH client
    """
    from logging import getLogger
    logger = getLogger()
    max_retries = 3
    while max_retries > 0:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if not password:
                ssh.connect(key_filename=key_filename, hostname=hostname, username=username)
            else:
                ssh.connect(key_filename=key_filename, hostname=hostname, username=username, password=password)
            return ssh
        except (paramiko.SSHException, paramiko.SFTPError) as exception:
            logger.warning(exception)
            max_retries -= 1
            if max_retries == 0 and propagate_exceptions:
                raise exception
    return None


def download_remote_file(ssh: paramiko.client, remote_file_path: str, local_dir_path: str = STORAGE_UPLOAD_FOLDER,
                         propagate_exceptions=False):
    """
    Download a remote file to local path. Assumes Read access to the file
    :param ssh: connected SSH client
    :param remote_file_path: path of the remote file to download from
    :param local_dir_path: (optional) path to the directory to download to
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return:
    """
    from logging import getLogger
    import os
    logger = getLogger()
    sftp = None
    try:
        sftp = ssh.open_sftp()
        file_name = remote_file_path.split('/')[-1]
        local_file_path = os.path.join(local_dir_path, file_name)
        sftp.get(remote_file_path, local_file_path)
    except (paramiko.SSHException, paramiko.SFTPError) as exception:
        logger.warning(exception)
    finally:
        if sftp:
            sftp.close()
        ssh.close()


def create_remote_directory(sftp, remote_directory):
    """
    Creates Directories if doesn't exists
    :param sftp:
    :param remote_directory:
    :return:
    """
    import os
    if remote_directory == '/':
        return
    if remote_directory == '':
        return
    try:
        sftp.chdir(remote_directory)
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        create_remote_directory(sftp, dirname)
        sftp.mkdir(basename)
        sftp.chdir(basename)
        return True


def upload_local_file(ssh: paramiko.client, upload_dir_path: str, local_file_path: str, propagate_exceptions=False,
                      connection_close=True):
    """
    Upload a local file to remote path. Assumes Write access to the remote location
    :param ssh: connected SSH client
    :param upload_dir_path: path of the directory to upload to
    :param local_file_path: path to the file to upload
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :param connection_close:
    :return:
    """
    from logging import getLogger
    import os
    logger = getLogger()
    sftp = None
    try:
        sftp = ssh.open_sftp()
        file_name = local_file_path.split('/')[-1]
        create_remote_directory(sftp, upload_dir_path)
        remote_file_path = os.path.join(upload_dir_path, file_name)
        sftp.put(local_file_path, remote_file_path)
        return True
    except (paramiko.SSHException, paramiko.SFTPError, IOError) as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception
        return False
    finally:
        if sftp:
            sftp.close()
        if connection_close:
            ssh.close()


def get_list_of_files(ssh: paramiko.client, remote_dir_path: str, propagate_exceptions=False) -> list:
    """
    Get list of file names in a remote directory
    :param ssh: connected SSH client
    :param remote_dir_path: path of the remote directory
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return: list of file names in the remote directory
    """
    from logging import getLogger
    logger = getLogger()
    list_of_files = list()
    sftp = None
    try:
        sftp = ssh.open_sftp()
        sftp.chdir(remote_dir_path)
        for i in sftp.listdir():
            lstatout = str(sftp.lstat(i)).split()[0]
            if 'd' not in lstatout:
                list_of_files.append(i)
    except (paramiko.SSHException, paramiko.SFTPError) as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception
    finally:
        if sftp:
            sftp.close()
        ssh.close()

    return list_of_files


def get_list_of_files_by_pattern(ssh: paramiko.client, remote_dir_path: str, file_pattern: str,
                                 propagate_exceptions=False) -> list:
    """
    Get list of file names in a remote directory that match a wildcard string
    :param ssh: connected SSH client
    :param remote_dir_path: path of the remote directory
    :param file_pattern: file pattern (wildcard string)
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return: list of file names in the remote directory that match the wildcard string
    """
    from logging import getLogger
    import fnmatch
    logger = getLogger()
    list_of_files = list()
    sftp = None
    try:
        sftp = ssh.open_sftp()
        sftp.chdir(remote_dir_path)
        for i in sftp.listdir():
            if fnmatch.fnmatch(i, file_pattern):
                list_of_files.append(i)
    except (paramiko.SSHException, paramiko.SFTPError) as exception:
        logger.warning(exception)
        if propagate_exceptions:
            raise exception
    finally:
        if sftp:
            sftp.close()
        ssh.close()
    return list_of_files


def get_file_content(ssh: paramiko.client, remote_dir_path: str, file_name: str, propagate_exceptions=False):
    """
    Read file content from remote path. Assumes Read access to the remote file
    :param ssh: connected SSH client
    :param remote_dir_path: path of the directory to read
    :param file_name: file to read
    :param propagate_exceptions: (optional) backwards compatible flag to raise access permission issues
    :return:
    """
    from logging import getLogger
    logger = getLogger()
    file_content = ''
    sftp = None
    try:
        sftp = ssh.open_sftp()
        sftp.chdir(remote_dir_path)
        remote_file = sftp.open(file_name)
        file_content = remote_file.read()
        remote_file.close()
    except (paramiko.SSHException, paramiko.SFTPError) as exception:
        logger.warning(exception)
    finally:
        sftp.close()
    return file_content


def is_file_exists(ssh: paramiko.client, remote_dir_path: str, file_name: str):
    """
    check file exists in remote path.
    :param ssh:
    :param remote_dir_path:
    :param file_name:
    :return:
    """
    sftp = None
    try:
        sftp = ssh.open_sftp()
        sftp.chdir(remote_dir_path)
        sftp.stat(file_name)
        return True
    except IOError as exception:
        return False
    finally:
        if sftp:
            sftp.close()
        ssh.close()
