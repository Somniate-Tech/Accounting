from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    MAIL_USERNAME: str

    MAIL_PASSWORD: str

    MAIL_FROM: str

    MAIL_PORT: int

    MAIL_SERVER: str

    MAIL_FROM_NAME: str

    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str

    RAZORPAY_WEBHOOK_SECRET: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880

    class Config:
        env_file = ".env"


settings = Settings()