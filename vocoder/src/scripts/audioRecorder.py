import pyaudio
import wave
from pynput.keyboard import Key, Controller, Listener


def winBeep(frequency, duration):
    import winsound
    winsound.Beep(frequency, duration)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

winBeep(700, 800)

def on_press(key):
    data = stream.read(CHUNK)
    frames.append(data)

def on_release(key):
    if key == Key.ctrl_l:
        winBeep(800, 800)
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

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

keyboard = Controller ()# You should only need to define this once
while(True):# This will repeat the indented code below forever   
    break

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)