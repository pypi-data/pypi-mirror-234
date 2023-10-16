"""
Celery launcher
"""
from celery import Celery
from lottostar_cli.app.config.main import settings


celery_app = Celery(settings.DEFAULT_CELERY_APP_NAME)
celery_app.config_from_object(settings, namespace='CELERY')
