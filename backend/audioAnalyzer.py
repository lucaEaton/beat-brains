import math

import os
os.environ["LIBROSA_CACHE_DIR"] = "/tmp"
os.environ["LIBROSA_NO_CACHE"] = "1"

import librosa
from librosa import feature

import numpy as np

KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


class AudioAnalyzer:
    # Set Path File
    def __init__(self, file_path):
        self.filePath = file_path

    # Loads the audio, and if it exists get the sample rate and
    def _load_audio(self):
        if not os.path.exists(self.filePath):
            raise FileNotFoundError(f"Audio file not found at: {self.filePath}")

        try:
            y, sr = librosa.load(self.filePath, sr=None)
            return y, sr
        except Exception as e:
            raise IOError(f"Failed to load audio file using Librosa. Error: {e}")

    # By rounding the tempo down provided by .beat_track
    # We are able to find the BPM within a ~1bpm range.
    @staticmethod
    def _extract_tempo(y, sr):
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return math.floor(tempo.item())

    # Using chroma features, we find the correlation within our song file
    # and find which correlation fits best with one of the keynotes
    @staticmethod
    def _extract_key(y, sr):
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_vals = np.sum(chroma, axis=1)
        most_common_pc = np.argmax(chroma_vals)
        key = KEYS[most_common_pc]
        return key

    # Creates a dictionary, needed to give to our Gemini AI prompt.
    def get_analysis(self):
        y, sr = self._load_audio()
        bpm_value = self._extract_tempo(y, sr)
        key_value = self._extract_key(y, sr)

        audio_dictionary = {
            "BPM": bpm_value,
            "Key Value": key_value
        }

        return audio_dictionary

# def main():

# filename = "test_audio/John Lennon - Original Imagine Music Video 1971.mp3"
# audio = AudioAnalyzer(file_path=filename)

# print(audio.get_analysis())


# if __name__ == "__main__":
#  main()
