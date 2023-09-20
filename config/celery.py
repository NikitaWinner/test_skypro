import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Конфигурируем Celery из объекта настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в установленных приложениях Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Настраиваем расписание для периодических задач (beat schedule)
app.conf.beat_schedule = {
    'run-code-check': {
        'task': 'code_verification_app.tasks.run_code_check',
        'schedule': crontab(hour='20', minute='0'),
    },
}
