# -*- coding:UTF-8 -*-

import paramiko
import creditutils.file_util as file_util
import os
import stat
import shutil

SUCCESS = 1
FAILED = -1

def sftp_connect(host, port, username, password):
    print('begin sftp connecting.')
    result_arr = [SUCCESS, '']
    try:
        handle = paramiko.Transport((host, int(port)))
        handle.connect(username=username, password=password)
        sftp_cli = paramiko.SFTPClient.from_transport(handle)
        result_arr = [SUCCESS, 'connect success', sftp_cli]
    except Exception as e:
        result_arr = [FAILED, 'connect failed, reason: {}'.format(e)]

    return result_arr


def sftp_upload(sftp_cli, sftp_path, local_path, only_first_step=True):
    handle_result = [SUCCESS, '']
    try:
        sftp_path = file_util.normal_unix_path(sftp_path)
        local_path = file_util.normalpath(local_path)

        if os.path.isdir(local_path):
            rs = sftp_upload_dir(sftp_cli, sftp_path, local_path, only_first_step=only_first_step)
        else:
            rs = sftp_upload_file(sftp_cli, sftp_path, local_path)

        if rs[0] == FAILED:
            handle_result[0] = FAILED
        handle_result[1] = handle_result[1] + rs[1]
    except Exception as e:
        handle_result = [FAILED, 'upload failed, reason:{}!'.format(e)]

    return handle_result

# 支持只上传根目录文件，或迭代上传所有子目录文件
def sftp_upload_dir(sftp_cli, sftp_dir_path, local_dir_path, only_first_step=True):
    handle_result = [SUCCESS, '']

    try:
        is_completed = False
        is_failed = False
        for root, _, files in os.walk(local_dir_path):
            if root == local_dir_path:
                target_sftp_dir = sftp_dir_path
                if only_first_step:
                    is_completed = True
            else:
                relative_path = root[len(local_dir_path):]
                target_sftp_dir = file_util.normal_unix_path(file_util.join_unix_path(sftp_dir_path, relative_path))

            if len(files) > 0:
                for filename in files:
                    local_file_path = os.path.join(root, filename)
                    rs = sftp_upload_file(sftp_cli, target_sftp_dir, local_file_path)
                    if handle_result[1]:
                        handle_result[1] = handle_result[1] + '\n' + rs[1]
                    else:
                        handle_result[1] = rs[1]

                    if rs[0] == FAILED:
                        handle_result[0] = FAILED
                        is_failed = True
                        break
            
            if is_completed or is_failed:
                break
    except Exception as e:
        handle_result = [FAILED, 'upload failed, reason:{}!'.format(e)]

    return handle_result


def sftp_upload_file(sftp_cli, sftp_dir_path, local_file_path):
    handle_result = [SUCCESS, '']
    try:
        sftp_dir_path = file_util.normal_unix_path(sftp_dir_path)
        try:
            sftp_cli.chdir(sftp_dir_path)
        except:
            sftp_dir_path_arr = sftp_dir_path.split(file_util.unix_sep)
            temp_path = ''

            for item in sftp_dir_path_arr:
                if item:
                    if temp_path:
                        temp_path = file_util.join_unix_path(temp_path, item)
                    else:
                        temp_path = file_util.unix_sep + item

                    try:
                        sftp_cli.chdir(temp_path)
                    except:
                        sftp_cli.mkdir(temp_path)

        filename = os.path.basename(local_file_path)
        sftp_file_path = file_util.join_unix_path(sftp_dir_path, filename)
        sftp_cli.put(local_file_path, sftp_file_path)

        handle_result = [SUCCESS, f'upload {filename} success.']
    except Exception as e:
        handle_result = [FAILED, 'upload failed, reason: {}!'.format(e)]

    return handle_result


def sftp_download(sftp_cli, sftp_path, local_dir_path, callback=None, max_concurrent_prefetch_requests=512):
    handle_result = [SUCCESS, '']
    try:
        sftp_path = file_util.normal_unix_path(sftp_path)
        local_dir_path = file_util.normalpath(local_dir_path)

        # download file
        if stat.S_ISREG(sftp_cli.stat(sftp_path).st_mode):
            sftp_file_name = os.path.basename(sftp_path)
            local_file_path = os.path.join(local_dir_path, sftp_file_name)

            if not os.path.isdir(local_dir_path):
                os.makedirs(local_dir_path)

            sftp_cli.get(sftp_path, local_file_path, callback=callback, max_concurrent_prefetch_requests=max_concurrent_prefetch_requests)

            handle_result = [SUCCESS, f'download {sftp_file_name} success.']
        # download dir
        else:
            for filename in sftp_cli.listdir(sftp_path):
                sftp_file_name = file_util.join_unix_path(sftp_path, filename)
                if is_dir(sftp_cli, sftp_file_name):
                    lad = os.path.join(local_dir_path, filename)
                else:
                    lad = local_dir_path

                rs = sftp_download(sftp_cli, sftp_file_name, lad)

                handle_result[1] = handle_result[1] + rs[1]
                if rs[0] == FAILED:
                    handle_result[0] = FAILED
                else:
                    if handle_result[0] != FAILED:
                        handle_result[0] = SUCCESS
    except Exception as e:
        handle_result = [FAILED, 'download failed, reason:{}!'.format(e)]

    return handle_result


def is_dir(sftp_cli, path):
    try:
        sftp_cli.chdir(path)
        return True
    except:
        return False

# as_file为true时，则以拷贝远程文件的方式下载到本地，否则以普通的ssh请求分片下载文件
def sftp_download_file(sftp_cli, sftp_file_path, local_file_path, force=True, as_file=True, callback=None, max_concurrent_prefetch_requests=512):
    handle_result = [SUCCESS, '']
    try:
        sftp_file_path = file_util.normal_unix_path(sftp_file_path)
        local_file_path = file_util.normalpath(local_file_path)

        # download file
        if stat.S_ISREG(sftp_cli.stat(sftp_file_path).st_mode):
            sftp_file_name = os.path.basename(sftp_file_path)
            local_dir_path = os.path.dirname(local_file_path)

            if not os.path.isdir(local_dir_path):
                os.makedirs(local_dir_path)

            # 如果本地已有相应文件，强制覆盖时，则直接删除本地现有文件，否则报本地已有相应文件。
            if os.path.isfile(local_file_path):
                if force:
                    os.remove(local_file_path)
                else:
                    handle_result = [FAILED, f'file {local_file_path} already exists!']
                    return handle_result

            if as_file:
                with sftp_cli.open(sftp_file_path, 'rb') as fp:
                    shutil.copyfileobj(fp, open(local_file_path, 'wb'))
            else:
                sftp_cli.get(sftp_file_path, local_file_path, callback=callback, max_concurrent_prefetch_requests=max_concurrent_prefetch_requests)

            handle_result = [SUCCESS, f'download {sftp_file_name} success.']
        else:
            handle_result = [FAILED, f'sftp_file_path {sftp_file_path} is not a file!']
    except Exception as e:
        handle_result = [FAILED, 'download failed, reason:{}!'.format(e)]

    return handle_result

if __name__ == '__main__':
    pass
