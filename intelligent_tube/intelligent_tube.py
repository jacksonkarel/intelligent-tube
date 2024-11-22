import streamlit as st
from googleapiclient.discovery import build
import openai
import os

# Function to search YouTube
def search_youtube(query, max_results=10):
    youtube = build('youtube', 'v3', developerKey=os.getenv('GOOGLE_API_KEY'))
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video_data = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'video_id': item['id']['videoId'],
            'thumbnail': item['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)
    return videos

# Function to filter videos using LLM
def filter_videos(videos):
    filtered_videos = []
    for video in videos:
        content = f"Title: {video['title']}\nDescription: {video['description']}"
        prompt = f"""
Determine if the following YouTube video content is intellectual.

Content:
{content}

Answer with 'Yes' if it is intellectual, or 'No' if it is not.
"""
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=5,
                n=1,
                stop=None,
                temperature=0
            )
            answer = response.choices[0].text.strip()
            if answer.lower() == 'yes':
                filtered_videos.append(video)
        except Exception as e:
            st.error(f"Error filtering video: {e}")
    return filtered_videos

# Streamlit App
def main():
    st.title("Intellectual YouTube Search")
    query = st.text_input("Enter a search term:")
    if query:
        with st.spinner('Searching YouTube...'):
            videos = search_youtube(query)
        with st.spinner('Filtering videos...'):
            filtered_videos = videos
        st.success(f"Found {len(filtered_videos)} intellectual videos.")
        for video in filtered_videos:
            st.image(video['thumbnail'], width=320)
            st.write(f"**{video['title']}**")
            st.write(f"https://www.youtube.com/watch?v={video['video_id']}")
            st.write("---")

if __name__ == "__main__":
    main()
