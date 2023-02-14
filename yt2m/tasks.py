import logging
import os
import subprocess

from django.conf import settings

from yt_dlp import YoutubeDL

from yt2m.celery import app
from yt2m.models import Download, STATES
from yt2m.utils import DummyLogger, DummyStore


logger = logging.getLogger(__name__)


@app.task(name="download_and_convert_youtube_video", bind=True)
def download_and_convert_youtube_video(self, uuid):
    self.update_state(meta={'progress': 1})
    d = Download.objects.get(uuid=uuid)

    ds = DummyStore()

    def report_hook(d):
        if d['status'] == "downloading":
            total_bytes = d.get("total_bytes") or d['total_bytes_estimate']
            self.update_state(meta={'progress': max(1, int(70 * d['downloaded_bytes'] / total_bytes))})
        elif d['status'] == 'finished':
            ds.set(d['filename'])
        else:
            logger.error("An error happened during getting the YouTube video: %s", d)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'logger': DummyLogger(),
        'progress_hooks': [report_hook],
        'outtmpl': "/tmp/{}-video.%(ext)s".format(uuid),
    }

    YoutubeDL(ydl_opts).download([d.youtube_id])

    d.state = STATES.CONVERTING
    d.save()

    convert_command = ['ffmpeg', '-i', ds.filename]
    if d.cut_start or d.cut_end:
        convert_command.extend(["-ss", str(d.cut_start or 0), '-to', str(d.cut_end or d.youtube_duration)])
    convert_command.append(os.path.join(settings.MP3_DIRECTORY, f"{uuid}.mp3"))

    result = subprocess.run(convert_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        d.state = STATES.ERROR
        d.error = "stdout: %s\nstderr: %s" % (result.stdout, result.stderr)
        logger.error(d.error)
        d.save()
    else:
        d.state = STATES.SUCCESS
        d.save()

    os.remove(ds.filename)
