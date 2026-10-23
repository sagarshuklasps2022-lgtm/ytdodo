import os
import streamlit as st
import yt_dlp
import requests

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub",
    page_icon="📥",
    layout="wide",
)

# Custom CSS & Styling
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

# Sidebar / Admin Panel
st.sidebar.title("🛠️ Admin Panel")
st.sidebar.subheader("Download registered users log file:")
if st.sidebar.button("No user logs recorded yet."):
    pass

# Function to shorten URL using ShrinkMe API
def shorten_with_shrinkme(long_url):
    api_token = "5993c830ec96cd0e9e4731657116fce22629f311"
    api_url = f"https://shrinkme.io/api?api={api_token}&url={long_url}&format=text"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text.strip()
    except Exception:
        pass
    return long_url

# --- HEADER & PROFILE BAR ---
header_html = """
<div class="max-w-4xl mx-auto p-4">
    <div class="flex justify-between items-center bg-[#161b22] p-4 rounded-xl border border-gray-800 mb-6 shadow-lg" style="display: flex; justify-content: space-between; align-items: center; background-color: #161b22; padding: 16px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color: #dc2626; padding: 10px; border-radius: 8px; color: white; font-size: 20px;">
                ⚡
            </div>
            <div>
                <h1 style="color: white; font-weight: bold; font-size: 18px; margin: 0;">YT DODO</h1>
                <p style="color: #9ca3af; font-size: 12px; margin: 0;">Welcome, Sagar Shukla</p>
            </div>
        </div>
        <div style="display: flex; gap: 8px;">
            <button style="background-color: #21262d; border: none; padding: 8px 12px; border-radius: 8px; color: #d1d5db; cursor: pointer;">👤</button>
            <button style="background-color: #21262d; border: none; padding: 8px 12px; border-radius: 8px; color: #d1d5db; cursor: pointer;">⚙️</button>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --- QUICK SHORTCUTS SECTION ---
shortcuts_html = """
<div class="max-w-4xl mx-auto p-4" style="margin-top: -20px;">
    <div style="background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 24px;">
        <h2 style="color: #9ca3af; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Quick Platforms & Shortcuts</h2>
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;">
            <a href="https://www.youtube.com" target="_blank" style="background-color: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; color: white; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">🔴 YouTube</a>
            <a href="https://www.google.com" target="_blank" style="background-color: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; color: white; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">🔵 Google</a>
            <a href="https://www.facebook.com" target="_blank" style="background-color: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; color: white; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">📘 Facebook</a>
            <a href="https://www.instagram.com" target="_blank" style="background-color: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; color: white; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">📸 Instagram</a>
            <a href="https://twitter.com" target="_blank" style="background-color: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 8px; text-align: center; color: white; text-decoration: none; font-size: 12px; font-weight: 600; display: block;">🐦 Twitter</a>
        </div>
    </div>
</div>
"""
st.markdown(shortcuts_html, unsafe_allow_html=True)

# --- SEARCH & DOWNLOAD HUB ---
st.markdown("### 🔍 SEARCH & DOWNLOAD HUB")
target_url = st.text_input("PASTE YOUTUBE, INSTAGRAM OR FACEBOOK LINK", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio", "APK File"])

if st.button("Prepare Download") and target_url:
    try:
        if "MP3" in format_type.upper() or "AUDIO" in format_type.upper():
            ydl_opts = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
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
                "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
                "http_headers": {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            direct_url = info.get("url")

        if direct_url:
            # Shortening via ShrinkMe API for ad integration
            shortened_url = shorten_with_shrinkme(direct_url)
            
            st.success("YouTube Video Media Ready")
            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:inline-block;padding:14px 24px;background-color:#ff0000;color:white;text-decoration:none;border-radius:8px;font-weight:bold;text-align:center;width:100%;font-size:18px;">📥 Click Here to Download (Via Ad Link)</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The download link could not be processed. Please verify the URL and try again.")

    except Exception as e:
        st.error(f"Download failed: {e}")

# Active Downloads Status Section
st.markdown(
    """
    <div style="background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-top: 20px;">
        <h4 style="color: #ff4444; font-size: 14px; margin-bottom: 5px;">📁 Active Downloads & Gallery Status</h4>
        <p style="color: gray; font-size: 12px; margin: 0;">No downloaded media history yet!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>YT Dodo Universal Media Hub $\\textcircled{c}$ 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)
