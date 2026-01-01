import os, logging


class Config():
    # Environment
    ENV = os.getenv("ENV") or "development"
    DEBUG = (ENV == "development")  # Enable debug mode only in development
    SECRET_KEY = os.getenv("SECRET_KEY") or os.environ.get("SECRET_KEY")
    EMERGENCY_MODE = os.getenv("EMERGENCY_MODE") or os.environ.get("EMERGENCY_MODE") or False
    

    # Static and template folders
    STATIC_FOLDER = "resources/static"
    TEMPLATE_FOLDER = "resources/templates"
    
    # CORS
    CORS_ORIGINS = os.getenv("CLIENT_ORIGINS", "http://localhost:3000,http://localhost:5173")
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS.split(",")]
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEED_DB = os.getenv("SEED_DB") or False
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD")
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    BASE_LOG_LEVEL = os.getenv("BASE_LOG_LEVEL", "WARNING")
    
    # JWT configurations
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    # Domains
    APP_DOMAIN = os.getenv("APP_DOMAIN") or "http://localhost:3000"
    API_DOMAIN = os.getenv("API_DOMAIN") or "http://localhost:5050"
    
    # mail configurations
    MAIL_SERVER = os.getenv("MAIL_SERVER") or 'smtp.gmail.com'
    MAIL_PORT = os.getenv("MAIL_PORT") or 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_ALIAS = (f"{MAIL_DEFAULT_SENDER}", f"{MAIL_USERNAME}")
    
    # Cloudinary configurations
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///db.sqlite3"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Map config based on environment
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
