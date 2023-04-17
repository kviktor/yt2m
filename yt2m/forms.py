import logging

from django.forms import Form, CharField, ValidationError
from django.conf import settings

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from yt2m.utils import DummyLogger


logger = logging.getLogger(__name__)


class YouTubeDownloadForm(Form):
    cut_start = CharField(required=False)
    cut_end = CharField(required=False)
    youtube_uri = CharField(
        required=True,
        error_messages={"required": "Please enter a valid YouTube video URL or ID."},
    )

    def clean_youtube_uri(self):
        uri = self.cleaned_data["youtube_uri"]

        try:
            ydl = YoutubeDL({"noplaylist": True, "logger": DummyLogger()})
            result = ydl.extract_info(uri, download=False)
        except YoutubeDLError:
            logger.exception("youtube dl error")
            raise ValidationError("Could not find the YouTube video on that URL.")

        return {
            "duration": result["duration"],
            "youtube_id": result["id"],
            "title": result["title"],
            "thumbnail": result["thumbnail"],
        }

    def clean_cut_start(self):
        cut_start = self.cleaned_data["cut_start"]
        if not cut_start:
            return None

        try:
            cut_start = int(cut_start)
        except ValueError:
            try:
                split = cut_start.split(":")
                cut_start = int(split[0]) * 60 + int(split[1])
            except (ValueError, IndexError):
                raise ValidationError(
                    "%s is not a valid start value, "
                    "either provide in seconds or mm:ss format" % cut_start
                )

        return cut_start

    def clean_cut_end(self):
        cut_end = self.cleaned_data["cut_end"]
        if not cut_end:
            return None

        try:
            cut_end = int(cut_end)
        except ValueError:
            try:
                split = cut_end.split(":")
                cut_end = int(split[0]) * 60 + int(split[1])
            except (ValueError, IndexError):
                raise ValidationError(
                    "%(cut_end)s is not a valid end value, "
                    "either provide in seconds or mm:ss format",
                    params={"cut_end": cut_end},
                )

        return cut_end

    def clean(self):
        data = super().clean()

        if data.get("youtube_uri"):
            cut_start = data.get("cut_start")
            cut_end = data.get("cut_end")
            duration = data["youtube_uri"]["duration"]
            title = data["youtube_uri"]["title"]

            if cut_start is not None:
                if cut_start > duration:
                    raise ValidationError(
                        "Cut start must be lower than the video's duration"
                    )

            if cut_end is not None:
                if cut_end > duration:
                    raise ValidationError(
                        "Cut end must be lower than the video's duration"
                    )

            if cut_start and cut_end and cut_start > cut_end:
                raise ValidationError("Cut end must have a higher value than cut end")

            if duration > settings.MAX_VIDEO_DURATION:
                raise ValidationError(
                    "%(title)s is too long, can't convert it to an audio file.",
                    params={"title": title},
                )
