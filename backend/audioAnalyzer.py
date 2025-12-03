import math
import librosa
from librosa import feature
import numpy as np
import os


KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        return math.floor(tempo.item())

    # Doesnt Work
    @staticmethod
    def _extract_key(y, sr):
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_vals = np.sum(chroma, axis=1)
        most_common_pc = np.argmax(chroma_vals)
        key = KEYS[most_common_pc]
        return key

    def get_analysis(self):
        y, sr = self._load_audio()
        bpm_value = self._extract_tempo(y, sr)
        key_value = self._extract_key(y, sr)

        audio_dictionary = {
            "BPM": bpm_value,
            "Key Value": key_value
        }

        return audio_dictionary



#def main():

    #filename = "test_audio/John Lennon - Original Imagine Music Video 1971.mp3"
    #audio = AudioAnalyzer(file_path=filename)

    #print(audio.get_analysis())


#if __name__ == "__main__":
  #  main()
