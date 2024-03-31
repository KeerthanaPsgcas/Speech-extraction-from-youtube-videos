"""In this app, we will create a Streamlit app that can fetch the transcript of a YouTube video 
or a playlist of videos. We will use the `pytube` library to fetch the video details.
The `youtube_transcript_api` library will be used to fetch the transcript of the video.
We will also use the `googletrans` library to translate the transcript to English if it is not in English.
The app will take a YouTube video URL or a playlist URL as input and display the video details and transcript and
 provide an option to download the transcript as a CSV file.
"""

import streamlit as st
import re
from googletrans import Translator
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import pandas as pd
from pytube import Playlist

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

def main():
    st.title('YouTube Playlist / Video Fetcher')
    
    url = st.text_input('Enter YouTube Playlist or Video URL:')
    
    if url:
        try:
            if 'playlist' in url.lower():
                playlist = Playlist(url)
                st.write(f'Found {len(playlist.video_urls)} videos in the playlist.')
                
                if st.button('Download Playlist CSV'):
                    video_data = []
                    for video_url in playlist.video_urls:
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

                    df = pd.DataFrame(video_data)
                    st.write(df)  # Display DataFrame

                    # Create a link to download the CSV file
                    csv_link = df.to_csv(index=False)
                    # st.markdown(f'<a href="data:file/csv;base64,{csv_link.encode().decode()}" download="playlist_data.csv">Download CSV</a>', unsafe_allow_html=True)
            
            else:
                yt = YouTube(url)
                video_id = yt.video_id
                video_title = yt.title
                video_link = yt.watch_url
                video_posted_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else ''
                video_transcript = get_transcript(video_id)

                st.write('Video Details:')
                st.write(f'Video ID: {video_id}')
                st.write(f'Title: {video_title}')
                st.write(f'Link: {video_link}')
                st.write(f'Posted Date: {video_posted_date}')
                st.write(f'Transcript: {video_transcript}')

  
              
        except Exception as e:
            st.error('Error fetching data. Please check the URL.')



if __name__ == '__main__':
    main()
