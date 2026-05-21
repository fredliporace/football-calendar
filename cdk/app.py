"""CDK app."""

from pathlib import Path
from subprocess import call
from typing import Dict

from aws_cdk import App, CfnOutput, Duration, Stack
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk.aws_lambda import Code, Function, FunctionUrl, FunctionUrlAuthType, Runtime
from config import StackSettings

SETTINGS = StackSettings()


# Mypy, error: Class cannot subclass "Stack" (has type "Any")
class FootcalStack(Stack):  # type: ignore
    """FootcalStack."""

    def __init__(self, application: App, idnt: str):
        """Ctor."""
        super().__init__(application, idnt)
        self.lambda_env_: Dict[str, str] = {}

        self.lambda_env_["PARSER"] = SETTINGS.parser
        self.lambda_env_["PARSER_CTOR_ARGS"] = SETTINGS.parser_ctor_args
        self.lambda_env_["PARSER_GET_CALENDAR_ARGS"] = SETTINGS.parser_get_calendar_args
        # Copy lambda code to build directory and install python dependencies there
        retcode = call("cp -u ./lambda/code.py ../cdk_build/lambda", shell=True)
        assert retcode == 0
        # We need --upgrade here since footcal itself must be installed
        retcode = call(
            "cd ../ && pip install . --upgrade -t ./cdk_build/lambda/ -c constraints.txt -q -q",
            shell=True,
        )
        assert retcode == 0
        lfun = Function(
            scope=self,
            id="footcal-lambda",
            runtime=Runtime.PYTHON_3_14,
            handler="code.handler",
            environment=self.lambda_env_,
            code=Code.from_asset(
                path=str(Path(__file__).parent.parent / "cdk_build/lambda")
            ),
            timeout=Duration.seconds(10),
            # Resource handler returned message: "Specified ReservedConcurrentExecutions
            # for function decreases account's
            # UnreservedConcurrentExecution below its minimum value of [10]
            # reserved_concurrent_executions=10,
        )
        lfun_url = FunctionUrl(
            scope=self,
            id="footcal-url",
            function=lfun,
            auth_type=FunctionUrlAuthType.NONE,
        )
        CfnOutput(
            scope=self,
            id="url",
            value=lfun_url.url,
        )

        # Create an SNS topic
        topic = sns.Topic(self, "FootcalTopic", display_name="Footcal Alarms topic")

        # Add an email subscription
        topic.add_subscription(
            subscriptions.EmailSubscription(SETTINGS.notification_email)
        )

        # Create a CloudWatch alarm for the Lambda function's errors
        alarm = cloudwatch.Alarm(
            self,
            "FootcalAlarm",
            metric=lfun.metric_errors(),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if the footcal lambda function fails",
        )

        # Add an action to the alarm to publish to the SNS topic
        alarm.add_alarm_action(cw_actions.SnsAction(topic))


app = App()
FootcalStack(app, "footcal")
app.synth()
