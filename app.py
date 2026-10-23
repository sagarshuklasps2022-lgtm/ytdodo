import os
import streamlit as st
import yt_dlp
import requests

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub",
    page_icon="📥",
    layout="centered",
)

# Professional 3D Dark Theme Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .main-header {
        background: linear-gradient(145deg, #131822, #0e121b);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.6);
    }
    .card-box {
        background: linear-gradient(145deg, #131822, #0e121b);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #30363d;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.6);
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0b0f19 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 20px;
        border: none;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ef4444, #b91c1c);
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.6);
    }
    .shortcut-btn {
        background-color: #0b0f19;
        border: 1px solid #30363d;
        padding: 14px 10px;
        border-radius: 14px;
        text-align: center;
        color: white;
        text-decoration: none;
        font-size: 12px;
        font-weight: 600;
        display: block;
        margin-bottom: 10px;
        box-shadow: inset 0 2px 5px rgba(255,255,255,0.05);
        transition: all 0.2s ease;
    }
    .shortcut-btn:hover {
        border-color: #dc2626;
        color: #ef4444;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

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

# Top Header UI matching 3D professional design
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 14px; color: white; font-size: 20px; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 style="color: white; font-weight: bold; font-size: 17px; margin: 0; letter-spacing: 0.5px;">YT DODO</h3>
                <p style="color: #9ca3af; font-size: 11px; margin: 0;">Welcome, Sagar Shukla</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <span style="background-color: #1f242d; padding: 8px 12px; border-radius: 12px; font-size: 14px; cursor: pointer; border: 1px solid #30363d;">☁️</span>
            <span style="background-color: #1f242d; padding: 8px 14px; border-radius: 12px; font-size: 12px; color: #f87171; font-weight: 600; cursor: pointer; border: 1px solid #30363d;">🚪 Logout</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Quick Platforms & Shortcuts Section Header
st.markdown("""
    <div class="card-box" style="padding-bottom: 12px;">
        <p style="color: #9ca3af; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 14px; letter-spacing: 1px;">Quick Platforms & Shortcuts</p>
""", unsafe_allow_html=True)

# Shortcut Grid using Streamlit Columns
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<a href="https://www.youtube.com" target="_blank" class="shortcut-btn">🔴 YouTube</a>', unsafe_allow_html=True)
with c2:
    st.markdown('<a href="https://www.google.com" target="_blank" class="shortcut-btn">🔵 Google</a>', unsafe_allow_html=True)
with c3:
    st.markdown('<a href="https://www.facebook.com" target="_blank" class="shortcut-btn">📘 Facebook</a>', unsafe_allow_html=True)
with c4:
    st.markdown('<a href="https://www.instagram.com" target="_blank" class="shortcut-btn">📸 Instagram</a>', unsafe_allow_html=True)

c5, c6 = st.columns(2)
with c5:
    st.markdown('<a href="https://twitter.com" target="_blank" class="shortcut-btn">🐦 Twitter</a>', unsafe_allow_html=True)
with c6:
    st.markdown('<div class="shortcut-btn" style="border-style: dashed; color: #9ca3af;">➕ Add URL</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Search & Download Hub Section
st.markdown("""
    <div class="card-box">
        <h3 style="color: #dc2626; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px;">🔍 Search & Download Hub</h3>
""", unsafe_allow_html=True)

target_url = st.text_input("PASTE YOUTUBE, INSTAGRAM OR FACEBOOK LINK", placeholder="Paste link or search songs, videos, apps...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio", "APK File"])

if st.button("Search & Prepare Download", use_container_width=True) and target_url:
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
            # Shortening through ShrinkMe API for Monetization
            shortened_url = shorten_with_shrinkme(direct_url)
            
            st.success("YouTube Video Media Ready")
            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:inline-block;padding:14px 24px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4);">📥 Download in Browser (Via Ad Link)</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The download link could not be processed. Please verify the URL and try again.")

    except Exception as e:
        st.error(f"Download failed: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# Active Downloads Status Box
st.markdown("""
    <div class="card-box">
        <h4 style="color: #dc2626; font-size: 13px; font-weight: bold; margin-bottom: 8px;">📁 Active Downloads & Gallery Status</h4>
        <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.6;">
            No active downloads right now. Click the top-right download icon to view completed files and options!
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border-color: #30363d; margin-top: 30px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>YT Dodo Universal Media Hub $\\textcircled{c}$ 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)
