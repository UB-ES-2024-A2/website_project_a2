""" Configuration utils """
import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    UrlConstraints,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl, Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

# Define a Pydantic definition for SQLite
SQLiteDsn = Annotated[
        Url,
        UrlConstraints(
            host_required=False,
            allowed_schemes=[
                'sqlite',
            ],
        ),
    ]


def parse_cors(v: Any) -> list[str] | str:
    """
    Parse the CORS origins from a string or list of strings.

    Args:
        v: A string or list that represents CORS origins.

    Returns:
        A list of strings if it's a comma-separated string, otherwise returns the input.

    Raises:
        ValueError: If input is not a valid string or list format.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    if isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        """
        Get the server host URL, depending on the environment.

        Returns:
            str: The server host URL.
        """
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    DB_ENGINE: str = "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "sd_db_user"
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn | SQLiteDsn:
        """
        Get the URI for the SQLAlchemy database connection.

        Returns:
            str: The database connection URI.

        Raises:
            ValueError: If the DB_ENGINE is neither 'sqlite' nor 'postgres'.
        """
        database_uri = None
        # Check database engine
        if self.DB_ENGINE == 'postgres':
            if self.DB_NAME is None:
                self.DB_NAME = 'sd_db'
            database_uri = MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        elif self.DB_ENGINE == 'sqlite':
            if self.DB_NAME is None:
                self.DB_NAME = 'sd_db.sqlite'
            database_uri = MultiHostUrl.build(
                scheme="sqlite",
                host='',
                path=self.DB_NAME,
            )
        else:
            raise ValueError(f'Invalid database engine {self.DB_ENGINE}. '
                             f'Valid options are [sqlite, postgres]')
        return database_uri

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        """
        Set the default value for the email sender name if not provided.
        """
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        """
        Check if email functionality is enabled by verifying SMTP settings.

        Returns:
            bool: Whether email sending is enabled.
        """
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False
    HOST: str = "localhost"
    USERDB: str = "username"
    PASSWORD: str = "password"
    DATABASE: str = "database"
    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """
        Check if a secret variable is still set to the default value 'changethis'.
        Raise a warning or error if so.

        Args:
            var_name: The name of the secret variable.
            value: The value of the secret variable.
        """
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        Enforce the use of non-default secrets for various settings.
        """
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        if self.DB_ENGINE != 'sqlite':
            self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self
