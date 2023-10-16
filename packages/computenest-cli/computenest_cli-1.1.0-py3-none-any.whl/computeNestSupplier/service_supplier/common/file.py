# -*- coding: utf-8 -*-
import oss2
import requests
import hashlib
import os
from computeNestSupplier.service_supplier.common import constant


class File:
    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def put_file(self, file_data, file_path, type):
        file_name = os.path.basename(file_path)
        if type == 'file':
            sts_access_key_id = file_data.body.data.access_key_id
            sts_access_key_secret = file_data.body.data.access_key_secret
            security_token = file_data.body.data.security_token
            bucket_name = file_data.body.data.bucket_name
            object_name = file_data.body.data.key
            region_id = file_data.body.data.region_id
        else:
            sts_access_key_id = file_data.body.credentials.access_key_id
            sts_access_key_secret = file_data.body.credentials.access_key_secret
            security_token = file_data.body.credentials.security_token
            bucket_name = file_data.body.available_resources[0].repository_name
            object_name = '{}/{}'.format(file_data.body.available_resources[0].path, file_name)
            region_id = file_data.body.available_resources[0].region_id
        endpoint = f'oss-{region_id}.aliyuncs.com'
        auth = oss2.StsAuth(sts_access_key_id, sts_access_key_secret, security_token)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        with open(file_path, 'rb') as fileobj:
            fileobj.seek(0, os.SEEK_SET)
            current = fileobj.tell()
            result = bucket.put_object(object_name, fileobj)

        url = "https://{}.{}/{}".format(bucket_name, endpoint, object_name)
        return url

    def check_file_repeat(self, file_url, file_path):
        response = requests.get(file_url)
        if '?' in file_url:
            # 文件部署物的私有链接会包含token，服务的logo和模版链接不包含token
            file_url = file_url.split('?')[0]
        file_name = os.path.basename(file_url)
        file_url_path = os.path.join(constant.TEMP_PATH, file_name)
        # 创建文件夹（如果不存在）
        os.makedirs(constant.TEMP_PATH, exist_ok=True)

        with open(file_url_path, 'wb') as f:
            f.write(response.content)

        # 计算文件的MD5值
        md5_hash = hashlib.md5()
        with open(file_url_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
        md5_file_url = md5_hash.hexdigest()

        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
        md5_file = md5_hash.hexdigest()

        if md5_file_url == md5_file:
            os.remove(file_url_path)
            return True
        else:
            os.remove(file_url_path)
            return False
