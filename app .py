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

# Initialize Session States
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

# Exact UI Styling matching your reference dashboard layout
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextInput input {
        background-color: #131822 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    .stSelectbox select {
        background-color: #131822 !important;
        color: #ffffff !important;
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
        box-shadow: 0 6px 15px rgba(220, 38, 38, 0.4);
        width: 100%;
    }
    .main-header {
        background: #131822;
        padding: 16px 20px;
        border-radius: 16px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .card-box {
        background: #131822;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #30363d;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .shortcut-btn {
        background: #0b0f19;
        border: 1px solid #30363d;
        padding: 20px 10px;
        border-radius: 14px;
        text-align: center;
        color: #ffffff;
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: 0.2s;
    }
    .shortcut-btn:hover {
        border-color: #dc2626;
        color: #ef4444;
    }
    .add-url-btn {
        background: #0b0f19;
        border: 1px dashed #dc2626;
        padding: 20px 10px;
        border-radius: 14px;
        text-align: center;
        color: #ef4444;
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- EXACT REFERENCE HEADER (No Logout, with Cloud Icon & Live User Counter) ---
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 10px; border-radius: 12px; color: white; font-size: 20px; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 style="color: #ffffff; font-weight: bold; font-size: 16px; margin: 0;">YT DOODO</h3>
                <p style="color: #9ca3af; font-size: 11px; margin: 0;">Welcome, <b>Sagar Shukla</b></p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #0b0f19; padding: 8px 12px; border-radius: 12px; border: 1px solid #30363d; position: relative; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 16px;">☁️</span>
                <span style="position: absolute; top: -5px; right: -5px; background: #dc2626; color: white; font-size: 9px; font-weight: bold; padding: 2px 5px; border-radius: 50%;">0</span>
            </div>
            <div style="background: #0b0f19; padding: 6px 12px; border-radius: 12px; border: 1px solid #30363d; display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 14px;">👤</span>
                <span style="color: #4ade80; font-size: 12px; font-weight: bold;">1,484</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SEARCH HUB SECTION ---
st.markdown("""
    <div class="card-box">
        <p style="color: #ef4444; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.5px;">SEARCH</p>
""", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="Paste link or search songs, videos, apps...", label_visibility="collapsed")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

# Search button layout matching reference
if st.button("🔍 Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

st.markdown("</div>", unsafe_allow_html=True)

# --- QUICK PLATFORMS & SHORTCUTS SECTION ---
st.markdown("""
    <div class="card-box">
        <p style="color: #9ca3af; font-size: 12px; font-weight: bold; margin-bottom: 15px;">Quick Platforms & Shortcuts:</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<a href="https://www.youtube.com" target="_blank" class="shortcut-btn">🔴<br><span style="font-size:11px;">YouTube</span></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="https://www.google.com" target="_blank" class="shortcut-btn">🔵<br><span style="font-size:11px;">Google</span></a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="https://www.facebook.com" target="_blank" class="shortcut-btn">📘<br><span style="font-size:11px;">Facebook</span></a>', unsafe_allow_html=True)
with col4:
    st.markdown('<a href="https://www.instagram.com" target="_blank" class="shortcut-btn">📸<br><span style="font-size:11px;">Instagram</span></a>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    st.markdown('<a href="https://twitter.com" target="_blank" class="shortcut-btn">🐦<br><span style="font-size:11px;">Twitter</span></a>', unsafe_allow_html=True)
with col6:
    st.markdown('<a href="#" class="add-url-btn">➕<br><span style="font-size:11px;">Add URL</span></a>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- AD FLOW & MEDIA PLAYER SECTION ---
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)

    st.markdown(
        f'<div class="card-box" style="border: 1px solid #dc2626; text-align:center;">'
        f'<p style="color:#ffffff; font-size:13px; font-weight:bold; margin-bottom:12px;">👇 Click below to proceed with search & review:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;font-size:14px;">Search and Review</a>'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("✅ Click here after review to load media player", use_container_width=True):
        st.session_state.review_step = True

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

            st.markdown(f"""
                <div style="background:#131822; padding:12px 18px; border-radius:12px 12px 0 0; border:1px solid #30363d; border-bottom:none; display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">🎵</span>
                    <p style="color:#ffffff; font-size:14px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{title}</p>
                </div>
            """, unsafe_allow_html=True)
            st.video(direct_url)

            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:15px;box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); margin-top: 15px; margin-bottom: 12px;">Download</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The media link could not be processed.")

    except Exception as ex:
        st.error(f"Extraction error: {ex}")

# --- ACTIVE DOWNLOADS & GALLERY STATUS ---
st.markdown("""
    <div class="card-box">
        <p style="color: #ef4444; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.5px;">📁 Active Downloads & Gallery Status</p>
        <div style="background: #0b0f19; padding: 18px; border-radius: 12px; border: 1px solid #30363d; text-align: center;">
            <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.5;">
                No active downloads right now. Click the top-right download icon to view completed files and options!
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Final Footer
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 30px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
