from aws_cdk import Stack, Aws
from aws_cdk import aws_glue as glue
from constructs import Construct


class GlueDataCatalogStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Ingest Glue Data Catalog database
        glue.CfnDatabase(
            self,
            "budget-guard-ingest-database",
            catalog_id=Aws.ACCOUNT_ID,
            database_input={
                "name": "budget-guard-ingest-database",
                "description": "AWS Glue Database for ingestion",
            },
        )

        # Create a Bronze Glue Data Catalog database
        glue.CfnDatabase(
            self,
            "budget-guard-bronze-database",
            catalog_id=Aws.ACCOUNT_ID,
            database_input={
                "name": "budget-guard-bronze-database",
                "description": "AWS Glue Database for bronze",
            },
        )


class GlueCrawlersStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a Ingestion Glue Crawler
        glue.CfnCrawler(
            self,
            "budget-guard-ingest-crawler",
            name="budget-guard-ingest-crawler",
            role=f"arn:aws:iam::{Aws.ACCOUNT_ID}:role/service-role/AWSGlueServiceRole",  # noqa
            database_name="budget-guard-ingest-database",
            targets={"s3Targets": [{"path": "s3://budget-guard-ingest"}]},
            # schedule=glue.CfnCrawler.ScheduleProperty(schedule_expression="cron(0 1 * * ? *)"),  # noqa
        )

        # Create a Bronze Glue Crawler
        glue.CfnCrawler(
            self,
            "budget-guard-bronze-crawler",
            name="budget-guard-bronze-crawler",
            role=f"arn:aws:iam::{Aws.ACCOUNT_ID}:role/service-role/AWSGlueServiceRole",  # noqa
            database_name="budget-guard-bronze-database",
            targets={"s3Targets": [{"path": "s3://budget-guard-bronze"}]},
            # schedule=glue.CfnCrawler.ScheduleProperty(schedule_expression="cron(0 1 * * ? *)"),  # noqa
        )
