from aws_cdk import (
    Stack,
    aws_codebuild as cb,
    aws_secretsmanager as sm,
    aws_iam as iam
)
from constructs import Construct

class TfCodebuildCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        codebuild_role = iam.Role(
            self,
            "CodebuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
        )

        codebuild_role.add_to_policy(
            iam.PolicyStatement(
                resources=["*"],
                actions=[
                    "cloudformation:*"
                ]
            )
        )

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

        # gh_secret = sm.Secret.from_secret_attributes(
        #     self,
        #     "ImportedSecret",
        #     secret_complete_arn = "arn:aws:secretsmanager:us-east-1:800493571185:secret:gh-token-HKxmQt",
        # ).secret_value #THIS .secret_value is needed 100%


        # cb.GitHubSourceCredentials(
        #     self,
        #     "credentials",
        #     access_token    = gh_secret
        # )

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

        build_spec = cb.BuildSpec.from_source_filename(
            filename=('buildspecs/cb_buildspec.yaml')
        )

        project = cb.Project(
            self,
            "CodebuildProject",
            project_name            = "timmy",
            source                  = source,
            environment             = build_env,
            build_spec              = build_spec,
            role                    = codebuild_role
        )

        self.output_props = {}
        self.output_props['cb_cdk_diff'] = project

    # Pass object to other stacks
    @property
    def outputs(self):
        return self.output_props