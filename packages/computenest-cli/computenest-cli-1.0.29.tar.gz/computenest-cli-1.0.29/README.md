# ComputeNest-CLI

## Project description
computenest-cli is a tool that integrates the creation, updating, and deployment of artifacts, as well as the creation and updating of services. It also provides the ability to associate artifacts with services and supports various custom operations, such as custom image creation. Users can choose different types of artifacts and associate them with services based on their needs.

## Requirements
Python >= 3.6

## Installation
computenest-cli uses a common package management tool named pip.
```
#Install the computenest-cli 
pip install computenest-cli
```

## Usage
To use computenest-cli, simply run the computenest-cli command with the required parameters:
```
computenest-cli --file_path $FILE_PATH --access_key_id $ACCESS_KEY_ID --access_key_secret $ACCESS_KEY_SECRET
```
Replace `$FILE_PATH` with the path to the config.yaml you want to manage, and `$ACCESS_KEY_ID` and `$ACCESS_KEY_SECRET` with your AccessKey ID and AccessKey Secret.

## How to get the AccessKey pair
[Create an AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair?spm=a2c63.p38356.0.0.aa567e1bcFd8lF)

