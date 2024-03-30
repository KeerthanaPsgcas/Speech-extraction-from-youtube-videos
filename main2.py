from googletrans import Translator
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import pandas as pd
from pytube import Playlist

playlist = Playlist("https://www.youtube.com/playlist?list=PLBG6UuYpOcTvg9ALz7cJelclMi1oc7TQp")

def translate_hindi_to_english(text):
    translator = Translator()
    chunk_size = 500  # Number of characters per chunk
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []
    for chunk in chunks:
        translated = translator.translate(chunk, src='hi', dest='en')
        translated_chunks.append(translated.text)
    return ' '.join(translated_chunks)

def get_transcript(video_id):
    languages = ['hi', 'en']  # List of languages to try
    for lang in languages:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            text = ' '.join([line['text'] for line in transcript])
            # Translate to English if the original text is not in English
            if lang != 'en':
                translated = translate_hindi_to_english(text)
                return translated
            return text
        except Exception as e:
            continue
    return ""

# Initialize an empty list to store video data
video_data = []

# Loop through each video URL
for video_url in playlist.video_urls:
    print(video_url)
    yt = YouTube(video_url)
    video_id = yt.video_id
    video_title = yt.title
    video_link = yt.watch_url
    video_posted_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else ''
    video_transcript = get_transcript(video_id)

    video_data.append({
        'Video ID': video_id,
        'Title': video_title,
        'Link': video_link,
        'Posted Date': video_posted_date,
        'Transcript': video_transcript
    })

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(video_data)

# Save the DataFrame to a CSV file
df.to_csv('final_date_mann_ki_batt.csv', index=False)

