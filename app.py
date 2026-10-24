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

# Initialize Session States for Ad Flow & Saved Data
if "ad_step" not in st.session_state:
    st.session_state.ad_step = False
if "review_step" not in st.session_state:
    st.session_state.review_step = False
if "saved_target_url" not in st.session_state:
    st.session_state.saved_target_url = ""
if "saved_format_type" not in st.session_state:
    st.session_state.saved_format_type = ""

# Professional Custom CSS mirroring your exact HTML/Tailwind Design
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

# Function to shorten URL using ShrinkMe API (Working Logic)
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

# --- 1. TOP DASHBOARD HEADER WITH GOLDEN LIGHTNING ICON & VISITOR COUNTER ---
st.markdown("""
    <div class="w-full max-w-xl mx-auto space-y-6">
        <div class="bg-[#131822]/95 backdrop-blur-md border border-red-500/30 p-5 rounded-2xl shadow-2xl flex items-center justify-between relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-32 h-32 bg-red-600/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="flex items-center space-x-3.5">
                <div class="w-16 h-14 bg-gradient-to-tr from-red-700 via-red-800 to-red-950 rounded-xl flex items-center justify-center shadow-lg shadow-red-600/40 border border-red-400/40 relative overflow-hidden">
                    <span class="text-2xl relative z-10 filter drop-shadow-[0_0_8px_rgba(251,191,36,0.9)] text-amber-400 font-extrabold">⚡</span>
                </div>
                <div>
                    <h1 class="font-extrabold text-xl tracking-wider bg-gradient-to-r from-red-500 via-white to-red-400 bg-clip-text text-transparent">YT DODO</h1>
                    <p class="text-xs font-semibold text-gray-400">Professional Media Hub • Creator: Sagar Shukla</p>
                </div>
            </div>
            <div class="bg-[#0b0f19]/80 border border-gray-700 px-3.5 py-2 rounded-xl flex items-center space-x-2 shadow-inner">
                <span class="w-2.5 h-2.5 bg-green-500 rounded-full animate-pulse"></span>
                <span class="text-xs font-bold text-gray-200">Live: 1,482</span>
            </div>
        </div>

        <!-- Sponsored Banner -->
        <div class="bg-[#131822]/90 border border-dashed border-red-600/60 p-3.5 rounded-xl text-center text-xs text-red-400 shadow-sm backdrop-blur-sm font-medium">
            📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! 
            <a href="https://shrinkme.io" target="_blank" class="font-bold text-red-500 underline ml-1 hover:text-red-400">INSTALL NOW</a>
        </div>

        <!-- Quick Platforms & Shortcuts Section with Original SVGs -->
        <div class="bg-[#131822]/95 backdrop-blur-md border border-gray-800 p-5 rounded-2xl shadow-xl">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 flex items-center gap-1.5">
                <span>🚀</span> Quick Platforms & Shortcuts
            </p>
            <div class="grid grid-cols-4 gap-3">
                <!-- YouTube -->
                <a href="https://www.youtube.com" target="_blank" class="bg-[#1e293b] border border-blue-900/60 hover:border-red-600/60 p-3.5 rounded-xl text-center transition-all duration-200 group shadow-md flex flex-col items-center justify-center" style="text-decoration:none;">
                    <svg class="w-6 h-6 mb-1.5 fill-red-500 transition-transform" viewBox="0 0 24 24" style="width:24px; height:24px;"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    <span class="text-xs font-bold text-gray-200" style="color:#f3f4f6; font-size:12px;">YouTube</span>
                </a>
                <!-- Google -->
                <a href="https://www.google.com" target="_blank" class="bg-[#1e293b] border border-blue-900/60 hover:border-blue-600/60 p-3.5 rounded-xl text-center transition-all duration-200 group shadow-md flex flex-col items-center justify-center" style="text-decoration:none;">
                    <svg class="w-6 h-6 mb-1.5 transition-transform" viewBox="0 0 24 24" style="width:24px; height:24px;"><path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.17z"/><path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.13 0-5.78-2.11-6.73-4.96H1.19v3.15C3.21 21.32 7.23 24 12 24z"/><path fill="#FBBC05" d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.19C.43 8.14 0 9.87 0 12s.43 3.86 1.19 5.39l4.08-3.15z"/><path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.23 0 3.21 2.68 1.19 6.61l4.08 3.15c.95-2.85 3.6-4.96 6.73-4.96z"/></svg>
                    <span class="text-xs font-bold text-gray-200" style="color:#f3f4f6; font-size:12px;">Google</span>
                </a>
                <!-- Facebook -->
                <a href="https://www.facebook.com" target="_blank" class="bg-[#1e293b] border border-blue-900/60 hover:border-blue-500/60 p-3.5 rounded-xl text-center transition-all duration-200 group shadow-md flex flex-col items-center justify-center" style="text-decoration:none;">
                    <svg class="w-6 h-6 mb-1.5 fill-[#1877F2] transition-transform" viewBox="0 0 24 24" style="width:24px; height:24px;"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    <span class="text-xs font-bold text-gray-200" style="color:#f3f4f6; font-size:12px;">Facebook</span>
                </a>
                <!-- Instagram -->
                <a href="https://www.instagram.com" target="_blank" class="bg-[#1e293b] border border-blue-900/60 hover:border-pink-600/60 p-3.5 rounded-xl text-center transition-all duration-200 group shadow-md flex flex-col items-center justify-center" style="text-decoration:none;">
                    <svg class="w-6 h-6 mb-1.5 fill-[#E4405F] transition-transform" viewBox="0 0 24 24" style="width:24px; height:24px;"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    <span class="text-xs font-bold text-gray-200" style="color:#f3f4f6; font-size:12px;">Instagram</span>
                </a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. UNIVERSAL VIDEO & MEDIA DOWNLOADER HUB ---
st.markdown("""
    <div class="w-full max-w-xl mx-auto space-y-6 mt-6">
        <div class="bg-[#131822]/95 backdrop-blur-md border border-gray-800 p-5 sm:p-6 rounded-2xl shadow-xl space-y-4">
            <h2 class="text-sm font-bold text-red-500 uppercase tracking-wide flex items-center gap-2" style="color:#ef4444;">
                <span>🔍</span> Universal Video & Media Downloader
            </h2>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

# Step 1: Clean Search Button (Working Backend Trigger)
if st.button("Search", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True
    st.session_state.review_step = False

# Step 2: Show Search and Review button linked with ShrinkMe ad
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)
    
    st.markdown(f"""
        <div class="space-y-3 pt-2">
            <div class="bg-[#0b0f19] border border-red-600/50 p-4 rounded-xl text-center space-y-2">
                <p class="text-xs font-semibold text-gray-300">👇 Click below to proceed with search & review:</p>
                <a href="{shortened_ad_url}" target="_blank" class="block w-full bg-gradient-to-r from-red-600 to-red-800 text-white font-bold py-3 rounded-lg text-sm shadow-md hover:opacity-90 transition-opacity" style="color:white; text-decoration:none; display:block; background:linear-gradient(to right, #dc2626, #991b1b); padding:12px; border-radius:8px; font-weight:bold;">
                    Search and Review
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ Click here after review to load media player", use_container_width=True):
        st.session_state.review_step = True

# Step 3: Media Player & Download Section (yt_dlp Working Backend)
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
                <div class="space-y-4 pt-3 border-t border-gray-800">
                    <div class="bg-[#1f242d] border border-gray-800 rounded-t-xl px-4 py-3 flex items-center space-x-2">
                        <span class="text-base">🎵</span>
                        <p class="text-sm font-bold text-white truncate">{title}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.video(direct_url)
            
            st.markdown(f"""
                <a href="{shortened_url}" target="_blank" style="display:block; width:100%; background:linear-gradient(to right, #2563eb, #1d4ed8); color:white; font-weight:bold; padding:14px 16px; border-radius:12px; text-align:center; text-decoration:none; margin-top:15px; margin-bottom:12px; box-shadow:0 10px 25px -5px rgba(37, 99, 235, 0.4);">
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

# --- 3. ACTIVE DOWNLOADS STATUS & FOOTER ---
st.markdown("""
    <div class="w-full max-w-xl mx-auto space-y-6 mt-6">
        <div class="bg-[#131822]/95 backdrop-blur-md border border-gray-800 p-5 rounded-2xl shadow-xl space-y-2">
            <h3 class="text-xs font-bold text-red-500 uppercase tracking-wide" style="color:#ef4444;">📁 Gallery & Active Downloads Status</h3>
            <p class="text-xs text-gray-400 leading-relaxed" style="color:#9ca3af;">
                No active downloads right now. Completed items will appear here securely!
            </p>
        </div>
        
        <footer class="mt-8 text-center text-xs text-gray-400 border-t border-gray-800/60 pt-4 w-full pb-6" style="border-top:1px solid rgba(31, 41, 55, 0.6); text-align:center; color:#9ca3af; font-size:12px; margin-top:30px; padding-top:15px;">
            YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla
        </footer>
    </div>
""", unsafe_allow_html=True)
