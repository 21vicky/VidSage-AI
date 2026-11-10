
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)



def summarize_transcript(transcript):
    if not transcript or not transcript.strip():
        return "No transcript available to summarize."

    # Limit transcript length for a more reliable API request
    transcript = transcript[:3000]

    prompt = f"""
    You are an expert YouTube video summarization assistant.

    Analyze this transcript and provide:

    1. Short Video Summary
    2. Five Important Key Points
    3. Main Topics Discussed
    4. Important Facts
    5. Simple Conclusion

    Use clear, easy-to-understand English.
    Correct obvious transcription mistakes where possible.
    Do not invent information.

    Transcript:
    {transcript}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            return "Gemini returned an empty response."

        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"
