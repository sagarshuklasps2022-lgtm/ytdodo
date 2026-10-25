import os
import streamlit as st
import yt_dlp
import requests
import random

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Next-Gen Media Downloader",
    page_icon="⚡",
    layout="centered",
)

# Initialize Session States for Theme, Language and Ad Flow
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"
if "app_lang" not in st.session_state:
    st.session_state.app_lang = "English"
if "ad_step" not in st.session_state:
    st.session_state.ad_step = False
if "review_step" not in st.session_state:
    st.session_state.review_step = False
if "saved_target_url" not in st.session_state:
    st.session_state.saved_target_url = ""
if "saved_format_type" not in st.session_state:
    st.session_state.saved_format_type = ""

# Professional Custom CSS & UI Styling matching your exact Professional Hub design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #1a0505 0%, #0b0f19 50%, #0b0f19 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextInput input {
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    .stSelectbox select {
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        font-weight: bold;
        border-radius: 14px;
        padding: 14px 24px;
        border: none;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
        width: 100%;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.6);
    }
    .main-header {
        background: #131822;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .card-box {
        background: #131822;
        padding: 22px;
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .shortcut-btn {
        background: #1a2230;
        border: 1px solid #30363d;
        padding: 16px 8px;
        border-radius: 16px;
        text-align: center;
        color: #ffffff;
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 10px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        transition: 0.2s;
    }
    .shortcut-btn:hover {
        border-color: #dc2626;
        color: #ef4444;
    }
    .sponsored-banner {
        background: #131822;
        border: 1px dashed #dc2626;
        padding: 14px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 12px;
        color: #ef4444;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Preferences: Theme and Language
st.sidebar.title("⚙️ Settings")
st.session_state.theme_mode = st.sidebar.selectbox("Theme Mode", ["Dark", "Light"], index=0)
st.session_state.app_lang = st.sidebar.selectbox("Language", ["English", "Hindi"], index=0)

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

# --- TOP PROFESSIONAL HEADER WITH LIVE COUNTER ---
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 14px; color: white; font-size: 22px; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 style="color: #ffffff; font-weight: bold; font-size: 17px; margin: 0;">YT DODO</h3>
                <p style="color: #9ca3af; font-size: 11px; margin: 0;">Professional Media Hub • Creator: Sagar Shukla</p>
            </div>
        </div>
        <div style="background: #1a2230; padding: 8px 14px; border-radius: 14px; border: 1px solid #30363d; text-align: center;">
            <p style="color: #9ca3af; font-size: 10px; margin: 0; font-weight: bold;">Live:</p>
            <p style="color: #4ade80; font-size: 13px; margin: 0; font-weight: bold;">🟢 1,484</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sponsored Banner Ad
st.markdown("""
    <div class="sponsored-banner">
        📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! <a href="https://shrinkme.io" target="_blank" style="color:#ef4444; font-weight:bold; text-decoration:none;">INSTALL NOW</a>
    </div>
""", unsafe_allow_html=True)

# Quick Platforms & Shortcuts Section
st.markdown("""
    <div class="card-box" style="padding-bottom: 10px;">
        <p style="color: #9ca3af; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;">🚀 Quick Platforms & Shortcuts</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<a href="https://www.youtube.com" target="_blank" class="shortcut-btn">🔴 YouTube</a>', unsafe_allow_html=True)
with c2:
    st.markdown('<a href="https://www.google.com" target="_blank" class="shortcut-btn">🔵 Google</a>', unsafe_allow_html=True)
with c3:
    st.markdown('<a href="https://www.facebook.com" target="_blank" class="shortcut-btn">📘 Facebook</a>', unsafe_allow_html=True)
with c4:
    st.markdown('<a href="https://www.instagram.com" target="_blank" class="shortcut-btn">📸 Instagram</a>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- SEARCH & AD FLOW HUB ---
st.markdown("""
    <div class="card-box" style="margin-top: 20px;">
        <h3 style="color: #ef4444; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px;">🔍 Universal Video & Media Downloader</h3>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

# Step 1: Clean Search button
if st.button("Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

# Step 2: Show Search and Review button linked with ShrinkMe ad
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)

    st.markdown(
        f'<div style="background:#1a2230; padding:18px; border-radius:16px; border:1px solid #dc2626; margin-top:20px; margin-bottom:15px; text-align:center;">'
        f'<p style="color:#ffffff; font-size:13px; font-weight:bold; margin-bottom:10px;">👇 Click below to proceed with search & review:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;font-size:14px;">Search and Review</a>'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("✅ Click here after review to load media player", use_container_width=True):
        st.session_state.review_step = True

# Step 3: Media player and Blue Download button display
if st.session_state.review_step and st.session_state.saved_target_url:
    try:
        active_url = st.session_state.saved_target_url
        active_format = st.session_state.saved_format_type

        if "MP3" in active_format.upper():
            ydl_opts = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
            }
        else:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(active_url, download=False)
            direct_url = info.get("url")
            title = info.get("title", "Media_Video")

        if direct_url:
            shortened_url = shorten_with_shrinkme(direct_url)

            st.success("Media Ready for Download!")

            # Video Player Display with Exact Video Title Header on Top
            st.markdown("""
                <div style="background:#1f242d; padding:12px 18px; border-radius:12px 12px 0 0; border:1px solid #30363d; border-bottom:none; display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">🎵</span>
                    <p style="color:#ffffff; font-size:15px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{}</p>
                </div>
            """.format(title), unsafe_allow_html=True)
            st.video(direct_url)

            # Single Monetized Download Button styled in Blue color
            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:14px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); margin-top: 15px; margin-bottom: 12px;">Download</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The media link could not be processed.")

    except Exception as ex:
        st.error(f"Extraction error: {ex}")

st.markdown("</div>", unsafe_allow_html=True)

# Active Downloads Status Box
st.markdown("""
    <div class="card-box">
        <h4 style="color: #ef4444; font-size: 13px; font-weight: bold; margin-bottom: 8px; text-transform: uppercase;">📁 Gallery & Active Downloads Status</h4>
        <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.6;">
            No active downloads right now. Completed items will appear here securely!
        </p>
    </div>
""", unsafe_allow_html=True)

# Final Footer
st.markdown("<hr style='border-color: #30363d; margin-top: 30px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
