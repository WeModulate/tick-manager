from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to manage application configuration.

    Attributes:
        app_name (str): The name of the application.
        debug (bool): Flag to enable or disable debug mode.
    """

    app_name: str = "Tick Manager"
    debug: bool = False

    class Config:
        """
        Configuration class for Settings.

        Attributes:
            env_file (str): The name of the environment file to load settings from.
        """

        env_file = ".env"


# Instantiate the Settings class to load the configuration
settings = Settings()
