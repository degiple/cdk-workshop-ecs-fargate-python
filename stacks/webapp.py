import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_route53 as route53
from constructs import Construct

from stacks.common import StackProps


class WebAppStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        sysname: str,
        vpc: ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        app_name = "webapp"

        ##############################
        # Create fargate task definition.
        ##############################

        # Create task definition
        # VCPU | MEMORY(MiB)
        # 0.25 | 512, 1024, 2048
        # 0.5  | 1024, 2048, 3072, 4096
        # 1    | 2048, 3072, 4096, 5120, 6144, 7168, 8192
        # 2    | 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384
        # 4    | 8192, 9216, 10240, 11264, 12288, 13312, 1436, 15360, 16384, 17408, 18432, 19456, 20480,
        #      | 21504, 22528, 23552, 24576, 25600, 26624, 2764, 28672, 2969, 30720
        fargate_task_definition = ecs.FargateTaskDefinition(
            self,
            id=f"{sysname}-{app_name}-ecs-task-definition",
            family=props.ecs_task_definition(app_name).name,
            cpu=,
            memory_limit_mib=,
        )

        # Add app to containers
        container_app = fargate_task_definition.add_container(
            id=props.ecs_container_name(app_name, "app").id,
            container_name=props.ecs_container_name(app_name, "app").name,
            image=image,
            environment={},
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=props.ecs_container_name(app_name, "app").name,
            ),
        )

        container_app.add_port_mappings(ecs.PortMapping(container_port=80))

        self.__container_app_name = container_app.container_name

        ##############################
        # Create ECS Cluster, Service and ALB
        ##############################

        albfs = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            id="WebappApplicationLoadBalancedFargateService",
            cluster=ecs.Cluster(
                self,
                id="WebappFargateåCluster",
                cluster_name=props.ecs_cluster().name,
                vpc=vpc,
            ),
            task_definition=fargate_task_definition,
            service_name=props.ecs_service(app_name).name,
            protocol=elb.ApplicationProtocol.HTTPS,
            listener_port=443,  # for ALB
            redirect_http=True,
            target_protocol=elb.ApplicationProtocol.HTTP,
            desired_count=1,
            health_check_grace_period=cdk.Duration.seconds(60),  # Default: 60s 
            enable_ecs_managed_tags=True,
        )

        # ECSデプロイの高速化
        # 参考：https://toris.io/2021/04/speeding-up-amazon-ecs-container-deployments/
        albfs.target_group.configure_health_check(
            interval=cdk.Duration.seconds(10),  # Default: 30s
            healthy_threshold_count=2,  # Default: 5
            unhealthy_threshold_count=6,  # Default: 2
        )

        # Quickly deregistration delay of alb target
        albfs.target_group.set_attribute(key="deregistration_delay.timeout_seconds", value="5")  # Default: 300s

        # Configure Auto Scaling
        scalable_target = albfs.service.auto_scale_task_count(min_capacity=2, max_capacity=10)
        scalable_target.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=50)
        scalable_target.scale_on_memory_utilization("MemoryScaling", target_utilization_percent=80)

        self.__service = albfs.service

    @property
    def service(self) -> ecs.FargateService:
        return self.__service
