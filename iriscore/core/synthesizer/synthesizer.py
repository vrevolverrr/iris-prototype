import numpy
import torch
from scipy.io import wavfile
from TTS.utils.audio import AudioProcessor
from TTS.utils.io import AttrDict, load_config
from TTS.vocoder.utils.generic_utils import setup_generator
from TTS.tts.utils.generic_utils import setup_model
from TTS.tts.utils.synthesis import synthesis
from TTS.tts.utils.text.symbols import symbols, phonemes

class Synthesizer:
    def __init__(self):
        TTS_MODEL_PATH = "./iriscore/core/synthesizer/model/tts_model.pth.tar"
        TTS_CONFIG_PATH = "./iriscore/core/synthesizer/model/config.json"
        VOCODER_MODEL_PATH = "./iriscore/core/synthesizer/model/vocoder/vocoder_model.pth.tar"
        VOCODER_CONFIG_PATH = "./iriscore/core/synthesizer/model/vocoder/config.json"

        self.TTS_CONFIG: AttrDict = load_config(TTS_CONFIG_PATH)
        self.VOCODER_CONFIG: AttrDict = load_config(VOCODER_CONFIG_PATH)

        self.TTS_CONFIG["audio"]["stats_path"] = "./iriscore/core/synthesizer/model/scale_stats.npy"
        self.audio_processor = AudioProcessor(**self.TTS_CONFIG["audio"])

        speakers = []

        num_chars = len(phonemes) if self.TTS_CONFIG["use_phonemes"] else len(symbols)
        self.model = setup_model(num_chars, len(speakers), self.TTS_CONFIG)

        cp =  torch.load(TTS_MODEL_PATH, map_location=torch.device('cpu'))

        self.model.load_state_dict(cp['model'])
        self.model.eval()

        if 'r' in cp:
            self.model.decoder.set_r(cp['r'])

        self.vocoder_model = setup_generator(self.VOCODER_CONFIG)
        self.vocoder_model.load_state_dict(torch.load(VOCODER_MODEL_PATH, map_location="cpu")["model"])
        self.vocoder_model.remove_weight_norm()
        self.vocoder_model.inference_padding = 0

        ap_vocoder = AudioProcessor(**self.VOCODER_CONFIG['audio'])
        self.vocoder_model.eval()

    def synthesize_speech(self, text):
        waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(self.model, text, self.TTS_CONFIG, False, self.audio_processor, None, style_wav=None, truncated=False, enable_eos_bos_chars=self.TTS_CONFIG["enable_eos_bos_chars"])

        waveform: numpy.ndarray = self.vocoder_model.inference(torch.FloatTensor(mel_postnet_spec.T).unsqueeze(0))
        waveform = waveform.flatten()
        waveform = waveform.numpy()
        
        return waveform.tobytes()

    def save_as_wave(self, data):
        wavfile.write("test.wav", 22050, data)
