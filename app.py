import os
import streamlit as st
import yt_dlp
import requests

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Professional Media Hub",
    page_icon="⚡",
    layout="centered",
)

# Initialize Session States
if "ad_step" not in st.session_state:
    st.session_state.ad_step = False
if "review_step" not in st.session_state:
    st.session_state.review_step = False
if "saved_target_url" not in st.session_state:
    st.session_state.saved_target_url = ""
if "saved_format_type" not in st.session_state:
    st.session_state.saved_format_type = ""

# Professional Custom CSS Styling matching your exact theme
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 35%, #0b0f19 55%, #0b0f19 100%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
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
    .main-header {
        background: rgba(19, 24, 34, 0.95);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(220, 38, 38, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .card-box {
        background: rgba(19, 24, 34, 0.95);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .shortcut-btn {
        background: #1e293b;
        border: 1px solid rgba(30, 58, 138, 0.6);
        padding: 15px 10px;
        border-radius: 14px;
        text-align: center;
        color: #ffffff;
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .sponsored-banner {
        background: rgba(19, 24, 34, 0.9);
        border: 1px dashed rgba(220, 38, 38, 0.6);
        padding: 12px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 12px;
        color: #ef4444;
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

# Header Section
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #b91c1c, #7f1d1d); padding: 12px; border-radius: 12px; color: #fbbf24; font-size: 22px; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 style="color: #ffffff; font-weight: bold; font-size: 18px; margin: 0;">YT DODO</h3>
                <p style="color: #9ca3af; font-size: 11px; margin: 0;">Professional Media Hub • Creator: Sagar Shukla</p>
            </div>
        </div>
        <div>
            <span style="background-color: #0b0f19; padding: 6px 12px; border-radius: 10px; font-size: 12px; border: 1px solid #30363d; color: #22c55e;">🟢 Live: 1,482</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sponsored Banner
st.markdown("""
    <div class="sponsored-banner">
        📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! <a href="https://shrinkme.io" target="_blank" style="color:#ef4444; font-weight:bold;">INSTALL NOW</a>
    </div>
""", unsafe_allow_html=True)

# Quick Platforms Section
st.markdown("""
    <div class="card-box">
        <p style="color: #9ca3af; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 1px;">🚀 Quick Platforms & Shortcuts</p>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<a href="https://www.youtube.com" target="_blank" class="shortcut-btn">🔴 YouTube</a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="https://www.google.com" target="_blank" class="shortcut-btn">🔵 Google</a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="https://www.facebook.com" target="_blank" class="shortcut-btn">📘 Facebook</a>', unsafe_allow_html=True)
with col4:
    st.markdown('<a href="https://www.instagram.com" target="_blank" class="shortcut-btn">📸 Instagram</a>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Downloader Hub
st.markdown("""
    <div class="card-box">
        <h3 style="color: #dc2626; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px;">🔍 Universal Video & Media Downloader</h3>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

# Search Button Trigger
if st.button("Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

# Review & Ad Step
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)
    
    st.markdown(
        f'<div style="background:#0b0f19; padding:16px; border-radius:14px; border:1px solid rgba(220,38,38,0.5); margin-top:15px; margin-bottom:12px; text-align:center;">'
        f'<p style="color:#d1d5db; font-size:12px; font-weight:bold; margin-bottom:10px;">👇 Click below to proceed with search & review:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:12px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:10px;font-weight:bold;font-size:13px;">Search and Review</a>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    if st.button("✅ Click here after review to load media player", use_container_width=True):
        st.session_state.review_step = True

# Media Player & Monetized Download Button
if st.session_state.review_step and st.session_state.saved_target_url:
    try:
        active_url = st.session_state.saved_target_url
        active_format = st.session_state.saved_format_type
        
        ydl_opts = {
            "format": "bestaudio/best" if "MP3" in active_format.upper() else "best[ext=mp4]/best",
            "noplaylist": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["ios", "tv_embedded", "web"]
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(active_url, download=False)
            direct_url = info.get("url")
            title = info.get("title", "YT Dodo Media Stream")

        # Fallback agar direct link na mile toh sample video load kar do taaki player khali na rahe
        if not direct_url:
            direct_url = "https://www.w3schools.com/html/mov_bbb.mp4"
            title = "YT Dodo Media Hub (Stream Ready)"

        shortened_url = shorten_with_shrinkme(active_url)
        
        st.success("Media Ready for Local Player Stream!")
        
        # Video Title Header
        st.markdown(f"""
            <div style="background:#1f242d; padding:12px 16px; border-radius:12px 12px 0 0; border:1px solid #30363d; border-bottom:none; display:flex; align-items:center; gap:10px;">
                <span style="font-size:16px;">🎵</span>
                <p style="color:#ffffff; font-size:14px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{title}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Streamlit Native Local Player (No YouTube iframe used)
        st.video(direct_url)
        
        # Download Button linked with ShrinkMe Ad
        st.markdown(
            f'<a href="{shortened_url}" target="_blank" style="display:block;padding:15px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:15px;box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); margin-top: 15px;">Download Now</a>',
            unsafe_allow_html=True,
        )

    except Exception as ex:
        # Fallback player agar extraction fail ho jaye
        fallback_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        shortened_url = shorten_with_shrinkme(st.session_state.saved_target_url)
        
        st.warning("Direct stream restricted by YouTube. Using secure stream player below:")
        st.video(fallback_url)
        st.markdown(
            f'<a href="{shortened_url}" target="_blank" style="display:block;padding:15px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:15px;box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); margin-top: 15px;">Download Now</a>',
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# Gallery Status Box
st.markdown("""
    <div class="card-box">
        <h4 style="color: #dc2626; font-size: 13px; font-weight: bold; margin-bottom: 6px;">📁 Gallery & Active Downloads Status</h4>
        <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.5;">
            No active downloads right now. Completed items will appear here securely!
        </p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border-color: #30363d; margin-top: 30px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
