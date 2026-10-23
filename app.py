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

# Custom CSS for Streamlit background alignment matching the 3D dark theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background-color: #dc2626;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b91c1c;
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

# --- EXACT REFERENCE 3D PROFESSIONAL DASHBOARD UI ---
dashboard_html = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-[#0b0f19] text-white font-sans">
    <div class="max-w-md mx-auto p-3">
        <!-- Top Header & Profile Bar -->
        <div class="flex justify-between items-center bg-[#131822] p-3 rounded-2xl border border-gray-800/80 mb-5 shadow-2xl">
            <div class="flex items-center space-x-2.5">
                <div class="bg-gradient-to-br from-red-600 to-red-700 p-2 rounded-xl text-white shadow-lg shadow-red-600/30">
                    <i class="fa-solid fa-bolt text-base"></i>
                </div>
                <div>
                    <h1 class="font-bold text-sm tracking-wider text-white m-0">YT DODO</h1>
                    <p class="text-[11px] text-gray-400 m-0">Welcome, Sagar Shukla</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <button class="bg-[#1f242d] p-2 rounded-xl hover:bg-gray-700 text-gray-300 text-xs shadow-md"><i class="fa-solid fa-cloud text-red-500"></i></button>
                <button class="bg-[#1f242d] px-3 py-1.5 rounded-xl hover:bg-red-600/20 hover:text-red-500 text-gray-300 text-xs font-semibold transition flex items-center space-x-1 shadow-md">
                    <i class="fa-solid fa-power-off text-[10px]"></i> <span>Logout</span>
                </button>
            </div>
        </div>

        <!-- Search & Download Hub Box -->
        <div class="bg-[#131822] p-4 rounded-2xl border border-gray-800/80 mb-5 shadow-2xl">
            <h2 class="text-xs font-bold uppercase tracking-widest text-red-500 mb-3 flex items-center space-x-2">
                <i class="fa-solid fa-magnifying-glass"></i> <span>Search & Download Hub</span>
            </h2>
        </div>

        <!-- Quick Platforms & Shortcuts Section -->
        <div class="bg-[#131822] p-4 rounded-2xl border border-gray-800/80 mb-5 shadow-2xl">
            <h2 class="text-[11px] font-bold uppercase tracking-wider text-gray-400 mb-3">Quick Platforms & Shortcuts:</h2>
            <div class="grid grid-cols-4 gap-2.5">
                <a href="https://www.youtube.com" target="_blank" class="bg-[#0b0f19] border border-gray-800/60 p-3 rounded-xl text-center hover:border-red-600 transition block text-white no-underline shadow-inner">
                    <i class="fa-brands fa-youtube text-red-500 text-base mb-1 block"></i>
                    <span class="text-[10px] font-medium text-gray-300">YouTube</span>
                </a>
                <a href="https://www.google.com" target="_blank" class="bg-[#0b0f19] border border-gray-800/60 p-3 rounded-xl text-center hover:border-red-600 transition block text-white no-underline shadow-inner">
                    <i class="fa-brands fa-google text-blue-500 text-base mb-1 block"></i>
                    <span class="text-[10px] font-medium text-gray-300">Google</span>
                </a>
                <a href="https://www.facebook.com" target="_blank" class="bg-[#0b0f19] border border-gray-800/60 p-3 rounded-xl text-center hover:border-red-600 transition block text-white no-underline shadow-inner">
                    <i class="fa-brands fa-facebook text-blue-600 text-base mb-1 block"></i>
                    <span class="text-[10px] font-medium text-gray-300">Facebook</span>
                </a>
                <a href="https://www.instagram.com" target="_blank" class="bg-[#0b0f19] border border-gray-800/60 p-3 rounded-xl text-center hover:border-red-600 transition block text-white no-underline shadow-inner">
                    <i class="fa-brands fa-instagram text-pink-500 text-base mb-1 block"></i>
                    <span class="text-[10px] font-medium text-gray-300">Instagram</span>
                </a>
            </div>
            <div class="grid grid-cols-2 gap-2.5 mt-2.5">
                <a href="https://twitter.com" target="_blank" class="bg-[#0b0f19] border border-gray-800/60 p-2.5 rounded-xl text-center hover:border-red-600 transition block text-white no-underline shadow-inner">
                    <i class="fa-brands fa-twitter text-sky-400 text-sm mr-1"></i> <span class="text-[10px] font-medium text-gray-300">Twitter</span>
                </a>
                <div class="bg-[#0b0f19] border border-dashed border-gray-700 p-2.5 rounded-xl text-center hover:border-red-600 transition cursor-pointer text-white shadow-inner">
                    <i class="fa-solid fa-plus text-red-500 text-sm mr-1"></i> <span class="text-[10px] font-medium text-gray-300">Add URL</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
    unsafe_allow_html=True,
)
st.markdown(dashboard_html, unsafe_allow_html=True)

# --- STREAMLIT SEARCH & DOWNLOAD FUNCTIONALITY ---
target_url = st.text_input("Paste link or search songs, videos, apps...", placeholder="https://www.youtube.com/watch?v=...")
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
            # Monetization via ShrinkMe API
            shortened_url = shorten_with_shrinkme(direct_url)
            
            st.success("YouTube Video Media Ready")
            st.markdown(
                f'<a href="{shortened_url}" target="_blank" style="display:inline-block;padding:14px 24px;background-color:#dc2626;color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.4);">📥 Download in Browser (Via Ad Link)</a>',
                unsafe_allow_html=True,
            )
        else:
            st.error("The download link could not be processed. Please verify the URL and try again.")

    except Exception as e:
        st.error(f"Download failed: {e}")

# Active Downloads Status Box matching reference
status_html = """
<div style="background-color: #131822; padding: 16px; border-radius: 16px; border: 1px solid #30363d; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <h4 style="color: #dc2626; font-size: 13px; font-weight: bold; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
        <i class="fa-solid fa-folder-open"></i> Active Downloads & Gallery Status
    </h4>
    <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.5;">
        No active downloads right now. Click the top-right download icon to view completed files and options!
    </p>
</div>
"""
st.markdown(status_html, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem; border-color: #30363d;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>YT Dodo Universal Media Hub $\\textcircled{c}$ 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)
