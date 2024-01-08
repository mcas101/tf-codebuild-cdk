from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_codebuild as cb,
)
from constructs import Construct

class TfCodebuildCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TfCodebuildCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        triggers = ["pr"]
        filters = []
        branch = "main"

        if "pr" in triggers:
            filters.append(
                cb.FilterGroup.in_event_of(
                    cb.EventAction.PULL_REQUEST_CREATED,
                    cb.EventAction.PULL_REQUEST_UPDATED
                ).and_base_branch_is(branch),
            )

        source = cb.Source.git_hub(
            owner                   = "mcas101",
            repo                    = "tf-codebuild-cdk",
            branch_or_ref           = branch,
            report_build_status     = True,
            webhook_filters         = filters
        )

        build_env = cb.BuildEnvironment(
            build_image  = cb.LinuxBuildImage.STANDARD_5_0,
            privileged   = True,
            compute_type = cb.ComputeType.MEDIUM,
        )

        build_spec = cb.BuildSpec.from_object({
            "version": "0.1",
            "phases": {
                "build": {
                    "commands": [
                        "echo this works!"
                    ]
                }
            }
            }
        )

        project = cb.Project(
            self,
            "CodebuildProject",
            project_name            = "timmy",
            source                  = source,
            environment             = build_env,
            build_spec              = build_spec
        )

        self.project = project