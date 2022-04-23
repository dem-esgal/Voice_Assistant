import numpy as np
import shutil
import os
import torch
from transliterate import translit

from download_youtube import search_yt, download_yt, OUTPUT_TEMPLATE, MAX_SONG_DURATION
from audio_player import AudioPlayer, DB_PATH
from vad_utils import get_speech_ts, read_audio_from_np

torch.set_num_threads(1)
device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU

# Min search command frame length.
MIN_SEARCH_LENGTH = 20000


class ASR:
    """
    Speech recognition and voice activity detection
    """

    def __init__(self):
        self.model_vad = torch.jit.load('vad.jit')
        self.model_vad.eval()

        self.model_cls, self.decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                             model='silero_stt',
                                                             language='ua',  # also available 'de', 'es'
                                                             device=device)

        # (self.read_batch, self.split_into_batches, self.read_audio_, self.prepare_model_input) = utils
        # see function signature for details
        self.audio_player = AudioPlayer()

    def download_and_play_request(self, speech_command_data: np.array) -> None:
        """
        Downloads media from YouTube and plays it with AudioPlayer.
        @param speech_command_data: search music command as np.array.
        """
        wav = read_audio_from_np(speech_command_data)
        speech_timestamps = get_speech_ts(wav, self.model_vad, num_steps=4)

        soundtrack = ''
        max_wav_sample_length = 0

        # Search for the longest command text
        for timestamp in speech_timestamps:
            wav_sample = wav[timestamp['start']:timestamp['end']]
            wav_sample_length = wav_sample.shape[0]
            if wav_sample_length > max_wav_sample_length:
                max_wav_sample_length = wav_sample_length
                if wav_sample_length > MIN_SEARCH_LENGTH:
                    wav_sample = wav_sample.unsqueeze(0)
                    output = self.model_cls(wav_sample)
                    soundtrack = self.decoder(output[0].cpu())
                    print(soundtrack)

        if len(soundtrack) > 0:
            translitted = translit(soundtrack, language_code='uk', reversed=True)
            db_path = os.path.join(DB_PATH, f'{translitted}.webm')
            if os.path.exists(db_path):
                self.audio_player.play_db_path(db_path)
            else:
                try:
                    results = search_yt(soundtrack, MAX_SONG_DURATION)
                except:
                    results = []

                if len(results) > 0:
                    print(results['webpage_url'])
                    url = results['webpage_url']
                    if os.path.exists(OUTPUT_TEMPLATE):
                        os.remove(OUTPUT_TEMPLATE)
                    try:
                        download_yt(url)
                        db_path = os.path.join(DB_PATH, f'{translitted}.webm')
                        shutil.move(OUTPUT_TEMPLATE, db_path)
                        self.audio_player.play_db_path(db_path)
                    except:
                        pass
