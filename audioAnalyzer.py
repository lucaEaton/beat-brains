import librosa
from librosa import feature
import os


class AudioAnalyzer:
    def __init__(self, file_path):
        self.filePath = file_path

    def _load_audio(self):
        if not os.path.exists(self.filePath):
            raise FileNotFoundError(f"Audio file not found at: {self.filePath}")

        try:
            y, sr = librosa.load(self.filePath, sr=None)
            return y, sr
        except Exception as e:
            raise IOError(f"Failed to load audio file using Librosa. Error: {e}")

    @staticmethod
    def _extract_tempo(y, sr):
        return round(float(librosa.beat.tempo(y=y, sr=sr)), 2)

    # Doesnt Work
    @staticmethod
    def _extract_key(y, sr):
        return librosa.feature.chroma_stft(y=sr, sr=sr)

    def get_analysis(self):
        audio_y, audio_sr = self._load_audio()
        bpm_value = self._extract_tempo(audio_y, audio_sr)
        key_value = self._extract_key(audio_y, audio_sr)

        audio_dictionary = {
            "BPM": bpm_value,
            "Key Value": key_value
        }

        return audio_dictionary
