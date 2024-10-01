import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from src.gif_generator import GifGenerator

def remove_redundant_spaces_and_newlines(input_string):
    return ' '.join(input_string.replace('\n', ' ').split())

def search_program(program_name):
    try:
        search_cmd = "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None


def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path


def get_output_media(audio_file_path, timed_captions, background_video_data):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    magick_path = get_program_path("magick")
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
    else:
        os.environ['IMAGEMAGICK_BINARY'] = '/usr/bin/convert'

    gif_generator = GifGenerator()
    visual_clips = []
    for (t1, t2), prompt in background_video_data:
        video_filename = tempfile.NamedTemporaryFile(
            delete=False, suffix=".gif").name
        gif_generator.generate_gif(prompt + " , realistic, high quality", video_filename)
        video_clip = VideoFileClip(video_filename)
        video_clip = video_clip.set_start(t1)
        video_clip = video_clip.set_end(t2)
        visual_clips.append(video_clip)

    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    for (t1, t2), text in timed_captions:
        text_clip = TextClip(txt=remove_redundant_spaces_and_newlines(text), fontsize=40, color="white",
                             stroke_width=1, stroke_color="black", method="caption", font='JetBrains-Mono-Bold-Nerd-Font-Complete', align='center')
        text_clip = text_clip.set_start(t1)
        text_clip = text_clip.set_end(t2)
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)

    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.duration = audio.duration
        video.audio = audio

    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264',
                          audio_codec='aac', fps=25, preset='veryfast')

    # Clean up downloaded files
    for (t1, t2), video_url in background_video_data:
        video_filename = tempfile.NamedTemporaryFile(delete=False).name
        os.remove(video_filename)

    return OUTPUT_FILE_NAME
