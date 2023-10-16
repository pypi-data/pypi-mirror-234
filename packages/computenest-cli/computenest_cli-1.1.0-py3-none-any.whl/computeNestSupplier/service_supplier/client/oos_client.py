# -*- coding: utf-8 -*-
from alibabacloud_oos20190601.client import Client as oos20190601Client
from computeNestSupplier.service_supplier.client.base_client import BaseClient


class OosClient(BaseClient):
    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)

    def create_client_oos(self):
        self.config.endpoint = f'oos.{self.region_id}.aliyuncs.com'
        return oos20190601Client(self.config)