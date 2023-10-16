from pydantic import BaseSettings
from axsqlalchemy.settings import Settings as _DBSettings


class JWTSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


class EmailSystemSettings(BaseSettings):
    EMAIL_SENDER: str
    EMAIL_SENDER_PASSWD: str
    EMAIL_HOST: str
    EMAIL_PORT: int = 587


class AuthRouteSettings(JWTSettings, EmailSystemSettings):
    VERIFICATION_CODE_EXPIRING_MINUTES: int = 300


class ConfigurationSettings(BaseSettings):
    FIRST_USER_NAME: str = 'admin'
    FIRST_USER_EMAIL: str
    FIRST_USER_PASSWD: str


class LimitationSettings(BaseSettings):
    CONTENT_SIZE_BYTES_LIMIT: int = (1024**2 * 10) + (1024 * 4)


class Settings(LimitationSettings, _DBSettings, AuthRouteSettings, ConfigurationSettings):
    class Config:
        env_file = '.env'


