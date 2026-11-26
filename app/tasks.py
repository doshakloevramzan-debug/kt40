from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def send_notification(email: str, item_title: str):
    # Имитация отправки уведомления
    print(f"Уведомление отправлено на {email}: Создан элемент '{item_title}'")
    return True