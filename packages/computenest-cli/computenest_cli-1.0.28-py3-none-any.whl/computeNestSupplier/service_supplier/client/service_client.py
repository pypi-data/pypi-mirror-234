# -*- coding: utf-8 -*-
import json
from alibabacloud_computenestsupplier20210521 import models as compute_nest_supplier_20210521_models
from computeNestSupplier.service_supplier.client.compute_nest_client import ComputeNestClient
from computeNestSupplier.service_supplier.common.util import Util
from computeNestSupplier.service_supplier.common import constant


class ServiceClient(ComputeNestClient):

    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)
        self.client = self.create_client_compute_nest()

    def create_service(self, service_data, service_id=''):
        service = service_data
        service_info = service_data.get(constant.SERVICE_INFO)
        deploy_meta_data = service_data.get(constant.DEPLOY_METADATA)
        operation_metadata = service_data.get(constant.OPERATION_METADATA)
        if operation_metadata is None:
            operation_metadata = '{}'
        else:
            operation_metadata = json.dumps(operation_metadata)
        version_name = Util.add_timestamp_to_version_name(service_data.get(constant.VERSION_NAME))
        for template in deploy_meta_data.get(constant.TEMPLATE_CONFIGS):
            template[constant.PREDEFINED_PARAMETERS] = template.get(constant.PREDEFINED_PARAMETERS) or []
            template[constant.HIDDEN_PARAMETER_KEYS] = template.get(constant.HIDDEN_PARAMETER_KEYS) or []
        json_data = json.dumps(deploy_meta_data)
        service_info_init = compute_nest_supplier_20210521_models.CreateServiceRequestServiceInfo(
            locale=service_info.get(constant.LOCALE),
            short_description=service_info.get(constant.SHORT_DESCRIPTION),
            image=service_info.get(constant.IMAGE),
            name=service_info.get(constant.NAME)
        )
        if service_id:
            create_service_request = compute_nest_supplier_20210521_models.CreateServiceRequest(
                region_id=service.get(constant.REGION_ID),
                service_id=service_id,
                deploy_type=service.get(constant.DEPLOY_TYPE),
                operation_metadata=operation_metadata,
                version_name=version_name,
                service_type=service.get(constant.SERVICE_TYPE),
                service_info=[service_info_init],
                deploy_metadata=json_data
            )
        else:
            create_service_request = compute_nest_supplier_20210521_models.CreateServiceRequest(
                region_id=service.get(constant.REGION_ID),
                deploy_type=service.get(constant.DEPLOY_TYPE),
                operation_metadata=operation_metadata,
                version_name=version_name,
                service_type=service.get(constant.SERVICE_TYPE),
                service_info=[service_info_init],
                deploy_metadata=json_data
            )
        response = self.client.create_service(create_service_request)
        return response

    def update_service(self, service_data, service_id):
        service = service_data
        service_info = service_data.get(constant.SERVICE_INFO)
        deploy_meta_data = service_data.get(constant.DEPLOY_METADATA)
        operation_metadata = service_data.get(constant.OPERATION_METADATA)
        if operation_metadata is None:
            operation_metadata = '{}'
        else:
            operation_metadata = json.dumps(operation_metadata)

        version_name = Util.add_timestamp_to_version_name(service_data.get(constant.VERSION_NAME))
        deploy_metadata = service_data.get(constant.DEPLOY_METADATA)
        for template in deploy_metadata.get(constant.TEMPLATE_CONFIGS):
            template[constant.PREDEFINED_PARAMETERS] = template.get(constant.PREDEFINED_PARAMETERS) or []
            template[constant.HIDDEN_PARAMETER_KEYS] = template.get(constant.HIDDEN_PARAMETER_KEYS) or []
        json_data = json.dumps(deploy_meta_data)
        service_info_init = compute_nest_supplier_20210521_models.UpdateServiceRequestServiceInfo(
            name=service_info.get(constant.NAME),
            image=service_info.get(constant.IMAGE),
            short_description=service_info.get(constant.SHORT_DESCRIPTION),
            locale=service_info.get(constant.LOCALE)
        )
        update_service_request = compute_nest_supplier_20210521_models.UpdateServiceRequest(
            region_id=service.get(constant.REGION_ID),
            deploy_type=service.get(constant.DEPLOY_TYPE),
            operation_metadata=operation_metadata,
            version_name=version_name,
            service_id=service_id,
            service_info=[service_info_init],
            deploy_metadata=json_data,
            service_type=service.get(constant.SERVICE_TYPE)
        )
        response = self.client.update_service(update_service_request)
        return response

    def list_service(self, service_name):
        filter_first = compute_nest_supplier_20210521_models.ListServicesRequestFilter(
            name=constant.NAME,
            value=[service_name]
        )
        list_services_request = compute_nest_supplier_20210521_models.ListServicesRequest(
            region_id=self.region_id,
            filter=[
                filter_first
            ]
        )
        response = self.client.list_services(list_services_request)
        return response

    def get_service(self, service_id, service_version):
        get_service_request = compute_nest_supplier_20210521_models.GetServiceRequest(
            region_id=self.region_id,
            service_id=service_id,
            service_version=service_version
        )
        response = self.client.get_service(get_service_request)
        return response
