import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

from stacks.common import StackProps


class VpcStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, props: StackProps, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            id=f"{props.sys_stage}-vpc",
            cidr="10.1.0.0/16",
            max_azs=2,  # 問題候補：あえて1にして、エラーが出るようにしておく？
            nat_gateways=2,
            subnet_configuration=[  # 問題にする
                ec2.SubnetConfiguration(
                    name=props.subnet("public").name,
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name=props.subnet("private").name,
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                ),
                # ec2.SubnetConfiguration(
                #     name=f"{props.sys_stage}-protected",
                #     cidr_mask=24,
                #     subnet_type=ec2.SubnetType.ISOLATED,
                # ),
            ],
        )

        cdk.Tags.of(vpc).add(key="Name", value=props.vpc().name)
        for i, pubsub in enumerate(vpc.public_subnets):
            cdk.Tags.of(pubsub).add(
                key="Name", value=props.subnet("public", i + 1).name
            )
        for i, prvsub in enumerate(vpc.private_subnets):
            cdk.Tags.of(prvsub).add(
                key="Name", value=props.subnet("private", i + 1).name
            )

        self.__vpc = vpc

    @property
    def vpc(self) -> ec2.Vpc:
        return self.__vpc
