#!/usr/bin/env python3
import os

import aws_cdk as cdk

from tf_codebuild_cdk.tf_codebuild_cdk_stack import TfCodebuildCdkStack


app = cdk.App()
TfCodebuildCdkStack(app, "TfCodebuildCdkStack")

app.synth()
