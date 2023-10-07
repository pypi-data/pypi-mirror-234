"""
Celery launcher
"""
import os
from dataclasses import dataclass
from celery import Celery


@dataclass
class Settings:
    """
    settings class for celery
    """
    #  pylint: disable=invalid-name
    CELERY_BROKER_URL: str = os.getenv('REDIS_HOST',
                                       'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND: str = os.getenv('REDIS_HOST',
                                           'redis://localhost:6379/0')
    DEFAULT_CELERY_APP_NAME: str = 'lottostar_celery'
    CELERY_IMPORTS = ["app.cli.main"]


settings = Settings()
celery_app = Celery(settings.DEFAULT_CELERY_APP_NAME)
celery_app.config_from_object(settings, namespace='CELERY')
