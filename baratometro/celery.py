import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baratometro.settings')

# Create the Celery instance
app = Celery('Baratometro')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set broker URL (Redis connection)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

# Configure result backend (optional but recommended)
app.conf.result_backend = 'django-db'

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')