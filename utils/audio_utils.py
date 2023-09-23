# utils/audio_utils

from txtai.pipeline import TextToSpeech
import soundfile as sf
import time

def genAudio(text, audName):

    try:
        tts = TextToSpeech()
        speech = tts(text)
        sf.write(f"audio/{audName}.mp3", speech, 22050)
        print('created')
    except:
        print('failed to create')
        print(text)
        time.sleep(3)
        genAudio(text, audName)