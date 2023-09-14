import praw
import colorama
import json
from moviepy.editor import *
import re
from gtts import gTTS
import pyttsx3
import time
from ovos_tts_plugin_mimic3_server import Mimic3ServerTTSPlugin
import soundfile as sf
from txtai.pipeline import TextToSpeech

def reddit_obj():

    with open('json-files/credentials.json') as f:
        data = json.load(f)

    user_values = data["api_credentials"]

    reddit = praw.Reddit(
        client_id=user_values['client_id'],
        client_secret=user_values['client_secret'],
        user_agent = user_values['user_agent'],
        password=user_values['password'],
    )

    return reddit


def split_sen(sen):
    split_chars = ['.', ',', ':', ';', '?']
    ignore_chars = { '(', ')', '[', ']'}
    newArr = []
    newLine = ''
    in_quotes_or_brackets = False

    for c in sen:
        newLine += c

        if c in ignore_chars:
            in_quotes_or_brackets = not in_quotes_or_brackets

        if not in_quotes_or_brackets and c in split_chars:
            newArr.append(newLine.strip())
            newLine = ''

    # Append the last part of the sentence if not empty
    if newLine:
        newArr.append(newLine.strip())

    return newArr


redditObj = reddit_obj()
subred = redditObj.subreddit("amitheasshole")

top = subred.top(time_filter = "day", limit = 2)

background = ImageClip("background/bg2.jpg")

for i in top:
    titl = i.title
    desc = i.selftext
    break
print(titl)

tt = Mimic3ServerTTSPlugin()

def genAudio(text, audName):
    # try:
        
    #     tt.get_tts(text, f"audio/{audName}.mp3", voice="en_US/m-ailabs_low#elliot_miller") # specify speaker together with voice
    #     print('created')
    # except Exception as e:
    #     print(e)
    #     print('failed to create, trying again')
    #     print(text)
    #     time.sleep(1)

    #     pass
# genAudio(desc)
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
fontsize = 150
color = "black"
method = "caption"
size = (2000, None)
font="Century-Schoolbook-Roman"

# text_clip = TextClip(titl, fontsize = fontsize, color = color, method = method, size = size, align='center').set_position('center')
# text_clip.duration = 2
# audio_clip = AudioFileClip('audio/audio.mp3')
clips = []
audio_clips = []

split_desc = split_sen(desc)
print(split_desc)
clip_dur = 0
for audName, clip in enumerate(split_desc):
    # clip = clip.replace('\n', '').replace('\r', '')
    genAudio(clip.strip(), audName)
    textclip = TextClip(clip.strip(), fontsize = fontsize, color = color, align='center', size=size, method=method, font = font)
    
    textclip = textclip.set_position(('center', 'center'))
    audio_clip = AudioFileClip(f'audio/{audName}.mp3')
    # textclip.set_audio(audio_clip)
    audio_clips.append(audio_clip)
    clip_dur += audio_clip.duration
    textclip.duration = audio_clip.duration
    clips.append(textclip)
    
    
    
    
videoClips = concatenate_videoclips(clips, method = 'compose').set_position(('center', 'center'))
#
background = background.set_duration(videoClips.duration)

final_vid = CompositeVideoClip([background, videoClips])
final_vid.duration = clip_dur
final_audio = concatenate_audioclips(audio_clips)
# final_audio = CompositeAudioClip([final_audio])
finalVid = final_vid.set_audio(final_audio)
# finalVid = finalVid.fx(vfx.speedx, 1)
finalVid.write_videofile("videos/yt.mp4", threads=4, fps=30,audio_bitrate="128k", bitrate="8000k")

