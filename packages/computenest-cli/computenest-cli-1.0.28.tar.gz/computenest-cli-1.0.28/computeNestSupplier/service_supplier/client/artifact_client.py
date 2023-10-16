# -*- coding: utf-8 -*-
from alibabacloud_computenestsupplier20210521 import models as compute_nest_supplier_20210521_models
from computeNestSupplier.service_supplier.client.compute_nest_client import ComputeNestClient
from computeNestSupplier.service_supplier.common.util import Util
from computeNestSupplier.service_supplier.common import constant


class ArtifactClient(ComputeNestClient):

    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)
        self.client = self.create_client_compute_nest()

    def create_artifact(self, artifact_data, artifact_id=''):
        artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
        version_name = Util.add_timestamp_to_version_name(artifact_data.get(constant.VERSION_NAME))
        supported_regions = artifact_data.get(constant.SUPPORT_REGION_IDS)
        if artifact_type == constant.ECS_IMAGE:
            artifact_property = compute_nest_supplier_20210521_models.CreateArtifactRequestArtifactProperty(
                region_id=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.REGION_ID),
                image_id=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.IMAGE_ID)
            )
        elif artifact_type == constant.FILE:
            artifact_property = compute_nest_supplier_20210521_models.CreateArtifactRequestArtifactProperty(
                url=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL)
            )
        elif artifact_type == constant.ACR_IMAGE or artifact_type == constant.HELM_CHART:
            repo_name = artifact_data[constant.ARTIFACT_NAME]
            repo_id = artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID]
            tag = artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG]
            artifact_property = compute_nest_supplier_20210521_models.CreateArtifactRequestArtifactProperty(
                repo_name=repo_name,
                repo_id=repo_id,
                tag=tag
            )
        if artifact_id:
            create_artifact_request = compute_nest_supplier_20210521_models.CreateArtifactRequest(
                artifact_id=artifact_id,
                artifact_type=artifact_data.get(constant.ARTIFACT_TYPE),
                name=artifact_data.get(constant.ARTIFACT_NAME),
                version_name=version_name,
                description=artifact_data.get(constant.DESCRIPTION),
                artifact_property=artifact_property,
                support_region_ids=supported_regions
            )
        else:
            create_artifact_request = compute_nest_supplier_20210521_models.CreateArtifactRequest(
                artifact_type=artifact_data.get(constant.ARTIFACT_TYPE),
                name=artifact_data.get(constant.ARTIFACT_NAME),
                version_name=version_name,
                description=artifact_data.get(constant.DESCRIPTION),
                artifact_property=artifact_property,
                support_region_ids=supported_regions
            )
        response = self.client.create_artifact(create_artifact_request)
        return response

    def release_artifact(self, artifact_id):
        release_service_request = compute_nest_supplier_20210521_models.ReleaseArtifactRequest(artifact_id)
        response = self.client.release_artifact(release_service_request)
        return response

    def update_artifact(self, artifact_data, artifact_id):
        artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
        version_name = Util.add_timestamp_to_version_name(artifact_data.get(constant.VERSION_NAME))
        supported_regions = artifact_data.get(constant.SUPPORT_REGION_IDS)
        if artifact_type == constant.ECS_IMAGE:
            artifact_property = compute_nest_supplier_20210521_models.UpdateArtifactRequestArtifactProperty(
                region_id=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.REGION_ID),
                image_id=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.IMAGE_ID)
            )
        elif artifact_type == constant.FILE:
            artifact_property = compute_nest_supplier_20210521_models.UpdateArtifactRequestArtifactProperty(
                url=artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL)
            )
        elif artifact_type == constant.ACR_IMAGE or artifact_type == constant.HELM_CHART:
            repo_name = artifact_data[constant.ARTIFACT_NAME]
            repo_id = artifact_data[constant.ARTIFACT_PROPERTY][constant.REPO_ID]
            tag = artifact_data[constant.ARTIFACT_PROPERTY][constant.TAG]
            artifact_property = compute_nest_supplier_20210521_models.CreateArtifactRequestArtifactProperty(
                repo_name=repo_name,
                repo_id=repo_id,
                tag=tag
            )
        update_artifact_request = compute_nest_supplier_20210521_models.UpdateArtifactRequest(
            artifact_id=artifact_id,
            version_name=version_name,
            description=artifact_data.get(constant.DESCRIPTION),
            artifact_property=artifact_property,
            support_region_ids=supported_regions
        )
        response = self.client.update_artifact(update_artifact_request)
        return response

    def delete_artifact(self, artifact_id, artifact_version):
        delete_artifact_request = compute_nest_supplier_20210521_models.DeleteArtifactRequest(artifact_id,
                                                                                              artifact_version)
        response = self.client.delete_artifact(delete_artifact_request)
        return response

    def list_artifact(self, artifact_name):
        filter_first = compute_nest_supplier_20210521_models.ListArtifactsRequestFilter(
            name=constant.NAME,
            values=[artifact_name]
        )
        list_artifact_request = compute_nest_supplier_20210521_models.ListArtifactsRequest(
            filter=[
                filter_first
            ]
        )
        response = self.client.list_artifacts(list_artifact_request)
        return response

    def list_acr_image_repositories(self, artifact_type, repo_name):
        list_acr_image_repositories_request = compute_nest_supplier_20210521_models.ListAcrImageRepositoriesRequest(
            artifact_type=artifact_type,
            repo_name=repo_name
        )
        response = self.client.list_acr_image_repositories(list_acr_image_repositories_request)
        return response

    def list_acr_image_tags(self, repo_id, artifact_type):
        list_acr_image_tags_request = compute_nest_supplier_20210521_models.ListAcrImageTagsRequest(
            repo_id=repo_id,
            artifact_type=artifact_type
        )
        response = self.client.list_acr_image_tags(list_acr_image_tags_request)
        return response

    def get_artifact(self, artifact_name, artifact_version='', artifact_id=''):
        get_artifact_request = compute_nest_supplier_20210521_models.GetArtifactRequest(
            artifact_version=artifact_version,
            artifact_name=artifact_name,
            artifact_id=artifact_id,
        )
        response = self.client.get_artifact(get_artifact_request)
        return response

    def list_versions(self, artifact_id):
        list_artifact_versions_request = compute_nest_supplier_20210521_models.ListArtifactVersionsRequest(artifact_id)
        response = self.client.list_artifact_versions(list_artifact_versions_request)
        return response
