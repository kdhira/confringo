
import boto3
import logging

logger: logging.Logger = logging.getLogger(__name__)

class SecretsManagerResolver:
    @classmethod
    def resolve(cls, data: str) -> str:
        logger.info("Retrieving secret %s from AWS SecretsManager", data)
        return get_secret(data)

def get_secret(secret_arn: str) -> str:
    client = boto3.client('secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_arn
        )
    except Exception as e:
        logger.error(e)
        return ''

    return get_secret_value_response['SecretString']

class ParameterStoreResolver:
    @classmethod
    def resolve(cls, data: str) -> str:
        logger.info("Retrieving parameter %s from AWS SSM Parameter Store", data)
        return get_parameter(data)

def get_parameter(parameter_name: str) -> str:
    client = boto3.client("ssm")

    try:
        get_parameter_response = client.get_parameter(
            Name=parameter_name
        )
    except Exception as e:
        logger.error(e)
        return ''

    return get_parameter_response['Parameter']['Value']
