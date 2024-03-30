#Version 1 :
"""
Extracting the transcript from the youtube video and saving it in a CSV file,
Translating the transcript to English if the original text is not in English
#NOTE: FOCUSES ON THE VIDEO THAT HAS CAPTIONS .
IF THE VIDEO DOESN'T HAVE CAPTIONS, THEN THE TRANSCRIPT WILL BE EMPTY.
UPDATED VERSION IN THE NEXT FILE
"""



from googletrans import Translator, LANGUAGES
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

# Define your YouTube playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLk_Jw3TebqxBqkHI71QhyECXK0vQl2TzZ=en"

# Initialize the translator
translator = Translator()

def get_transcript(video_id):
    languages = ['hi', 'en']  # List of languages to try
    for lang in languages:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            text = ' '.join([line['text'] for line in transcript])
            # Translate to English if the original text is not in English
            if lang != 'en':
                translated = translator.translate(text, dest='en').text
                return translated
            return text
        except Exception as e:
            continue
    return ""

# Extract metadata for each video in the playlist
ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'force_generic_extractor': True,
    'extractor_args': {'youtube:tab': 'videos'},
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(playlist_url, download=False)
    videos = playlist_info['entries']

    # Initialize an empty list to store video data
    video_data = []

    # Loop through each video
    for video in videos:
        video_id = video['id']
        video_title = video['title']
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        video_transcript = get_transcript(video_id)

        video_data.append({
            'Video ID': video_id,
            'Title': video_title,
            'Link': video_link,
            'Transcript': video_transcript
        })

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(video_data)

# Save the DataFrame to a CSV file
df.to_csv('transcription_translated.csv', index=False)