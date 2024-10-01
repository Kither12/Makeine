from src.generate_audio import generate_audio
from src.timed_captions_generator import generate_timed_captions
from src.render_engine import get_output_media
from src.story_generator import generate_script
from src.video_prompt_generator import getVideoPromptTimed, generateMainKeyWords

import asyncio


def generate_video(script):
    SAMPLE_FILE_NAME = "audio_tts.wav"

    if script == None:
        script = generate_script()
    print(script)

    asyncio.run(generate_audio(script, SAMPLE_FILE_NAME))

    timed_captions, timed_videos = generate_timed_captions(SAMPLE_FILE_NAME)
    prompt_terms = getVideoPromptTimed(script, timed_videos)
    uvideo = get_output_media(
        SAMPLE_FILE_NAME, timed_captions, prompt_terms)
