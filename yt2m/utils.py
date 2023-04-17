import logging

from django.conf import settings
from django.utils import timezone

from yt2m.celery import app

from yt2m.models import Download

logger = logging.getLogger(__name__)


def get_progress(obj):
    if obj.state == Download.States.DOWNLOADING:
        result = app.AsyncResult(obj.task_id)
        progress = 1
        if result and result.info:
            progress = result.info.get("progress", 1)
    elif obj.state == Download.States.CONVERTING:
        # TODO do this properly, this is just based on some assumptions
        elapsed = (timezone.now() - obj.created_at).total_seconds()
        progress = min(
            95, int(70 + 30 * elapsed / obj.youtube_duration * settings.PROGRESS_MAGIC)
        )
    else:
        progress = 100

    return progress


class DummyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        logger.error("DummyLogger error: %s", msg)


class DummyStore:
    def __init__(self):
        self.filename = None

    def set(self, value):
        self.filename = value
