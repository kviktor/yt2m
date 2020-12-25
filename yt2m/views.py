from urllib.parse import quote
import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from yt2m.forms import YouTubeDownloadForm
from yt2m.models import Download, STATES
from yt2m.tasks import download_and_convert_youtube_video
from yt2m.utils import get_progress


def index(request):
    return render(request, "index.html", {})


def start_download(request):
    form = YouTubeDownloadForm(request.POST)
    if not form.is_valid():
        for field, errors in form.errors.as_data().items():
            for error in errors:
                messages.error(request, error.message % (error.params or {}))

        return redirect("index")

    d = form.cleaned_data['youtube_uri']
    obj = Download.objects.create(
        youtube_id=d['youtube_id'],
        youtube_title=d['title'],
        youtube_duration=d['duration'],
        youtube_thumbnail=d['thumbnail'],
        cut_start=form.cleaned_data.get("cut_start"),
        cut_end=form.cleaned_data.get("cut_end"),
    )

    result = download_and_convert_youtube_video.apply_async((obj.uuid, ))
    obj.task_id = result.id
    obj.save()

    return redirect(obj)


def download(request, download_id):
    obj = get_object_or_404(Download, uuid=download_id)
    progress = get_progress(obj)

    return render(request, "download.html", {'object': obj, 'progress': progress})


def ajax_download(request, download_id):
    obj = get_object_or_404(Download, uuid=download_id)
    progress = get_progress(obj)

    return JsonResponse({
        'progress': progress,
        'readable_state': obj.get_state_display(),
        'state': obj.state},
    )


def download_audio(request, download_id):
    obj = get_object_or_404(Download, uuid=download_id)
    if obj.in_progress or obj.state != STATES.SUCCESS:
        return redirect(obj)

    return FileResponse(
        open(os.path.join(settings.MP3_DIRECTORY, f"{obj.uuid}.mp3"), "rb"),
        as_attachment=True,
        filename=f'{quote(obj.youtube_title)}.mp3',
    )
