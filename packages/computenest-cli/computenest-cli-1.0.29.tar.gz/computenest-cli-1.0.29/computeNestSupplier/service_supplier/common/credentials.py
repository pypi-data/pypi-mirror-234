# -*- coding: utf-8 -*-
from alibabacloud_computenestsupplier20210521 import models as compute_nest_supplier_20210521_models
from computeNestSupplier.service_supplier.client.compute_nest_client import ComputeNestClient


class Credentials:
    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.compute_nest_client = ComputeNestClient(self.region_id, self.access_key_id, self.access_key_secret)
        self.client = self.compute_nest_client.create_client_compute_nest()

    def get_upload_credentials(self, file_name):
        get_upload_credentials_request = compute_nest_supplier_20210521_models.GetUploadCredentialsRequest(file_name)
        response = self.client.get_upload_credentials(get_upload_credentials_request)
        return response

    def get_artifact_repository_credentials(self, artifact_type):
        get_artifact_repository_credentials = compute_nest_supplier_20210521_models.GetArtifactRepositoryCredentialsRequest(
            artifact_type, self.region_id)
        response = self.client.get_artifact_repository_credentials(get_artifact_repository_credentials)
        return response
