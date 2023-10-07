from cloudlift.deployment.environment_creator import EnvironmentCreator
from cloudlift.version import VERSION
from cloudlift.config import EnvironmentConfiguration

from moto import mock_cloudformation,mock_dynamodb
from unittest.mock import patch
import os
import pytest
import json
environment_name = "cloudlift-test"

def mocked_environment_config(cls, *args, **kwargs):
    return json.loads("""
    {"Item":{"configuration":{
     "environment": "cloudlift-test",
     "configuration": {
      "cloudlift_version": "2.0.0",
      "staging": {
       "environment": {
        "notifications_arn": "arn:aws:sns:ap-south-1:725827686899:non-prod-mumbai",
        "ssl_certificate_arn": "arn:aws:acm:ap-south-1:725827686899:certificate/a5293a7e-f780-42ac-aa22-35ea42ebe040"
       },
       "cluster": {
        "ami_id": "/staging/optimized-ami/amazon-linux-2",
        "ecs_instance_default_lifecycle_type": "spot",
        "instance_type": "c5a.xlarge,c5a.2xlarge,m5a.xlarge,t3a.xlarge,t4g.xlarge,r5a.xlarge",
        "key_name": "staging-cluster-v3",
        "max_instances": 20,
        "min_instances": 5,
        "spot_max_instances": 20,
        "spot_min_instances": 10
       },
       "region": "ap-south-1",
       "vpc": {
        "cidr": "10.30.0.0/16",
        "nat-gateway": {
         "elastic-ip-allocation-id": "eipalloc-05f2599c8bd8d3d28"
        },
        "subnets": {
         "private": {
          "subnet-1": {
           "cidr": "10.30.4.0/22"
          },
          "subnet-2": {
           "cidr": "10.30.12.0/22"
          }
         },
         "public": {
          "subnet-1": {
           "cidr": "10.30.0.0/22"
          },
          "subnet-2": {
           "cidr": "10.30.8.0/22"
          }
         }
        }
       }
      }
     }}}}
    
    """)
# @pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


def test_config_present():
    aws_credentials()
    assert type(mocked_environment_config(None)) == dict
    with mock_cloudformation(aws_credentials()),mock_dynamodb(aws_credentials()):
        with patch.object(EnvironmentConfiguration,'update_config',
                          new=mocked_environment_config, ),patch.object(EnvironmentConfiguration,'get_config',
                          new=mocked_environment_config):
            EnvironmentCreator(environment_name).run()



if __name__=="__main__":
    print(type(mocked_environment_config(None,None)))