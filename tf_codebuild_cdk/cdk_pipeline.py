import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_s3 as s3,
)
from constructs import Construct

class CdkPipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "ArtifactBucket",
            bucket_name = "cdk-timmy-011124",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            access_control = s3.BucketAccessControl.PRIVATE,
            encryption = s3.BucketEncryption.S3_MANAGED,
            versioned = False,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL,
        )

        cdk_build_outputs = cp.Artifact(artifact_name="cdk_build")
        source_output = cp.Artifact(artifact_name='source')

        cdk_build_project = cb.PipelineProject(
            self,
            "Build",
            project_name="cdk-build-project",
            build_spec=cb.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        "commands": [
                            "python -m pip install -r requirements.txt",
                            "npx cdk ls",
                        ]
                    }
                }
            }),
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_5_0,
                privileged=True,
                compute_type=cb.ComputeType.MEDIUM,
            )
        )

        pipeline_stages = [
            cp.StageProps(
            stage_name='Source',
            actions=[
                    cp_actions.CodeStarConnectionsSourceAction(
                        connection_arn="arn:aws:codestar-connections:us-east-1:800493571185:connection/9d781b7a-835e-4880-b59d-b04f4034b216k",
                        repo="tf-codebuild-cdk",
                        branch="main",
                        owner="mcas101",
                        action_name="Pull",
                        trigger_on_push=True,
                        output=source_output
                    )
                ]
            ),
            cp.StageProps(
                stage_name='Build',
                actions=[
                    cp_actions.CodeBuildAction(
                        action_name="cdk_synth",
                        input=source_output,
                        project=cdk_build_project,
                        outputs=[cdk_build_outputs],
                        run_order=1
                    )
                ]
            )

        ]

        pipeline = cp.Pipeline(
            self,
            "CdkPipeline",
            pipeline_name="Timmy-Pipe",
            artifact_bucket=bucket,
            stages=pipeline_stages
        )