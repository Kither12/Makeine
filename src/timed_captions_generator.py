import whisper_timestamped as whisper
from whisper_timestamped import load_model, transcribe_timestamped
import re


def generate_timed_captions(audio_filename, model_size="base"):
    WHISPER_MODEL = load_model(model_size)

    gen = transcribe_timestamped(
        WHISPER_MODEL, audio_filename, verbose=False, fp16=False)

    return getCaptionsWithTime(gen)


def splitWordsBySize(words, maxCaptionSize):

    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions


def getTimestampMapping(whisper_analysis):

    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            newIndex = index + len(word['text'])+1
            locationToTimestamp[(index, newIndex)] = word['end']
            index = newIndex
    return locationToTimestamp


def cleanWord(word):

    return re.sub(r'[^\w\s\-_"\'\']', '', word)


def interpolateTimeFromDict(word_position, d):

    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None


def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, maxWordsSize=45):

    wordLocationToTime = getTimestampMapping(whisper_analysis)
    VideoPairs = []
    CaptionsPairs = []
    text = whisper_analysis['text']

    sentences = re.split(r'(?<=[.!?]) +', text)
    captions = [word for sentence in sentences for word in splitWordsBySize(
        sentence.split(), maxCaptionSize)]
    words = [word for sentence in sentences for word in splitWordsBySize(
        sentence.split(), maxWordsSize)]

    position = 0
    start_time = 0
    end_time = 0
    for word in captions:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if end_time and word:
            CaptionsPairs.append(((start_time, end_time), word))
            start_time = end_time

    position = 0
    start_time = 0
    end_time = 0
    for sentence in words:
        position += len(sentence) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if end_time and sentence:
            VideoPairs.append(((start_time, end_time), sentence))
            start_time = end_time

    return (CaptionsPairs, VideoPairs)
