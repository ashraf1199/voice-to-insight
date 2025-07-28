# audio_recorder.py
import pyaudio
import wave
import threading
import keyboard  # Install with: pip install keyboard

recording = True

def _record_loop(frames, stream, chunk):
    global recording
    while recording:
        data = stream.read(chunk)
        frames.append(data)

def record_from_mic(filename="uploads/recorded.wav"):
    global recording
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    recording = True

    print("🎙️ Recording... Press ENTER to stop")
    thread = threading.Thread(target=_record_loop, args=(frames, stream, chunk))
    thread.start()

    keyboard.wait("enter")  # Wait for ENTER key to stop
    recording = False
    thread.join()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("✅ Recording saved to", filename)
