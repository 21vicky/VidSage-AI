from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url):
    pattern = r"(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?]+)"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


def get_transcript(video_url):
    video_id = extract_video_id(video_url)

    if not video_id:
        return "Invalid YouTube URL"

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        full_text = " ".join(
            snippet.text for snippet in transcript
        )

        return full_text

    except Exception as e:
        return f"Transcript extraction failed: {str(e)}"