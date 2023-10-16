import os
import sys
import json
from ruamel.yaml import YAML
from Tea.exceptions import TeaException
from computeNestSupplier.service_supplier.client.service_client import ServiceClient
from computeNestSupplier.service_supplier.common import constant
from computeNestSupplier.service_supplier.common.util import Util
from computeNestSupplier.service_supplier.processor.artifact_processor import ArtifactProcessor
from computeNestSupplier.service_supplier.common.file import File
from computeNestSupplier.service_supplier.common.credentials import Credentials


class ServiceProcessor:
    FILE = 'file'
    DRAFT = 'draft'
    SERVICE_NOT_FOUND = 'ServiceNotFound'
    CUSTOM_OPERATIONS = 'CustomOperations'
    ACTIONS = 'Actions'
    TEMPLATE_URL = 'TemplateUrl'
    SHARE_TYPE = 'ShareType'
    APPROVAL_TYPE = 'ApprovalType'
    ALWAYS_LATEST = 'AlwaysLatest'
    SECURITY_GROUPS = 'SecurityGroups'
    HIDDEN_PARAMETER_KEYS = 'HiddenParameterKeys'
    PREDEFINED_PARAMETERS = 'PredefinedParameters'
    NETWORK_METADATA = 'NetworkMetadata'
    DEPLOY_TIME_OUT = 'DeployTimeout'
    UPDATE_INFO = 'UpdateInfo'

    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.service = ServiceClient(self.region_id, self.access_key_id, self.access_key_secret)

    def _get_service_logo_url(self, service_name):
        data_list_service = self.service.list_service(service_name)
        service_id = data_list_service.body.services[0].service_id
        service_version = data_list_service.body.services[0].version
        data_get_service = self.service.get_service(service_id, service_version)
        url = data_get_service.body.service_infos[0].image
        return url

    def _get_template_url_data(self, service_name):
        data_list_service = self.service.list_service(service_name)
        service_id = data_list_service.body.services[0].service_id
        service_version = data_list_service.body.services[0].version
        data_get_service = self.service.get_service(service_id, service_version)
        deploy_metadata = data_get_service.body.deploy_metadata
        return deploy_metadata

    def _replace_artifact_data(self, data_service, data_artifact, artifact_type):
        for artifact_service in data_service[constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA][
            artifact_type]:
            id_file = data_service.get(constant.DEPLOY_METADATA).get(constant.SUPPLIER_DEPLOY_METADATA).get(
                artifact_type).get(artifact_service).get(constant.ARTIFACT_ID)
            version_file = data_service.get(constant.DEPLOY_METADATA).get(constant.SUPPLIER_DEPLOY_METADATA).get(
                artifact_type).get(artifact_service).get(constant.ARTIFACT_VERSION)
            id_match = Util.regular_expression(id_file)
            # 将占位符${Artifact.Artifact_x.ArtifactId}解析并输出dict
            version_match = Util.regular_expression(version_file)
            artifact_id_file = data_artifact.get(id_match[1]).get(id_match[2])
            # [0][1][2]为刚才解析出得占位符的分解，即Artifact，Artifact_x，ArtifactId
            artifact_version_file = data_artifact.get(version_match[1]).get(version_match[2])
            data_service[constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA][
                artifact_type][artifact_service][constant.ARTIFACT_ID] = artifact_id_file
            data_service[constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA][
                artifact_type][artifact_service][constant.ARTIFACT_VERSION] = artifact_version_file
        return data_service

    def _replace_file_path_with_url(self, file_path):
        file = File(self.region_id, self.access_key_id, self.access_key_secret)
        credentials = Credentials(self.region_id, self.access_key_id, self.access_key_secret)
        file_name = os.path.basename(file_path)
        data_file = credentials.get_upload_credentials(file_name)
        file_url = file.put_file(data_file, file_path, self.FILE)
        return file_url

    def _delete_field(self, data, field):
        if isinstance(data, dict):
            for key in list(data.keys()):
                if key == field:
                    del data[key]
                else:
                    self._delete_field(data[key], field)
        elif isinstance(data, list):
            for item in data:
                self._delete_field(item, field)

    def _get_service_detail(self, region_id, service_name):
        service = ServiceClient(self.region_id, self.access_key_id, self.access_key_secret)
        response = service.list_service(service_name)
        if len(response.body.services) == 0:
            print("Service does not exist, please check the region_id and service_name")
            sys.exit(1)
        service_id = response.body.services[0].service_id
        version = response.body.services[0].version
        data = service.get_service(service_id, version)
        deploy_metadata = json.loads(data.body.deploy_metadata)
        approval_type = data.body.approval_type
        share_type = data.body.share_type
        service_type = data.body.service_type
        deploy_type = data.body.deploy_type
        self._delete_field(deploy_metadata, self.NETWORK_METADATA)
        self._delete_field(deploy_metadata, self.DEPLOY_TIME_OUT)
        self._delete_field(deploy_metadata, self.ALWAYS_LATEST)
        for config in deploy_metadata[constant.TEMPLATE_CONFIGS]:
            self._delete_field(config, self.SECURITY_GROUPS)
            self._delete_field(config, self.HIDDEN_PARAMETER_KEYS)
            self._delete_field(config, self.PREDEFINED_PARAMETERS)
            self._delete_field(config, self.UPDATE_INFO)
        service_info_pre = data.body.service_infos[0]
        image = service_info_pre.image
        name = service_info_pre.name
        locale = service_info_pre.locale
        short_description = service_info_pre.short_description
        service_info = {
            constant.LOCALE: locale,
            constant.SHORT_DESCRIPTION: short_description,
            constant.IMAGE: image,
            constant.NAME: name
        }
        parameters = {
            constant.REGION_ID: region_id,
            constant.DEPLOY_TYPE: deploy_type,
            constant.DEPLOY_METADATA: deploy_metadata,
            constant.SERVICE_TYPE: service_type,
            constant.SERVICE_INFO: service_info,
            constant.SHARE_TYPE: share_type,
            constant.APPROVAL_TYPE: approval_type
        }

        service = {
            constant.SERVICE: parameters
        }
        return service, deploy_metadata

    @Util.measure_time
    def import_command(self, data_config, file_path, update_artifact, service_name='', version_name='', ):
        data_service = data_config[constant.SERVICE]
        deploy_metadata = data_service[constant.DEPLOY_METADATA]
        file = File(self.region_id, self.access_key_id, self.access_key_secret)
        if data_config.get(constant.ARTIFACT):
            artifact_processor = ArtifactProcessor(self.region_id, self.access_key_id, self.access_key_secret)
            data_artifact = artifact_processor.process(data_config, file_path, update_artifact, version_name)
            if constant.FILE_ARTIFACT_RELATION in deploy_metadata.get(constant.SUPPLIER_DEPLOY_METADATA, {}):
                data_service = self._replace_artifact_data(data_service, data_artifact, constant.FILE_ARTIFACT_RELATION)
            elif constant.ARTIFACT_RELATION in deploy_metadata.get(constant.SUPPLIER_DEPLOY_METADATA, {}):
                data_service = self._replace_artifact_data(data_service, data_artifact, constant.ARTIFACT_RELATION)
            elif constant.ACR_IMAGE_ARTIFACT_RELATION in deploy_metadata.get(constant.SUPPLIER_DEPLOY_METADATA, {}):
                data_service = self._replace_artifact_data(data_service, data_artifact, constant.ACR_IMAGE_ARTIFACT_RELATION)
            elif constant.HELM_CHART_ARTIFACT_RELATION in deploy_metadata.get(constant.SUPPLIER_DEPLOY_METADATA, {}):
                data_service = self._replace_artifact_data(data_service, data_artifact, constant.HELM_CHART_ARTIFACT_RELATION)
        if service_name:
            # 如果有service_name传入，那么覆盖yaml文件中的服务名称
            data_service[constant.SERVICE_INFO][constant.NAME] = service_name
        if version_name:
            data_service[constant.VERSION_NAME] = version_name
        service_name = data_service.get(constant.SERVICE_INFO).get(constant.NAME)
        data_list = self.service.list_service(service_name)
        # 将相对路径替换成绝对路径
        image_path = os.path.join(os.path.dirname(file_path),
                                  data_service.get(constant.SERVICE_INFO).get(constant.IMAGE))
        if data_service.get(constant.OPERATION_METADATA):
            for operation_template in data_service[constant.OPERATION_METADATA][self.CUSTOM_OPERATIONS][self.ACTIONS]:
                # 将相对路径替换成绝对路径
                operation_template_path = os.path.join(os.path.dirname(file_path), operation_template.get(self.TEMPLATE_URL))
                operation_template[self.TEMPLATE_URL] = self._replace_file_path_with_url(operation_template_path)
        # 将部署物的id和version替换成正确的值
        if len(data_list.body.services) == 0:
            # 将服务logo的本地路径替换成Url
            data_service[constant.SERVICE_INFO][constant.IMAGE] = self._replace_file_path_with_url(image_path)
            # 将模版文件的本地路径替换成url
            for template in deploy_metadata.get(constant.TEMPLATE_CONFIGS):
                # 将相对路径替换成绝对路径
                template_path = os.path.join(os.path.dirname(file_path), template.get(constant.URL))
                template[constant.URL] = self._replace_file_path_with_url(template_path)
            data_create = self.service.create_service(data_service)
            service_id = data_create.body.service_id
            current_time = Util.get_current_time()
            print("========================================================")
            print("Successfully created a new service!")
            print("The service name: ", service_name)
            print("The service id: ", service_id)
            print("Completion time: ", current_time)
            print("========================================================")
        else:
            service_id = data_list.body.services[0].service_id
            image_url_existed = self._get_service_logo_url(service_name)
            result_image = file.check_file_repeat(image_url_existed, image_path)
            # 检查服务logo是否重复，重复则不再上传，直接使用原有Url
            if result_image:
                image_url = image_url_existed
            else:
                image_url = self._replace_file_path_with_url(image_path)
            data_service[constant.SERVICE_INFO][constant.IMAGE] = image_url
            data_existed = json.loads(self._get_template_url_data(service_name))
            name_url_mapping = {template[constant.NAME]: template[constant.URL] for template in
                                data_existed.get(constant.TEMPLATE_CONFIGS)}
            # 检查模版文件是否重复，重复则不再上传，直接使用原有Url
            for template in data_service[constant.DEPLOY_METADATA][constant.TEMPLATE_CONFIGS]:
                if template[constant.NAME] in name_url_mapping:
                    # 将相对路径替换成绝对路径
                    template_path = os.path.join(os.path.dirname(file_path), template.get(constant.URL))
                    result_template = file.check_file_repeat(name_url_mapping[template[constant.NAME]], template_path)
                    if result_template:
                        template[constant.URL] = name_url_mapping.get(template[constant.NAME])
                    else:
                        template[constant.URL] = self._replace_file_path_with_url(template_path)
                else:
                    template_path = os.path.join(os.path.dirname(file_path), template.get(constant.URL))
                    template[constant.URL] = self._replace_file_path_with_url(template_path)
            if data_list.body.services[0].status == 'Draft':
                self.service.update_service(data_service, service_id)
                service_name = data_service.get(constant.SERVICE_INFO).get(constant.NAME)
                current_time = Util.get_current_time()
                print("========================================================")
                print("Successfully updated the service!")
                print("The service name: ", service_name)
                print("The service id: ", service_id)
                print("Completion time: ", current_time)
                print("========================================================")
            else:
                service_id = data_list.body.services[0].service_id
                try:
                    self.service.get_service(service_id, self.DRAFT)
                except TeaException as e:
                    if e.code == self.SERVICE_NOT_FOUND:
                        self.service.create_service(data_service, service_id)
                    else:
                        raise
                else:
                    self.service.update_service(data_service, service_id)
                current_time = Util.get_current_time()
                print("========================================================")
                print("Successfully updated the service!")
                print("The service name: ", service_name)
                print("The service id: ", service_id)
                print("Completion time: ", current_time)
                print("========================================================")

    def export_command(self, service_name, file_path):
        artifact = ArtifactProcessor(self.region_id, self.access_key_id, self.access_key_secret)
        data_yaml, deploy_metadata = self._get_service_detail(self.region_id, service_name)
        supplier_deploy_metadata = deploy_metadata[constant.SUPPLIER_DEPLOY_METADATA]
        if data_yaml[constant.SERVICE][constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA]:
            data_yaml.setdefault(constant.ARTIFACT, {})
            i = 1
            for artifact_metadata in supplier_deploy_metadata:
                if artifact_metadata == constant.ARTIFACT_RELATION:
                    relation = constant.ARTIFACT_RELATION
                elif artifact_metadata == constant.HELM_CHART_ARTIFACT_RELATION:
                    relation = constant.HELM_CHART_ARTIFACT_RELATION
                elif artifact_metadata == constant.FILE_ARTIFACT_RELATION:
                    relation = constant.FILE_ARTIFACT_RELATION
                elif artifact_metadata == constant.ACR_IMAGE_ARTIFACT_RELATION:
                    relation = constant.ACR_IMAGE_ARTIFACT_RELATION
                for image_key in data_yaml[constant.SERVICE][constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA][relation]:
                    artifact_key = constant.ARTIFACT + '_' + str(i)
                    i += 1
                    artifact_id = data_yaml[constant.SERVICE][constant.DEPLOY_METADATA][constant.SUPPLIER_DEPLOY_METADATA][relation][image_key][constant.ARTIFACT_ID]
                    data_yaml = artifact.get_artifact_detail(artifact_id, data_yaml, artifact_key)
        yaml = YAML(typ='rt')
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.width = 180
        with open(file_path, "w") as file:
            yaml.dump(data_yaml, file)
        print("========================================================")
        print("Successfully export the config.yaml!")
        print("The file path: \n", file_path)
        print("========================================================")
