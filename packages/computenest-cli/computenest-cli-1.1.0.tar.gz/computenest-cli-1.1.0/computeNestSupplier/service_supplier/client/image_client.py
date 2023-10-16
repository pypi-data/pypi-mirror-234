# -*- coding: utf-8 -*-
import json
from computeNestSupplier.service_supplier.client.oos_client import OosClient
from alibabacloud_oos20190601 import models as oos_20190601_models
from computeNestSupplier.service_supplier.client.ecs_client import EcsClient
from computeNestSupplier.service_supplier.common import constant
from alibabacloud_ecs20140526 import models as ecs_20140526_models


class ImageClient(OosClient, EcsClient):
    ACS_ECS_UPDATE_IMAGE = 'ACS-ECS-UpdateImage'
    ZONE = 'Zone'
    INSTANCE_TYPE = 'instanceType'

    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)
        self.client = self.create_client_oos()

    def describe_available_resource(self, instance_type):
        client = self.create_client_ecs()
        describe_available_resource_request = ecs_20140526_models.DescribeAvailableResourceRequest(
            region_id=self.region_id,
            destination_resource=self.ZONE,
            instance_type=instance_type
        )
        response = client.describe_available_resource(describe_available_resource_request)
        return response

    def get_available_zone_id(self, instance_type):
        response = self.describe_available_resource(instance_type)
        zone_id = response.body.available_zones.available_zone[0].zone_id
        return zone_id


    def start_update_Image_execution(self, image_data):
        instance_type = image_data.get(self.INSTANCE_TYPE)
        # 根据用户提供的实例类型和地域选择合适的可用区
        zone_id = self.get_available_zone_id(instance_type)
        image_data[constant.ZONE_ID] = zone_id
        # 默认用户选择新建vpc，无需用户指定vpc/vswitch
        image_data[constant.WHETHER_CREATE_VPC] = True
        json_data = json.dumps(image_data)
        start_execution_request = oos_20190601_models.StartExecutionRequest(
            region_id=self.region_id,
            template_name=self.ACS_ECS_UPDATE_IMAGE,
            parameters=json_data
        )
        response = self.client.start_execution(start_execution_request)
        execution_id = response.body.execution.execution_id

        return execution_id

    def list_execution(self, execution_id):
        list_execution_request = oos_20190601_models.ListExecutionsRequest(execution_id=execution_id)
        response = self.client.list_executions(list_execution_request)
        return response

    def list_task_executions(self, execution_id):
        list_task_executions_request = oos_20190601_models.ListTaskExecutionsRequest(
            region_id=self.region_id,
            execution_id=execution_id
        )
        response = self.client.list_task_executions(list_task_executions_request)
        return response

    def list_execution_logs(self, execution_id):
        list_execution_logs_request = oos_20190601_models.ListExecutionLogsRequest(
            region_id=self.region_id,
            execution_id=execution_id
        )
        response = self.client.list_execution_logs(list_execution_logs_request)
        return response