"""CDK app."""

from pathlib import Path

from aws_cdk import App, CfnOutput, Stack
from aws_cdk.aws_lambda import Code, Function, FunctionUrl, FunctionUrlAuthType, Runtime


# Mypy, error: Class cannot subclass "Stack" (has type "Any")
class FootcalStack(Stack):  # type: ignore
    """FootcalStack."""

    def __init__(self, application: App, idnt: str):
        """Ctor."""
        super().__init__(application, idnt)

        lfun = Function(
            scope=self,
            id="footcal-lambda",
            runtime=Runtime.PYTHON_3_7,
            handler="code.handler",
            code=Code.from_asset(path=str(Path(__file__).parent / "lambda")),
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


app = App()
FootcalStack(app, "footcal")
app.synth()
