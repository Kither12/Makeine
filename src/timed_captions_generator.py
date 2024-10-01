import whisper
import re


def generate_timed_captions(audio_filename, model_size="small"):
    transcript = whisper.load_model(model_size).transcribe(word_timestamps=True, audio=audio_filename, condition_on_previous_text = False)

    return getCaptionsWithTime(transcript)


def splitWordsBySize(words, maxCaptionSize):

    captions = []
    cur_caption = ""
    for i, word in enumerate(words):
        if len(cur_caption) < maxCaptionSize:
            if cur_caption != "":
                cur_caption += " "
            cur_caption += word
        else:
            captions.append((cur_caption, i))
            cur_caption = word
    captions.append((cur_caption, len(words)))
    return captions

def get_end_time_segment(w, transcript):
    cnt = 0
    for segment in transcript["segments"]:
        for word_segment in segment["words"]:
            cnt += 1
            if w == cnt:
                return word_segment["end"]
    return None


def getCaptionsWithTime(transcript, maxCaptionSize=15, maxWordsSize=45):

    VideoPairs = []
    CaptionsPairs = []

    word_text = [word_segment["word"] for segment in transcript["segments"] for word_segment in segment["words"]]

    captions = splitWordsBySize(word_text, maxCaptionSize)
    words = splitWordsBySize(word_text, maxWordsSize)

    start_time = 0
    end_time = 0
    cnt = 0
    for word, i in captions:
        end_time = get_end_time_segment(i, transcript)
        CaptionsPairs.append(((start_time, end_time), word))
        start_time = end_time
    start_time = 0
    end_time = 0
    for sentence, i in words:
        end_time = get_end_time_segment(i, transcript)
        VideoPairs.append(((start_time, end_time), sentence))
        start_time = end_time

    return CaptionsPairs, VideoPairs
