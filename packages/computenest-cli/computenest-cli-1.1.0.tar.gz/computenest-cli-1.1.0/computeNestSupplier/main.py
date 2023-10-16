# -*- coding: utf-8 -*-
import yaml
import click
from computeNestSupplier.service_supplier.processor.service_processor import ServiceProcessor
from computeNestSupplier.service_supplier.processor.check_processor import CheckProcesser


@click.group()
def main():
    click.echo("Welcome to computenest-cli")


@click.command(name='import')
@click.option('--update_artifact', default=None, help='Region ID')
@click.option('--service_name', default=None, help='Service name')
@click.option('--version_name', default=None, help='Vervice name')
@click.option('--file_path', required=True, help='File path')
@click.option('--access_key_id', required=True, help='Access Key ID')
@click.option('--access_key_secret', required=True, help='Access Key Secret')
def import_command(update_artifact, service_name, version_name, file_path, access_key_id, access_key_secret):
    if file_path is None:
        click.echo('Please provide the file_path')
        return
    if access_key_id is None:
        click.echo('Please provide the access_key_id')
        return
    if access_key_secret is None:
        click.echo('Please provide the access_key_secret')
        return
    if service_name == 'None':
        service_name = None
    if version_name == 'None':
        version_name = None
    with open(file_path, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    region_id = data['Service']['RegionId']
    service = ServiceProcessor(region_id, access_key_id, access_key_secret)
    check = CheckProcesser(data, file_path)
    check.processor()
    service.import_command(data, file_path, update_artifact, service_name, version_name)


@click.command(name='export')
@click.option('--region_id', required=True, help='Region ID')
@click.option('--service_name', required=True, help='Service name')
@click.option('--file_path', required=True, help='File path')
@click.option('--access_key_id', required=True, help='Access Key ID')
@click.option('--access_key_secret', required=True, help='Access Key Secret')
def export_command(region_id, service_name, file_path, access_key_id, access_key_secret):
    service = ServiceProcessor(region_id, access_key_id, access_key_secret)
    service.export_command(service_name, file_path)


main.add_command(import_command)
main.add_command(export_command)

if __name__ == '__main__':
    main()
