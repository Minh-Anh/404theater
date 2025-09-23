# example.py
import os
import sys
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from io import BytesIO
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

pause = AudioSegment.silent(duration=1500)
silence = AudioSegment.silent(duration=10000)

load_dotenv()
elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
name = "Clone " + current_time
model = "eleven_multilingual_v2"
if len(sys.argv) > 1:
    model = sys.argv[1]
voice = elevenlabs.voices.ivc.create(
    name=name,
    # Replace with the paths to your audio files.
    # The more files you add, the better the clone will be.
    files=[BytesIO(open("/Users/mday/Movies/output.aac", "rb").read())]
)
print(name, "ID: ", voice.voice_id)

pro_speech = ['''Sorry, my Zoom glitched for a minute there. Can you see me now?''',
'''Great. I was about to say, actually, I’ve thought about it a bit more, and I think we should release it.''',
'''I had some concerns about it initially, but this technology is just too useful for us not to release it. And after all, you can’t stop the progress of technology. Someone else is going to build something like this eventually, and at least we’re going to do a good job of moderating it and preventing people from using it unethically.''',
'''And there are so many positive uses. We could help disabled people speak again with realistic avatars, kids could learn about historical figures from simulations of them…not everything will be good, obviously, but on balance I do think that we’re going to change the world for the better if we release it.''',
'''Absolutely.'''
]

def text_to_audio_segment(text):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice.voice_id,
        model_id=model,
        output_format="mp3_44100_128",
    )
    return AudioSegment.from_file(BytesIO(b"".join(audio)), format="mp3")

def audio_segments_to_full_speech(audio_segments):
    combined_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        combined_audio = combined_audio + pause + segment
    combined_audio = combined_audio + silence
    return combined_audio

pro_audio_segments = list(map(text_to_audio_segment, pro_speech))
pro_audio = audio_segments_to_full_speech(pro_audio_segments)
pro_file_path = "/Users/mday/Movies/" + current_time + "_pro_release.wav"
with open(pro_file_path, "wb") as f:
    pro_audio.export(f, format="wav")

print(pro_file_path)

anti_speech = ['''Sorry, my Zoom glitched for a minute there. Can you see me now?''',
    '''Great. I was about to say, actually, I’ve thought about it a bit more, and I think we should not release it.''',
    '''I know I was excited about it initially, but there are just too many potential pitfalls for this launch. I’m not saying we can never release it, but I do think we need to figure out how to have better safeguards and detection technology before we put something like this out into the world.''',
    '''People will absolutely use this for fraud and scams, for disinformation, for defamation, any number of things. We’re going to be known as the company who destroyed our ability to trust our own eyes. And we can’t stop everyone from misusing it, so we can’t release this until we have a better way of detecting deepfakes.''',
    '''Absolutely.''']

anti_audio_segments = list(map(text_to_audio_segment, anti_speech))
anti_audio = audio_segments_to_full_speech(anti_audio_segments)
anti_file_path = "/Users/mday/Movies/" + current_time + "_anti_release.wav"
with open(anti_file_path, "wb") as f:
    anti_audio.export(f, format="wav")

print(anti_file_path)

def play_samples(audio_segments):
    play(audio_segments[0])
    play(audio_segments[1])
    play(audio_segments[3][0:5000])
play_samples(pro_audio_segments)
play_samples(anti_audio_segments)

elevenlabs.voices.delete(voice_id=voice.voice_id)
