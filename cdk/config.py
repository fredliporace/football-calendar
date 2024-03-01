"""CDK stack config."""

from pydantic_settings import BaseSettings


class StackSettings(BaseSettings):  # pylint: disable=too-few-public-methods
    """CDK application settings."""

    parser: str
    parser_ctor_args: str
    parser_get_calendar_args: str

    class Config:  # pylint: disable=too-few-public-methods
        """model config."""

        env_file = ".env"
        env_prefix = "FOOTCAL_"
