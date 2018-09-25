import uuid

from django.db.models import Model, UUIDField, DateTimeField, SmallIntegerField, IntegerField, CharField, TextField
from django.urls import reverse

from model_utils import Choices


STATES = Choices(
    (0, "DOWNLOADING", "Downloading video..."),
    (1, "CONVERTING", "Converting video..."),
    (2, "SUCCESS", "Finished"),
    (3, "ERROR", "ERROR"),
    (4, "CLEANED", "Cleaned"),
)


class Download(Model):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    state = SmallIntegerField(choices=STATES, default=STATES.DOWNLOADING)
    youtube_id = CharField(max_length=128)
    youtube_title = CharField(max_length=128)
    youtube_thumbnail = CharField(max_length=255)
    youtube_duration = IntegerField()
    error = TextField(null=True, blank=True)
    task_id = CharField(max_length=128)
    cut_start = SmallIntegerField(null=True, default=0)
    cut_end = SmallIntegerField(null=True, default=None)

    @property
    def in_progress(self):
        return self.state in (STATES.DOWNLOADING, STATES.CONVERTING)

    def get_absolute_url(self):
        return reverse("download", kwargs={'download_id': self.uuid})
