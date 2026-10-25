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
if "download_history" not in st.session_state:
    st.session_state.download_history = []

# Exact UI Styling matching your reference image with Golden text, Red Glow and Framed Cards
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, #991b1b 0%, #7f1d1d 20%, #1f0505 50%, #0b0f19 85%);
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
        padding: 14px 20px;
        border: none;
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
        width: 100%;
    }
    .main-header {
        background: #131822;
        padding: 18px 22px;
        border-radius: 20px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .card-box {
        background: #131822;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .sponsored-banner {
        background: #131822;
        border: 1px dashed #dc2626;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 12px;
        color: #ef4444;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    .shortcut-card {
        background: #0b0f19;
        border: 1px solid #30363d;
        padding: 16px 10px;
        border-radius: 14px;
        text-align: center;
        color: #ffffff;
        text-decoration: none;
        display: block;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: 0.2s;
    }
    .shortcut-card:hover {
        border-color: #dc2626;
    }
    .yt-title {
        font-weight: 900;
        font-size: 18px;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #ffffff 40%, #f87171 80%, #ef4444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .golden-sub {
        color: #fbbf24;
        font-size: 12px;
        font-weight: 600;
        margin: 2px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Settings
st.sidebar.title("⚙️ Settings")
st.session_state.theme_mode = st.sidebar.selectbox("Theme Mode", ["Dark", "Light"], index=0)
st.session_state.app_lang = st.sidebar.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu", "Marathi"], index=0)

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

# --- TOP HEADER ---
st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 14px; color: white; font-size: 22px; width: 46px; height: 46px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 class="yt-title">YT DODO</h3>
                <p class="golden-sub">Professional Media Hub • Creator: Sagar Shukla</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #0b0f19; padding: 10px 16px; border-radius: 14px; border: 1px solid #30363d; position: relative; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 18px;">☁️</span>
                <span style="position: absolute; top: -6px; right: -6px; background: #ea580c; color: white; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 50%;">{len(st.session_state.download_history)}</span>
            </div>
            <div style="background: #0b0f19; padding: 6px 14px; border-radius: 14px; border: 1px solid #30363d; text-align: center;">
                <p style="color: #9ca3af; font-size: 9px; margin: 0; font-weight: bold; text-transform: uppercase;">Live</p>
                <div style="display: flex; align-items: center; gap: 4px;">
                    <span style="color: #4ade80; font-size: 10px;">●</span>
                    <span style="color: #ffffff; font-size: 12px; font-weight: bold;">👤 1,484</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sponsored Banner Ad
st.markdown("""
    <div class="sponsored-banner">
        📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! <a href="https://shrinkme.io" target="_blank" style="color:#ef4444; font-weight:bold; text-decoration:none;">INSTALL NOW</a>
    </div>
""", unsafe_allow_html=True)

# --- FIRST FRAME: QUICK PLATFORMS & SHORTCUTS ---
st.markdown("""
    <div class="card-box">
        <p style="color: #ef4444; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px;">🚀 QUICK PLATFORMS & SHORTCUTS</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('''
        <a href="https://www.youtube.com" target="_blank" class="shortcut-card">
            <svg height="24" viewBox="0 0 24 24" width="24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" fill="#ff0000"/></svg>
            <div style="font-size:11px; font-weight:bold; color:#ffffff; margin-top:6px;">YouTube</div>
        </a>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('''
        <a href="https://www.google.com" target="_blank" class="shortcut-card">
            <svg height="24" viewBox="0 0 24 24" width="24"><path d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.8 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.1 8.9 5 12 5z" fill="#ea4335"/><path d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z" fill="#4285f4"/><path d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.7s.2-2 .4-2.7L1.6 6.4C.6 8.4 0 10.6 0 13s.6 4.6 1.6 6.6l3.7-2.9c-.3-.7-.5-1.4-.5-2z" fill="#fbbc05"/><path d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.1-6.7-5.3L1.6 15.9C3.5 19.7 7.4 23 12 23z" fill="#34a853"/></svg>
            <div style="font-size:11px; font-weight:bold; color:#ffffff; margin-top:6px;">Google</div>
        </a>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown('''
        <a href="https://www.facebook.com" target="_blank" class="shortcut-card">
            <svg height="24" viewBox="0 0 24 24" width="24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" fill="#1877f2"/></svg>
            <div style="font-size:11px; font-weight:bold; color:#ffffff; margin-top:6px;">Facebook</div>
        </a>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown('''
        <a href="https://www.instagram.com" target="_blank" class="shortcut-card">
            <svg height="24" viewBox="0 0 24 24" width="24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" fill="#e1306c"/></svg>
            <div style="font-size:11px; font-weight:bold; color:#ffffff; margin-top:6px;">Instagram</div>
        </a>
    ''', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- SECOND FRAME: UNIVERSAL VIDEO & MEDIA DOWNLOADER ---
st.markdown("""
    <div class="card-box">
        <p style="color: #ef4444; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 14px; letter-spacing: 0.5px;">🔍 UNIVERSAL VIDEO & MEDIA DOWNLOADER</p>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...", label_visibility="visible")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

if st.button("Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

st.markdown("</div>", unsafe_allow_html=True)

# --- SECURE VERIFICATION & AD FLOW SECTION ---
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)

    st.markdown(
        f'<div class="card-box" style="border: 1px solid #dc2626; text-align:center;">'
        f'<p style="color:#ffffff; font-size:13px; font-weight:bold; margin-bottom:12px;">👇 Click below to complete verification on ShrinkMe:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;font-size:14px;">Verify & Proceed to Ad Page</a>'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("✅ Click here after verification to load media player", use_container_width=True):
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
            final_download_link = shorten_with_shrinkme(direct_url)

            history_item = {"title": title, "url": active_url, "format": active_format}
            if history_item not in st.session_state.download_history:
                st.session_state.download_history.insert(0, history_item)

            st.success("Verification Successful! Media Player Ready.")

            st.markdown(f"""
                <div style="background:#131822; padding:12px 18px; border-radius:12px 12px 0 0; border:1px solid #30363d; border-bottom:none; display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">🎵</span>
                    <p style="color:#ffffff; font-size:14px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{title}</p>
                </div>
            """, unsafe_allow_html=True)
            st.video(direct_url)

            st.markdown(
                f'<a href="{final_download_link}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:15px;box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); margin-top: 15px; margin-bottom: 12px;">Download Video File</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The media link could not be processed.")

    except Exception as ex:
        st.error(f"Extraction error: {ex}")

# --- THIRD FRAME: GALLERY & ACTIVE DOWNLOADS STATUS ---
st.markdown("""
    <div class="card-box">
        <p style="color: #ef4444; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.5px;">📁 GALLERY & ACTIVE DOWNLOADS STATUS</p>
""", unsafe_allow_html=True)

if len(st.session_state.download_history) > 0:
    for idx, item in enumerate(st.session_state.download_history):
        st.markdown(f"""
            <div style="background: #0b0f19; padding: 12px 16px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #ffffff; font-size: 12px; font-weight: bold; margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 260px;">🎵 {item['title']}</p>
                    <p style="color: #4ade80; font-size: 10px; margin: 2px 0 0 0;">Format: {item['format']}</p>
                </div>
                <span style="background: #1e293b; color: #94a3b8; font-size: 10px; padding: 4px 8px; border-radius: 6px;">Saved</span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="background: #0b0f19; padding: 18px; border-radius: 12px; border: 1px solid #30363d; text-align: center;">
            <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.5;">
                No active downloads right now. Completed items will appear here securely!
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Final Footer
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 30px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
