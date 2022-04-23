from typing import Optional

import onnxruntime
import numpy as np
import torch
import torchaudio
import torchaudio.functional as F

DEFAULT_SR = 16000

COMMAND_MIN_TOLERANCE = 6.0


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


class Spotter:
    """
    Speach command spotter.
    """

    def __init__(self, sr):
        self.sr = sr  # Speech rate.
        self.ort_session = onnxruntime.InferenceSession('detect_command.onnx')
        self.prepare_fun = torchaudio.transforms.MFCC(melkwargs={'n_mels': 128, 'hop_length': 160, 'n_fft': 800},
                                                      n_mfcc=40)

    def spot(self, np_audio: np.array) -> Optional[int]:
        """
        Parses command from np array.
        @param np_audio: audio data as numpy array.
        @return: command id or None.
        """
        audio = torch.from_numpy(np_audio)
        if self.sr != DEFAULT_SR:
            audio = F.resample(audio, self.sr, DEFAULT_SR, lowpass_filter_width=18)

        clean_features = self.prepare_fun(audio)
        clean_features = torch.unsqueeze(clean_features, 0)

        # Compute ONNX Runtime output prediction.
        ort_inputs = {self.ort_session.get_inputs()[0].name: clean_features.detach().cpu().numpy()}
        ort_outs = self.ort_session.run(None, ort_inputs)
        id = int(np.argmax(ort_outs[0]))

        if (np.max(ort_outs[0])) > COMMAND_MIN_TOLERANCE:
            return id

        return None
