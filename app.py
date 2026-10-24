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
if "saved_target_url" not in st.session_state:
    st.session_state.saved_target_url = ""
if "saved_format_type" not in st.session_state:
    st.session_state.saved_format_type = ""

# Dynamic Theme Colors based on user selection
if st.session_state.theme_mode == "Dark":
    bg_color = "#0b0f19"
    card_bg = "#131822"
    text_color = "#ffffff"
    border_color = "#30363d"
    sub_text = "#9ca3af"
else:
    bg_color = "#f3f4f6"
    card_bg = "#ffffff"
    text_color = "#1f2937"
    border_color = "#d1d5db"
    sub_text = "#4b5563"

# Professional Custom CSS & UI Styling with Dynamic Themes
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .stTextInput input {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 6px 15px rgba(220, 38, 38, 0.4);
        width: 100%;
    }}
    .main-header {{
        background: {card_bg};
        padding: 20px;
        border-radius: 20px;
        border: 1px solid {border_color};
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    .card-box {{
        background: {card_bg};
        padding: 25px;
        border-radius: 20px;
        border: 1px solid {border_color};
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    .shortcut-btn {{
        background: {card_bg};
        border: 1px solid {border_color};
        padding: 18px 10px;
        border-radius: 18px;
        text-align: center;
        color: {text_color};
        text-decoration: none;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-bottom: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    .sponsored-banner {{
        background: {card_bg};
        border: 1px dashed #dc2626;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 12px;
        color: #ef4444;
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

# --- DIRECT DASHBOARD ---
st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 12px; color: white; font-size: 22px; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                ⚡
            </div>
            <div>
                <h3 style="color: {text_color}; font-weight: bold; font-size: 17px; margin: 0;">YT DODO</h3>
                <p style="color: {sub_text}; font-size: 11px; margin: 0;">Universal Media Hub | Creator: Sagar Shukla</p>
            </div>
        </div>
        <div>
            <span style="background-color: {card_bg}; padding: 8px 12px; border-radius: 12px; font-size: 14px; border: 1px solid {border_color};">☁️ Online</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sponsored Banner Ad
st.markdown("""
    <div class="sponsored-banner">
        📢 <b>SPONSORED:</b> Play Free Games & Win Big Rewards on YT Dodo Hub! <a href="https://shrinkme.io" target="_blank" style="color:#ef4444; font-weight:bold;">INSTALL NOW</a>
    </div>
""", unsafe_allow_html=True)

# Quick Shortcuts Section
st.markdown(f"""
    <div class="card-box" style="padding-bottom: 15px;">
        <p style="color: {sub_text}; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;">Quick Platforms & Shortcuts</p>
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

# --- Search & Monetized Ad Flow Hub ---
st.markdown(f"""
    <div class="card-box" style="margin-top: 25px;">
        <h3 style="color: #dc2626; font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px;">🔍 Universal Video & Media Downloader</h3>
""", unsafe_allow_html=True)

target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

# Step 1: User clicks search button to trigger ad
if st.button("Search & View Sponsored Ad", use_container_width=True) and target_url:
    st.session_state.saved_target_url = target_url
    st.session_state.saved_format_type = format_type
    st.session_state.ad_step = True

# If ad step is triggered, show the monetized link and return verification button
if st.session_state.ad_step and st.session_state.saved_target_url:
    current_link = st.session_state.saved_target_url
    shortened_ad_url = shorten_with_shrinkme(current_link)
    
    st.markdown(
        f'<div style="background:{card_bg}; padding:18px; border-radius:14px; border:1px solid #dc2626; margin-top:20px; margin-bottom:15px; text-align:center;">'
        f'<p style="color:{text_color}; font-size:13px; font-weight:bold; margin-bottom:10px;">🎁 Step 1: Click below to support creator & unlock media search:</p>'
        f'<a href="{shortened_ad_url}" target="_blank" style="display:block;padding:14px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:10px;font-weight:bold;font-size:14px;">🔗 Click Here to Open Sponsored Ad Link</a>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Step 2: Confirmation button after visiting ad
    if st.button("✅ I have completed the ad! Load Media Player", use_container_width=True):
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
                
                # Clean filename generator
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
                filename = f"{safe_title}.mp4"
                
                # Video Player Display with Exact Video Title Header on Top
                st.markdown(f"""
                    <div style="background:#1f242d; padding:12px 18px; border-radius:12px 12px 0 0; border:1px solid {border_color}; border-bottom:none; display:flex; align-items:center; gap:10px;">
                        <span style="font-size:18px;">🎵</span>
                        <p style="color:#ffffff; font-size:15px; font-weight:bold; margin:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{title}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.video(direct_url)
                
                # 1. Download Button (Via Ad Link / ShrinkMe)
                st.markdown(
                    f'<a href="{shortened_url}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.4); margin-top: 15px; margin-bottom: 12px;">Download</a>',
                    unsafe_allow_html=True,
                )
                
                # 2. Direct Video Download using server-side yt_dlp processing
                if st.button("Direct Video Download", use_container_width=True):
                    with st.spinner("Downloading media securely... Please wait."):
                        try:
                            out_file = f"ytdodo_{random.randint(1000,9999)}.mp4"
                            dl_opts = {
                                "format": "best[ext=mp4]/best",
                                "outtmpl": out_file,
                                "noplaylist": True,
                                "geo_bypass": True,
                                "nocheckcertificate": True,
                                "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
                            }
                            with yt_dlp.YoutubeDL(dl_opts) as ydl_dl:
                                ydl_dl.download([active_url])
                            
                            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                                with open(out_file, "rb") as f:
                                    video_bytes = f.read()
                                os.remove(out_file)
                                st.download_button(
                                    label="💾 Click here to save file now",
                                    data=video_bytes,
                                    file_name=filename,
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                                st.success("File ready! Click the save button above.")
                            else:
                                st.error("Download failed or file is empty.")
                        except Exception as e:
                            st.error(f"Download error: {e}")
            else:
                st.error("The media link could not be processed.")

        except Exception as ex:
            st.error(f"Extraction error: {ex}")

st.markdown("</div>", unsafe_allow_html=True)

# Active Downloads Status Box
st.markdown("""
    <div class="card-box">
        <h4 style="color: #dc2626; font-size: 14px; font-weight: bold; margin-bottom: 8px;">📁 Gallery & Active Downloads Status: Ready to manage your downloaded media</h4>
        <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.6;">
            No active downloads right now. Completed items will appear here!
        </p>
    </div>
""", unsafe_allow_html=True)

# Final Footer
st.markdown(f"<hr style='border-color: {border_color}; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sub_text}; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
