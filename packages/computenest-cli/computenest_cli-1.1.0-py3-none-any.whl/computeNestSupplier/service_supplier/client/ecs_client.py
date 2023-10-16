# -*- coding: utf-8 -*-
from computeNestSupplier.service_supplier.client.base_client import BaseClient
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client

class EcsClient(BaseClient):
    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)

    def create_client_ecs(self):
        self.config.endpoint = f'ecs.{self.region_id}.aliyuncs.com'
        return Ecs20140526Client(self.config)