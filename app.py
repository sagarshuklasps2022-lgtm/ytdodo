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

# Custom CSS matching the exact original HTML background and layout
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body, .stApp { 
            font-family: 'Inter', sans-serif !important;
            background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 35%, #0b0f19 55%, #0b0f19 100%) !important;
            background-attachment: fixed !important;
            color: white !important;
        }
        .block-container {
            max-width: 42rem;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stTextInput input, .stSelectbox select {
            background-color: #0b0f19 !important;
            color: white !important;
            border: 1px solid #1f2937 !important;
            border-radius: 0.75rem !important;
            padding: 12px 16px !important;
        }
        .stButton>button {
            background: linear-gradient(to right, #dc2626, #991b1b) !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 0.75rem !important;
            padding: 12px 24px !important;
            border: none !important;
            box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.4) !important;
            width: 100% !important;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #ef4444, #b91c1c) !important;
        }
        footer {visibility: hidden;}
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

# --- TOP DASHBOARD HEADER ---
st.markdown("""
    <div style="width: 100%; max-width: 36rem; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem;">
        <!-- Top Dashboard Header Box -->
        <div style="background-color: rgba(19, 24, 34, 0.95); backdrop-filter: blur(12px); border: 1px solid rgba(220, 38, 38, 0.3); padding: 1.25rem; border-radius: 1rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); display: flex; align-items: center; justify-content: space-between; position: relative; overflow: hidden;">
            <div style="display: flex; align-items: center; gap: 0.875rem;">
                <div style="width: 4rem; height: 3.5rem; background: linear-gradient(to top right, #b91c1c, #991b1b, #450a0a); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.4); border: 1px solid rgba(248, 113, 113, 0.4);">
                    <span style="font-size: 1.5rem; filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.9)); color: #fbbf24; font-weight: 800;">⚡</span>
                </div>
                <div>
                    <h1 style="font-weight: 800; font-size: 1.25rem; letter-spacing: 0.05em; background: linear-gradient(to right, #ef4444, #ffffff, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">YT DODO</h1>
                    <p style="font-size: 0.75rem; font-weight: 600; color: #9ca3af; margin: 0;">Professional Media Hub • Creator: Sagar Shukla</p>
                </div>
            </div>
            <div style="background-color: rgba(11, 15, 25, 0.8); border: 1px solid #374151; padding: 0.5rem 0.875rem; border-radius: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 0.625rem; height: 0.625rem; background-color: #22c55e; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.75rem; font-weight: bold; color: #e5e7eb;">Live: 1,482</span>
            </div>
        </div>

        <!-- Sponsored Banner -->
        <div style="background-color: rgba(19, 24, 34, 0.9); border: 1px dashed rgba(220, 38, 38, 0.6); padding: 0.875rem; border-radius: 0.75rem; text-align: center; font-size: 0.75rem; color: #f87171; font-weight: 500;">
            📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! 
            <a href="https://shrinkme.io" target="_blank" style="font-weight: bold; color: #ef4444; text-decoration: underline; margin-left: 0.25rem;">INSTALL NOW</a>
        </div>

        <!-- Quick Platforms & Shortcuts Section with Exact HTML Grid and SVGs -->
        <div style="background-color: rgba(19, 24, 34, 0.95); backdrop-filter: blur(12px); border: 1px solid #1f2937; padding: 1.25rem; border-radius: 1rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
            <p style="font-size: 0.75rem; font-weight: bold; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.375rem;">
                <span>🚀</span> Quick Platforms & Shortcuts
            </p>
            <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem;">
                <!-- YouTube -->
                <a href="https://www.youtube.com" target="_blank" style="background-color: #1e293b; border: 1px solid rgba(30, 58, 138, 0.6); padding: 0.875rem 0.5rem; border-radius: 0.75rem; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <svg style="width: 1.5rem; height: 1.5rem; margin-bottom: 0.375rem; fill: #ef4444;" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    <span style="font-size: 0.75rem; font-weight: bold; color: #f3f4f6;">YouTube</span>
                </a>
                <!-- Google -->
                <a href="https://www.google.com" target="_blank" style="background-color: #1e293b; border: 1px solid rgba(30, 58, 138, 0.6); padding: 0.875rem 0.5rem; border-radius: 0.75rem; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <svg style="width: 1.5rem; height: 1.5rem; margin-bottom: 0.375rem;" viewBox="0 0 24 24"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.19v3.15C3.21 21.32 7.23 24 12 24z"/><path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.19C.43 8.14 0 9.87 0 12s.43 3.86 1.19 5.39l4.08-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.21 2.68 1.19 6.61l4.08 3.15c.95-2.85 3.6-4.96 6.73-4.96z"/></svg>
                    <span style="font-size: 0.75rem; font-weight: bold; color: #f3f4f6;">Google</span>
                </a>
                <!-- Facebook -->
                <a href="https://www.facebook.com" target="_blank" style="background-color: #1e293b; border: 1px solid rgba(30, 58, 138, 0.6); padding: 0.875rem 0.5rem; border-radius: 0.75rem; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <svg style="width: 1.5rem; height: 1.5rem; margin-bottom: 0.375rem; fill: #1877F2;" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    <span style="font-size: 0.75rem; font-weight: bold; color: #f3f4f6;">Facebook</span>
                </a>
                <!-- Instagram -->
                <a href="https://www.instagram.com" target="_blank" style="background-color: #1e293b; border: 1px solid rgba(30, 58, 138, 0.6); padding: 0.875rem 0.5rem; border-radius: 0.75rem; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; text-decoration: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <svg style="width: 1.5rem; height: 1.5rem; margin-bottom: 0.375rem; fill: #E4405F;" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    <span style="font-size: 0.75rem; font-weight: bold; color: #f3f4f6;">Instagram</span>
                </a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DOWNLOADER SECTION ---
st.markdown("""
    <div style="width: 100%; max-width: 36rem; margin: 0 auto; margin-top: 1.5rem;">
        <div style="background-color: rgba(19, 24, 34, 0.95); backdrop-filter: blur(12px); border: 1px solid #1f2937; padding: 1.25rem; border-radius: 1rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
            <h2 style="font-size: 0.875rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 0.5rem; color: #ef4444; margin-bottom: 1rem;">
                <span>🔍</span> Universal Video & Media Downloader
            </h2>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

if st.button("Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)
    
    st.markdown(f"""
        <div style="margin-top: 0.75rem; margin-bottom: 0.75rem;">
            <div style="background-color: #0b0f19; border: 1px solid rgba(220, 38, 38, 0.5); padding: 1rem; border-radius: 0.75rem; text-align: center; display: flex; flex-direction: column; gap: 0.5rem;">
                <p style="font-size: 0.75rem; font-weight: 600; color: #d1d5db; margin: 0;">👇 Click below to proceed with search & review:</p>
                <a href="{shortened_ad_url}" target="_blank" style="color: white; text-decoration: none; display: block; background: linear-gradient(to right, #dc2626, #991b1b); padding: 0.75rem; border-radius: 0.5rem; font-weight: bold; font-size: 0.875rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);">
                    Search and Review
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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
            title = info.get("title", "Sample Media Title - YT Dodo Stream")

        if direct_url:
            shortened_url = shorten_with_shrinkme(direct_url)
            
            st.success("Media Ready for Download!")
            
            st.markdown(f"""
                <div style="margin-top: 1rem; border-top: 1px solid #1f2937; padding-top: 1rem;">
                    <div style="background-color: #1f242d; border: 1px solid #374151; border-top-left-radius: 0.75rem; border-top-right-radius: 0.75rem; padding: 0.75rem 1rem; display: flex; align-items: center; gap: 0.625rem;">
                        <span style="font-size: 1rem;">🎵</span>
                        <p style="font-size: 0.875rem; font-weight: bold; color: white; margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{title}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.video(direct_url)
            
            st.markdown(f"""
                <a href="{shortened_url}" target="_blank" style="display: block; width: 100%; background: linear-gradient(to right, #2563eb, #1d4ed8); color: white; font-weight: bold; padding: 0.875rem 1rem; border-radius: 0.75rem; text-align: center; text-decoration: none; margin-top: 1rem; margin-bottom: 0.75rem; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4);">
                    Download
                </a>
            """, unsafe_allow_html=True)
        else:
            st.error("The media link could not be processed.")

    except Exception as ex:
        st.error(f"Extraction error: {ex}")

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STATUS & FOOTER ---
st.markdown("""
    <div style="width: 100%; max-width: 36rem; margin: 0 auto; margin-top: 1.5rem; margin-bottom: 2rem;">
        <div style="background-color: rgba(19, 24, 34, 0.95); backdrop-filter: blur(12px); border: 1px solid #1f2937; padding: 1.25rem; border-radius: 1rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);">
            <h3 style="font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; color: #ef4444; margin-bottom: 0.5rem;">📁 Gallery & Active Downloads Status</h3>
            <p style="font-size: 0.75rem; color: #9ca3af; line-height: 1.6; margin: 0;">
                No active downloads right now. Completed items will appear here securely!
            </p>
        </div>
        
        <footer style="border-top: 1px solid rgba(31, 41, 55, 0.6); text-align: center; color: #9ca3af; font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem;">
            YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla
        </footer>
    </div>
""", unsafe_allow_html=True)
