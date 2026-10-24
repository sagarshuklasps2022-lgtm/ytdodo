import os
import streamlit as st
import yt_dlp
import requests
import random

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Professional Media Hub",
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

# Dynamic Theme Colors based on user selection
if st.session_state.theme_mode == "Dark":
    bg_gradient = "linear-gradient(135deg, #7f1d1d 0%, #dc2626 35%, #0b0f19 55%, #0b0f19 100%)"
    card_bg = "rgba(19, 24, 34, 0.95)"
    text_color = "#ffffff"
    border_color = "rgba(220, 38, 38, 0.3)"
    sub_text = "#9ca3af"
    shortcut_bg = "#1e293b"
else:
    bg_gradient = "linear-gradient(135deg, #fecaca 0%, #fef2f2 35%, #f3f4f6 55%, #f3f4f6 100%)"
    card_bg = "rgba(255, 255, 255, 0.95)"
    text_color = "#1f2937"
    border_color = "#d1d5db"
    sub_text = "#4b5563"
    shortcut_bg = "#ffffff"

# Professional Custom CSS & UI Styling mirroring the exact HTML design
st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_gradient};
        background-attachment: fixed;
        color: {text_color};
        font-family: 'Inter', sans-serif;
    }}
    .stTextInput input {{
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }}
    .stSelectbox select {{
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.4);
        width: 100%;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #ef4444, #b91c1c);
    }}
    .main-header {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid {border_color};
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }}
    .card-box {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid {border_color};
        margin-bottom: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }}
    .shortcut-btn {{
        background: {shortcut_bg};
        border: 1px solid rgba(30, 58, 138, 0.6);
        padding: 16px 10px;
        border-radius: 12px;
        text-align: center;
        color: {text_color};
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }}
    .shortcut-btn:hover {{
        border-color: rgba(220, 38, 38, 0.6);
        transform: scale(1.03);
    }}
    .sponsored-banner {{
        background: {card_bg};
        backdrop-filter: blur(8px);
        border: 1px dashed rgba(220, 38, 38, 0.6);
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 12px;
        color: #ef4444;
        font-weight: 500;
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Preferences: Theme and Language
st.sidebar.title("⚙️ Settings")
st.session_state.theme_mode = st.sidebar.selectbox("Theme Mode", ["Dark", "Light"], index=0 if st.session_state.theme_mode=="Dark" else 1)
st.session_state.app_lang = st.sidebar.selectbox("Language", ["English", "Hindi"], index=0 if st.session_state.app_lang=="English" else 1)

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

# --- DASHBOARD HEADER WITH GOLDEN LIGHTNING ICON ---
st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #b91c1c, #450a0a); width: 60px; height: 52px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.4); border: 1px solid rgba(248, 113, 113, 0.4);">
                <span style="font-size: 24px; filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.8));">⚡</span>
            </div>
            <div>
                <h3 style="background: linear-gradient(to right, #ef4444, #ffffff, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 20px; margin: 0; letter-spacing: 0.05em;">YT DODO</h3>
                <p style="color: {sub_text}; font-size: 11px; font-weight: 600; margin: 0;">Professional Media Hub • Creator: Sagar Shukla</p>
            </div>
        </div>
        <div style="background: rgba(11, 15, 25, 0.8); border: 1px solid #374151; padding: 6px 12px; border-radius: 10px; display: flex; align-items: center; gap: 8px;">
            <span style="width: 10px; height: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block;"></span>
            <span style="font-size: 12px; font-weight: bold; color: #e5e7eb;">Live: 1,482</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sponsored Banner Ad
st.markdown("""
    <div class="sponsored-banner">
        📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! 
        <a href="https://shrinkme.io" target="_blank" style="color:#ef4444; font-weight:bold; text-decoration:underline; margin-left: 4px;">INSTALL NOW</a>
    </div>
""", unsafe_allow_html=True)

# Quick Shortcuts Section
st.markdown(f"""
    <div class="card-box" style="padding-bottom: 15px;">
        <p style="color: {sub_text}; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px; display: flex; align-items: center; gap: 6px;">
            <span>🚀</span> Quick Platforms & Shortcuts
        </p>
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

# --- Universal Video & Media Downloader Hub ---
st.markdown(f"""
    <div class="card-box">
        <h3 style="color: #ef4444; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
            <span>🔍</span> Universal Video & Media Downloader
        </h3>
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
        f'<div style="background:#0b0f19; padding:18px; border-radius:12px; border:1px solid rgba(220, 38, 38, 0.5); margin-top:20px; margin-bottom:15px; text-align:center;">'
        f'<p style="color:#d1d5db; font-size:12px; font-weight:600; margin-bottom:10px;">👇 Click below to proceed with search & review:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:12px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">Search and Review</a>'
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
            title = info.get("title", "Sample Media Title - YT Dodo Stream")

        if direct_url:
            shortened_url = shorten_with_shrinkme(direct_url)
            
            st.success("Media Ready for Download!")
            
            # Video Player Display Header
            st.markdown(f"""
                <div style="background:#1f242d; padding:12px 16px; border-radius:12px 12px 0 0; border:1px solid #374151; border-bottom:none; display:flex; align-items:center; gap:10px; margin-top: 15px;">
                    <span style="font-size:16px;">🎵</span>
                    <p style="color:#ffffff; font-size:14px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{title}</p>
                </div>
            """, unsafe_allow_html=True)
            st.video(direct_url)
            
            # Single Monetized Download Button styled in Blue color
            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:block;padding:14px 24px;background:linear-gradient(135deg, #2563eb, #1d4ed8);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:15px;box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4); margin-top: 15px; margin-bottom: 12px;">Download</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The media link could not be processed.")

    except Exception as ex:
        st.error(f"Extraction error: {ex}")

st.markdown("</div>", unsafe_allow_html=True)

# Active Downloads Status Box
st.markdown(f"""
    <div class="card-box">
        <h3 style="color: #ef4444; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px;">📁 Gallery & Active Downloads Status</h3>
        <p style="color: {sub_text}; font-size: 11px; margin: 0; line-height: 1.6;">
            No active downloads right now. Completed items will appear here securely!
        </p>
    </div>
""", unsafe_allow_html=True)

# Final Footer
st.markdown(f"<hr style='border-color: {border_color}; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sub_text}; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
