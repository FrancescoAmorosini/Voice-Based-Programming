import pyaudio
import wave

def beep():
    bipf = wave.open('../../bip.wav', 'rb')
    bp = pyaudio.PyAudio()
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
    bp.terminate()
    bipf.close()


beep()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

beep()

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
