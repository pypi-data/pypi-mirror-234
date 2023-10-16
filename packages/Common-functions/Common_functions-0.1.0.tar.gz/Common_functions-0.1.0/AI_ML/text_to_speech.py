from gtts import gTTS
import playsound
import multiprocessing
from playsound import playsound



def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    p = multiprocessing.Process(target=playsound, args=(filename))
    p.start()
    input("press ENTER to stop playback")
    p.terminate()
