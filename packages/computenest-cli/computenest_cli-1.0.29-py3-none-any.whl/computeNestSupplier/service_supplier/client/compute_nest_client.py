# -*- coding: utf-8 -*-
from alibabacloud_computenestsupplier20210521.client import Client as ComputeNestSupplier20210521Client
from computeNestSupplier.service_supplier.client.base_client import BaseClient


class ComputeNestClient(BaseClient):
    AP_SOUTHEST_1 = 'ap-southeast-1'

    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)

    def create_client_compute_nest(self):
        if self.region_id == self.AP_SOUTHEST_1:
            self.config.endpoint = f'computenestsupplier.ap-southeast-1.aliyuncs.com'
        else:
            self.config.endpoint = f'computenestsupplier.cn-hangzhou.aliyuncs.com'

        return ComputeNestSupplier20210521Client(self.config)