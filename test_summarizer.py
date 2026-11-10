from transcript import get_transcript
from summarizer import summarize_transcript

url = input("Enter YouTube URL: ")

print("\nExtracting transcript...")

transcript = get_transcript(url)

if transcript.startswith("Transcript extraction failed"):
    print(transcript)

elif transcript == "Invalid YouTube URL":
    print(transcript)

else:
    print("\nGenerating AI summary...")

    summary = summarize_transcript(transcript)

    print("\n===== VIDSAGE AI SUMMARY =====\n")
    print(summary)