from . import constants
from aws_cdk import Stack
from aws_cdk import aws_mwaa as mwaa
from aws_cdk import aws_iam as iam
from constructs import Construct
from .s3_stack import MWAAS3Stack
from .vpc_stack import MWAAVpcStack


class MWAAStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: MWAAVpcStack,
        s3: MWAAS3Stack,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        mwaa_env_name = f"{constants.CDK_APP_NAME}_codeartifact_env"
        airflow_version = constants.CDK_AIRFLOW_VERSION

        # Create MWAA role
        mwaa_role = iam.Role(
            self,
            "MWAARole",
            assumed_by=iam.ServicePrincipal("airflow-env.amazonaws.com"),
        )

        # Add policies for MWAA Role
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=[
                    (
                        f"arn:aws:airflow:{self.region}:"
                        f"{self.account}:environment/{mwaa_env_name}"
                    )
                ],
                actions=["airflow:PublishMetrics"],
                effect=iam.Effect.ALLOW,
            )
        )
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=[
                    f"arn:aws:s3:::{s3.bucket.bucket_name}",
                    f"arn:aws:s3:::{s3.bucket.bucket_name}/*",
                ],
                actions=["s3:ListAllMyBuckets"],
                effect=iam.Effect.DENY,
            )
        )
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=[
                    f"arn:aws:s3:::{s3.bucket.bucket_name}",
                    f"arn:aws:s3:::{s3.bucket.bucket_name}/*",
                ],
                actions=["s3:*"],
                effect=iam.Effect.ALLOW,
            )
        )
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=[
                    (
                        f"arn:aws:logs:{self.region}:{self.account}:"
                        f"log-group:airflow-{mwaa_env_name}-*"
                    )
                ],
                actions=[
                    "logs:CreateLogStream",
                    "logs:CreateLogGroup",
                    "logs:PutLogEvents",
                    "logs:GetLogEvents",
                    "logs:GetLogRecord",
                    "logs:GetLogGroupFields",
                    "logs:GetQueryResults",
                    "logs:DescribeLogGroups",
                ],
                effect=iam.Effect.ALLOW,
            )
        )
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=["*"],
                actions=["cloudwatch:PutMetricData"],
                effect=iam.Effect.ALLOW,
            )
        )
        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                resources=[f"arn:aws:sqs:{self.region}:*:airflow-celery-*"],
                actions=[
                    "sqs:ChangeMessageVisibility",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ReceiveMessage",
                    "sqs:SendMessage",
                ],
                effect=iam.Effect.ALLOW,
            )
        )

        mwaa_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "kms:Decrypt",
                    "kms:DescribeKey",
                    "kms:GenerateDataKey*",
                    "kms:Encrypt",
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"],
                conditions={
                    "StringEquals": {
                        "kms:ViaService": [
                            f"sqs.{self.region}.amazonaws.com",
                            f"s3.{self.region}.amazonaws.com",
                        ]
                    }
                },
            ),
        )

        # Define MWAA configuration
        security_group_ids = mwaa.CfnEnvironment.NetworkConfigurationProperty(
            security_group_ids=[vpc.mwaa_sg.security_group_id],
            subnet_ids=vpc.get_vpc_private_subnet_ids,
        )

        logs_conf = mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(
            enabled=True, log_level="INFO"
        )

        logging_configuration = (
            mwaa.CfnEnvironment.LoggingConfigurationProperty(
                scheduler_logs=logs_conf,
                webserver_logs=logs_conf,
                dag_processing_logs=logs_conf,
                task_logs=logs_conf,
            )
        )

        # Create MWAA environment
        mwaa_ca_env = mwaa.CfnEnvironment(
            self,
            f"{constants.CDK_APP_NAME}_ca_env",
            name=mwaa_env_name,
            environment_class="mw1.small",
            requirements_s3_path="requirements-mwaa.txt",
            airflow_version=airflow_version,
            execution_role_arn=mwaa_role.role_arn,
            source_bucket_arn=s3.bucket.bucket_arn,
            dag_s3_path="dags",
            max_workers=2,
            webserver_access_mode="PUBLIC_ONLY",
            network_configuration=security_group_ids,
            logging_configuration=logging_configuration,
        )
        mwaa_ca_env.node.add_dependency(mwaa_role)
