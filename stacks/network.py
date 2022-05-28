import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

from stacks.common import StackProps


class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, sysname: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs) 

        vpc = ec2.Vpc(
            self,
            id=f"{sysname}-vpc",
            cidr="10.1.0.0/16",
            max_azs=1,
            nat_gateways=2,
            subnet_configuration=[ # 問題にする
                ec2.SubnetConfiguration(
                    name=f"{sysname}-public",
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name=f"{sysname}-private",
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PRIVATE,
                ),
                # ec2.SubnetConfiguration(
                #     name=f"{sysname}-protected",
                #     cidr_mask=24,
                #     subnet_type=ec2.SubnetType.ISOLATED,
                # ),
            ],
        )

        cdk.Tags.of(vpc).add(key="Name", value=f"{sysname}-vpc")

        self.__vpc = vpc

    @property
    def vpc(self) -> ec2.Vpc:
        return self.__vpc
