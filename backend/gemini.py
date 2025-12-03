import os
import json
from google import genai
from backend.audioAnalyzer import AudioAnalyzer

class GeminiClient:
    def __init__(self, api_key_env_var: str = "GEMINI_API_KEY", model_name: str = 'gemini-2.5-flash'):
        self.client = genai.Client(api_key=os.getenv(api_key_env_var))
        self.model = model_name

    def build_response(self, file_name: str) -> str:
        audio = AudioAnalyzer(file_path=file_name)
        audio_dictionary = audio.get_analysis()
        prompt = (
            "Act as a Master DJ Analyst specializing in dance music and music theory. "
            "Your task is to provide a comprehensive, actionable analysis for the track "
            f"'{file_name}' based on the provided technical data.\n\n"
            "Technical Data:\n"
            f"{json.dumps(audio_dictionary, indent=2)}\n\n"
            "Provide the analysis in the following strict, structured format. "
            "Do not include any introductory or concluding sentences outside of the requested sections. "
            "Provide a concise, engaging description of the track's mood, energy, and best use case "
            "(e.g., peak-time banger, warm-up groove, late-night deep cut). "
            "Mention the found tempo and key value of the provided audio and talk about about the song in one "
            "sentence.\n"
            "Base this strictly on the provided BPM and key.\n"
            "- Recommended Transition BPM Range: Suggest a tight range for pitch correction "
            "(e.g., 127.5 BPM to 135.0 BPM).\n"
            "- Harmonic Mixing Keys: Suggest 2-3 compatible next keys/scales using the Camelot Wheel logic "
            "(e.g., if input is 8A, suggest 7A, 8B, 9A). Assume the user understands this notation "
            "Assign a grade (A, B, or C) for the track's overall mix-ability and complexity and why "
            "(A=Easy/Perfect Loop, B=Standard Complexity, C=Tricky/Lots of vocals).\n"
            "Provide one short, actionable piece of advice specific to mixing this track "
            "(e.g., 'Use a high-pass filter for a smooth entrance')."
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

def main():
    #testing purposes
   filename = "../test_audio/John Lennon - Original Imagine Music Video 1971.mp3"
   gemini_client = GeminiClient(model_name='gemini-2.5-flash')

   print(gemini_client.build_response(file_name=filename))


if __name__ == "__main__":
    main()
