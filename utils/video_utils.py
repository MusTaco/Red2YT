
from moviepy.editor import *
from .text_utils import split_sen
from .audio_utils import genAudio

fontsize = 150
color = "black"
method = "caption"
size = (2000, None)
font="Century-Schoolbook-Roman"

def create_video(titl, desc):

    # Load background image
    background = ImageClip("background/bg2.jpg")

    # Process the description into segments
    split_desc = split_sen(desc)

    clips = []
    audio_clips = []

    split_desc = split_sen(desc)
    print(split_desc)
    clip_dur = 0
    for audName, clip in enumerate(split_desc):
        genAudio(clip.strip(), audName)
        textclip = TextClip(clip.strip(), fontsize = fontsize, color = color, align='center', size=size, method=method, font = font)
        
        textclip = textclip.set_position(('center', 'center'))
        audio_clip = AudioFileClip(f'audio/{audName}.mp3')
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

