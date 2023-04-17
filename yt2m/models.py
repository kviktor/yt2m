import uuid

from django.db import models
from django.urls import reverse


class Download(models.Model):
    class States(models.IntegerChoices):
        DOWNLOADING = 0, "Downloading video..."
        CONVERTING = 1, "Converting video..."
        SUCCESS = 2, "Finished"
        ERROR = 3, "ERROR"
        CLEANED = 4, "Cleaned"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.SmallIntegerField(choices=States.choices, default=States.DOWNLOADING)
    youtube_id = models.CharField(max_length=128)
    youtube_title = models.CharField(max_length=128)
    youtube_thumbnail = models.CharField(max_length=255)
    youtube_duration = models.IntegerField()
    error = models.TextField(null=True, blank=True)
    task_id = models.CharField(max_length=128)
    cut_start = models.SmallIntegerField(null=True, default=0)
    cut_end = models.SmallIntegerField(null=True, default=None)

    @property
    def in_progress(self):
        return self.state in (self.States.DOWNLOADING, self.States.CONVERTING)

    def get_absolute_url(self):
        return reverse("download", kwargs={'download_id': self.uuid})
