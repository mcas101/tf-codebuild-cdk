import aws_cdk as core
import aws_cdk.assertions as assertions

from tf_codebuild_cdk.tf_codebuild_cdk_stack import TfCodebuildCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tf_codebuild_cdk/tf_codebuild_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TfCodebuildCdkStack(app, "tf-codebuild-cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })
