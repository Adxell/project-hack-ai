from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str

    secret_key: str 

    algorithm: str

    access_token_expire_minutes: int

    path_api: str

    model_config = SettingsConfigDict(
        env_file='.env.dev',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

settings = Settings()
