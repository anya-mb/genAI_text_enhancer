import os
from os.path import dirname

from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
)
import aws_cdk.aws_apigatewayv2_alpha as _apigw
import aws_cdk.aws_apigatewayv2_integrations_alpha as _integrations

from constructs import Construct


DIRNAME = dirname(dirname(__file__))


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_improve_text = lambda_.Function(
            self,
            "TextImprover",
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
