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

# --- ORIGINAL DASHBOARD UI WITH SHORTCUTS & ICONS ---
dashboard_html = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Dodo - Universal Media Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-[#0e1117] text-white font-sans">
    <div class="max-w-4xl mx-auto p-4">
        <!-- Top Header & Profile Bar -->
        <div class="flex justify-between items-center bg-[#161b22] p-4 rounded-xl border border-gray-800 mb-6 shadow-lg">
            <div class="flex items-center space-x-3">
                <div class="bg-red-600 p-2 rounded-lg text-white">
                    <i class="fa-solid fa-bolt text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-wider">YT DODO</h1>
                    <p class="text-xs text-gray-400">Welcome, Sagar Shukla</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button class="bg-[#21262d] p-2 rounded-lg hover:bg-gray-700 text-gray-300"><i class="fa-solid fa-user"></i></button>
                <button class="bg-[#21262d] p-2 rounded-lg hover:bg-gray-700 text-gray-300"><i class="fa-solid fa-gear"></i></button>
            </div>
        </div>

        <!-- Quick Platforms & Shortcuts Section -->
        <div class="bg-[#161b22] p-5 rounded-xl border border-gray-800 mb-6 shadow-xl">
            <h2 class="text-xs font-bold uppercase tracking-widest text-gray-400 mb-3">Quick Platforms & Shortcuts</h2>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                <a href="https://www.youtube.com" target="_blank" class="bg-[#0d1117] border border-gray-700 p-3 rounded-lg text-center hover:border-red-600 transition text-xs font-semibold block text-white no-underline">
                    <i class="fa-brands fa-youtube text-red-500 text-lg mb-1 block"></i> YouTube
                </a>
                <a href="https://www.google.com" target="_blank" class="bg-[#0d1117] border border-gray-700 p-3 rounded-lg text-center hover:border-red-600 transition text-xs font-semibold block text-white no-underline">
                    <i class="fa-brands fa-google text-blue-500 text-lg mb-1 block"></i> Google
                </a>
                <a href="https://www.facebook.com" target="_blank" class="bg-[#0d1117] border border-gray-700 p-3 rounded-lg text-center hover:border-red-600 transition text-xs font-semibold block text-white no-underline">
                    <i class="fa-brands fa-facebook text-blue-600 text-lg mb-1 block"></i> Facebook
                </a>
                <a href="https://www.instagram.com" target="_blank" class="bg-[#0d1117] border border-gray-700 p-3 rounded-lg text-center hover:border-red-600 transition text-xs font-semibold block text-white no-underline">
                    <i class="fa-brands fa-instagram text-pink-500 text-lg mb-1 block"></i> Instagram
                </a>
                <a href="https://twitter.com" target="_blank" class="bg-[#0d1117] border border-gray-700 p-3 rounded-lg text-center hover:border-red-600 transition text-xs font-semibold block text-white no-underline">
                    <i class="fa-brands fa-twitter text-sky-400 text-lg mb-1 block"></i> Twitter
                </a>
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
            # Shortening through ShrinkMe API for Monetization
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
        <h4 style="color: #ff4444; font-size: 14px; margin-bottom: 5px;"><i class="fa-solid fa-folder-open"></i> Active Downloads & Gallery Status</h4>
        <p style="color: gray; font-size: 12px; margin: 0;">No downloaded media history yet!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>YT Dodo Universal Media Hub $\\textcircled{c}$ 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)
