from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_ecr as _ecr
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_notifications as _s3_notifications
from aws_cdk import Aws, Duration
from constructs import Construct


class IngestionLambdaStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, image_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.build_lambda_func(self.get_lambda_image(image_name))

    def get_lambda_image(self, image_name: str):
        ecr_repository = _ecr.Repository.from_repository_attributes(
            self,
            id="ECR",
            repository_arn="arn:aws:ecr:{0}:{1}:repository".format(
                Aws.REGION, Aws.ACCOUNT_ID
            ),
            repository_name=image_name,
        )
        ecr_image = _lambda.DockerImageCode.from_ecr(
            repository=ecr_repository,
            tag="0.13.0",
            cmd=[
                "budgetguard.cdk_infrastructure.lambda_function.core.lambda_handler"  # noqa
            ],
            entrypoint=["python", "-m", "awslambdaric"],
        )
        return ecr_image

    def build_lambda_func(self, lambda_image: _lambda.Code):
        ingestion_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="IngestionLambda",
            function_name="IngestionLambda",
            code=lambda_image,
            timeout=Duration.seconds(300),
            memory_size=1024,
        )
        bucket = _s3.Bucket.from_bucket_name(
            self, id="budget-guard-ingest", bucket_name="budget-guard-ingest"
        )
        bucket.add_event_notification(
            _s3.EventType.OBJECT_CREATED,
            _s3_notifications.LambdaDestination(ingestion_lambda),
        )
