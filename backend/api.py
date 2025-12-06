import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from gemini import GeminiClient

load_dotenv()
load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "/.env"
    )
)

app = FastAPI()

#allowing all methods n urls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_client = GeminiClient(model_name="gemini-2.5-flash")

# api magic
@app.post("/analyze")
async def analyze_track(file: UploadFile = File(...)):
    # catch if the key isn't set up or can't read ./.env file
    if not gemini_client:
        return {"error": "Gemini API Key not set."}

    # creates a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp:
        content = await file.read()
        temp.write(content)
        temp_name = temp.name

    try:
        # plugs temp file into the gemini.api .build_response function and returns as a json file for App.tsx to read
        result_text = gemini_client.build_response(temp_name)
        return {"result": result_text}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # removes temp file from mem
        if os.path.exists(temp_name):
            os.remove(temp_name)
