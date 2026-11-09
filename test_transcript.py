from transcript import get_transcript

url = input("Enter YouTube URL: ")

result = get_transcript(url)

print("\n===== VIDEO TRANSCRIPT =====\n")

print(result)