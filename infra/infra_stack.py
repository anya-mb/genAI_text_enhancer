import os
from os.path import dirname

from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
    aws_iam as iam,
)
import aws_cdk.aws_apigatewayv2_alpha as _apigw
import aws_cdk.aws_apigatewayv2_integrations_alpha as _integrations

from constructs import Construct


DIRNAME = dirname(dirname(__file__))


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM Role
        lambda_role = iam.Role(self, "LambdaRole",
                               assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
                               )

        # Define policy statements
        logs_policy = iam.PolicyStatement(
            actions=["logs:CreateLogGroup"],
            resources=["arn:aws:logs:us-east-1:723351182543:*"],
            effect=iam.Effect.ALLOW
        )

        lambda_policy = iam.PolicyStatement(
            actions=["logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["arn:aws:logs:us-east-1:723351182543:log-group:/aws/lambda/bedrock:*"],
            effect=iam.Effect.ALLOW
        )

        bedrock_policy = iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=[
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v1",
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2",
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1"
            ],
            effect=iam.Effect.ALLOW
        )

        # Attach policies to the role
        lambda_role.add_to_policy(logs_policy)
        lambda_role.add_to_policy(lambda_policy)
        lambda_role.add_to_policy(bedrock_policy)

        lambda_improve_text = lambda_.Function(
            self,
            "TextReverser",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset(os.path.join(DIRNAME, "backend")),
            handler="main.lambda_reverse_text_backend",
            timeout=Duration.seconds(30),

        )

        lambda_summarize_text = lambda_.Function(
            self,
            "TextSummarizer",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset(os.path.join(DIRNAME, "backend")),
            handler="main.lambda_summarize_text_backend",
            timeout=Duration.seconds(30),
            role=lambda_role
        )

        # Create the HTTP API with CORS
        http_api = _apigw.HttpApi(
            self,
            "MyHttpApi",
            cors_preflight=_apigw.CorsPreflightOptions(
                allow_methods=[_apigw.CorsHttpMethod.POST],
                allow_origins=["*"],

                max_age=Duration.days(10),
            ),
        )

        # Add a route to POST: reverse
        http_api.add_routes(
            path="/reverse",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=lambda_improve_text
            ),
        )

        # Add a route to POST: summarize
        http_api.add_routes(
            path="/summarize",
            methods=[_apigw.HttpMethod.POST],
            integration=_integrations.HttpLambdaIntegration(
                "LambdaProxyIntegration", handler=lambda_summarize_text
            ),
        )

        # Outputs
        CfnOutput(
            self,
            "API Endpoint",
            description="API Endpoint",
            value=http_api.api_endpoint,
        )
