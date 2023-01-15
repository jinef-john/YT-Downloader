import streamlit as st
import youtube_dl
from PIL import Image
import io
import urllib.request

st.set_page_config(page_title="YouTube Downloader", page_icon=":video_camera:", layout="wide")

def download_video(url, download_format):
    ydl_opts = {}
    if download_format == "Audio":
        ydl_opts["format"] = "bestaudio/best"
    else:
        ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if 'playlist' in url:
            info = ydl.extract_info(url, download=False)
            st.write("Downloading playlist with {} videos".format(len(info['entries'])))
            for video in info['entries']:
                st.write("Downloading {}".format(video['title']))
                ydl.download([video['url']])
        else:
            ydl.download([url])
        st.success("Download complete!")

def get_thumbnail(url):
    ydl = youtube_dl.YoutubeDL({'quiet': True})
    info = ydl.extract_info(url, download=False)
    return info['thumbnail']

def show_thumbnail(thumbnail_url):
    image_bytes = urllib.request.urlopen(thumbnail_url).read()
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption='Video Thumbnail', use_column_width=True)

url = st.text_input("Enter the URL of the YouTube video/playlist:")
download_format = st.selectbox("Select the download format:", ["Video", "Audio"])

if url:
    thumbnail_url = get_thumbnail(url)
    show_thumbnail(thumbnail_url)

if st.button("Download"):
    download_video(url, download_format)
