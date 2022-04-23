import pyaudio
import numpy as np
import wave
import collections

from asr import ASR
from spotter import Spotter
from command import Command

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 44100

CHUNK = 4096  # RATE / number of updates per second.

SPOTTER_CHECKS_RATE = 6  # How often spotter will be called.

# The next two lengths use CHUNK/RATE seconds units.
COMMAND_LENGTH = 15

DETAILS_LENGTH = 50

DEQUE = collections.deque(maxlen=COMMAND_LENGTH)

DEQUE_DETAILS = collections.deque(maxlen=DETAILS_LENGTH)

SOUND_SCALE = 1024 * 8


def read_audio_from_stream(pa_stream: pyaudio.Stream) -> np.array:
    """
    Reads audio from pyaudio stream to numpy array.
    @param pa_stream: pyaudio stream.
    @return: clipped and scaled numpy array.
    """
    stream_data = pa_stream.read(CHUNK, exception_on_overflow=False)
    wave_data = wave.struct.unpack("%dh" % CHUNK, stream_data)
    np_array_data = np.array(wave_data, dtype=np.float32)
    np_array_data = np_array_data / SOUND_SCALE
    np_array_data[np_array_data < -1] = -1.0
    np_array_data[np_array_data > 1] = 1.0

    return np_array_data


if __name__ == "__main__":
    spotter = Spotter(RATE)
    asr = ASR()

    p = pyaudio.PyAudio()
    wait = COMMAND_LENGTH
    stream = None

    try:
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=1,
                        )
        cntr = 0
        read_description_on = -1
        while True:
            cntr += 1
            data = read_audio_from_stream(stream)
            DEQUE.append(data)
            DEQUE_DETAILS.append(data)

            if cntr == read_description_on:
                audio = np.array(np.concatenate(list(DEQUE_DETAILS)))
                scaled = np.int16(audio * SOUND_SCALE)
                asr.download_and_play_request(audio)

            if cntr > wait:
                if (cntr % SPOTTER_CHECKS_RATE == 0) and cntr > read_description_on:
                    audio = np.array(np.concatenate(list(DEQUE)))
                    command_id = spotter.spot(audio)
                    if Command.is_play(command_id):
                        print('play')
                        read_description_on = cntr + DETAILS_LENGTH
                    if Command.is_pause(command_id):
                        print('pause')
                        asr.audio_player.pause()
                    if Command.is_resume(command_id):
                        print('resume')
                        asr.audio_player.resume()
    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        p.terminate()
