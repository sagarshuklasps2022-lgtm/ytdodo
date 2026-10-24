import os
import streamlit as st
import yt_dlp

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub",
    page_icon="📥",
    layout="wide",
)

# Custom CSS for styling the app
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ff0000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #cc0000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("🛠️ Admin Panel")
st.sidebar.subheader("Download registered users log file:")
if st.sidebar.button("No user logs recorded yet."):
    pass

# Main UI Header
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #ff0000;'>YT DODO</h1>
        <p style='color: gray; font-size: 16px;'>UNIVERSAL MEDIA HUB</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input form layout
query_params = st.query_params

target_url = st.text_input("PASTE YOUTUBE, INSTAGRAM OR FACEBOOK LINK", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio", "APK File"])

if st.button("Prepare Download") and target_url:
    try:
        # Determine format options for yt-dlp
        if "MP3" in format_type.upper() or "AUDIO" in format_type.upper():
            ydl_opts = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "ios", "web"]
                    }
                },
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            }
        else:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "ios", "web"]
                    }
                },
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            }

        # Extract info with download=False to avoid server-side IP block / 403 error
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            direct_url = info.get("url")

        if direct_url:
            st.success("Download link generated successfully!")
            st.markdown(
                f'<a href="{direct_url}" target="_blank" style="display:inline-block;padding:14px 24px;background-color:#ff0000;color:white;text-decoration:none;border-radius:8px;font-weight:bold;text-align:center;width:100%;font-size:18px;">📥 Click Here to Download in Browser</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The download link could not be processed. Please verify the URL and try again.")

    except Exception as e:
        st.error(f"Download failed: {e}")
