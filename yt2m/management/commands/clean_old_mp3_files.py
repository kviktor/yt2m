import logging
import os
import shutil
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from yt2m.models import Download, STATES


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clean old mp3 files if neccessary"

    def handle(self, *args, **options):
        two_days_ago = timezone.now() - timedelta(days=2)
        for d in Download.objects.filter(state=STATES.SUCCESS, created_at__lt=two_days_ago):
            file_path = os.path.join(settings.MP3_DIRECTORY, f"{d.uuid}.mp3")

            try:
                os.unlink(file_path)
            except OSError:
                logger.error("%s not found", file_path)

    total, used, free = shutil.disk_usage(__file__)
    if free / 1024 ** 3 < settings.FREE_SPACE_WARNING:
        logger.error("Available free space: %s", free / 1024 ** 3)
