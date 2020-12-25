import pyaudio
import wave
from pynput.keyboard import Key, Controller, Listener
import os

onMac = True if os.name == 'posix' else False

def beep(bp):
    if not onMac:
        import winsound
        winsound.Beep(1000, 850)
    else:
        bipf = wave.open('../../beep.wav', 'rb')
        bipstream = bp.open(format=bp.get_format_from_width(bipf.getsampwidth()),
                        channels=bipf.getnchannels(),
                        rate=bipf.getframerate(),
                        output=True)
        bipdata = bipf.readframes(1024)
        while bipdata!= b'':
            bipstream.write(bipdata)
            bipdata = bipf.readframes(1024)
        bipstream.stop_stream()
        bipstream.close()
        bipf.close()

p = pyaudio.PyAudio()

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

def on_press(key):
    data = stream.read(CHUNK)
    frames.append(data)

def on_release(key):
    if key == Key.ctrl_l:
        beep(p)
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return False

beep(p)
# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

keyboard = Controller ()