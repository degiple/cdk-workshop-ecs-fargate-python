import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.cdk_workshop_ecs_fargate_python_stack import CdkWorkshopEcsFargatePythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_workshop_ecs_fargate_python/cdk_workshop_ecs_fargate_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkWorkshopEcsFargatePythonStack(app, "cdk-workshop-ecs-fargate-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
