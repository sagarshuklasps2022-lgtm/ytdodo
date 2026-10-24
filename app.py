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

# Robust Secure Session State Initialization for Users & Auth
if "users_db" not in st.session_state:
    st.session_state.users_db = {"sagar": {"password": "Sagar@123", "yt_dodo_id": "YTDODO_463385"}}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "remember_user" not in st.session_state:
    st.session_state.remember_user = ""
if "remember_pass" not in st.session_state:
    st.session_state.remember_pass = ""
if "new_account_created" not in st.session_state:
    st.session_state.new_account_created = False
if "pending_yt_id" not in st.session_state:
    st.session_state.pending_yt_id = ""
if "pending_pass" not in st.session_state:
    st.session_state.pending_pass = ""
if "pending_user" not in st.session_state:
    st.session_state.pending_user = ""
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"
if "app_lang" not in st.session_state:
    st.session_state.app_lang = "English"

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
    .login-container {{
        background: {card_bg};
        padding: 30px;
        border-radius: 24px;
        border: 1px solid {border_color};
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        text-align: center;
        margin-top: 20px;
    }}
    .banner-badge {{
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 15px;
    }}
    .login-header {{
        color: {text_color};
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    .login-subheader {{
        color: {sub_text};
        font-size: 13px;
        margin-bottom: 20px;
    }}
    .feature-box {{
        display: flex;
        justify-content: space-around;
        background: {bg_color};
        padding: 15px;
        border-radius: 16px;
        border: 1px solid {border_color};
        margin-top: 20px;
        margin-bottom: 20px;
        font-size: 12px;
        color: {text_color};
        font-weight: 600;
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

# --- SECURE AUTHENTICATION & REGISTRATION FLOW ---
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<span class="banner-badge">👑 NEXT-GEN MEDIA DOWNLOADER</span>', unsafe_allow_html=True)
    st.markdown('<p class="login-header">YT DODO APP</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="login-subheader">{"Universal Video & Media Downloader" if st.session_state.app_lang=="English" else "यूनिवर्सल वीडियो और मीडिया डाउनलोडर"}</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-box">
            <span>⚡ Ultra Fast</span>
            <span>🌐 Anytime Anywhere</span>
            <span>🛡️ 100% Secure</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        if st.session_state.auth_mode == "login":
            st.markdown(f'<h4 style="text-align: left; color: #ff0000; font-size: 16px;">{"🔐 Secure Sign In" if st.session_state.app_lang=="English" else "🔐 सुरक्षित साइन इन"}</h4>', unsafe_allow_html=True)
            
            default_user = st.session_state.remember_user if st.session_state.remember_user else ""
            default_pass = st.session_state.remember_pass if st.session_state.remember_pass else ""

            with st.form("login_form"):
                username_input = st.text_input("Username / YT Dodo ID", value=default_user, placeholder="user@ytdodo.app or YTDODO_xxxxxx")
                password_input = st.text_input("Password", value=default_pass, type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("Sign In")

            if st.session_state.new_account_created:
                st.success("🎉 Account Created Successfully!")
                shrink_dummy_url = shorten_with_shrinkme("https://ytdodo.app/welcome")
                st.markdown(
                    f'<div style="background:{card_bg}; padding:15px; border-radius:12px; border:1px solid #dc2626; margin-bottom:15px;">'
                    f'<p style="color:{text_color}; font-size:12px; margin-bottom:8px;"><b>✨ Your Unique YT Dodo ID:</b> <span style="color:#f87171;">{st.session_state.pending_yt_id}</span></p>'
                    f'<a href="{shrink_dummy_url}" target="_blank" style="display:block;padding:12px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:8px;font-weight:bold;text-align:center;font-size:13px;">🔗 Activate Account via Secure Ad Link</a>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if st.button("I have clicked & verified! Proceed to Login"):
                    st.session_state.remember_user = st.session_state.pending_yt_id
                    st.session_state.remember_pass = st.session_state.pending_pass
                    st.session_state.new_account_created = False
                    st.rerun()

            if submit_login:
                matched_user = None
                for uname, udata in st.session_state.users_db.items():
                    if (uname.lower() == username_input.strip().lower() or udata["yt_dodo_id"].lower() == username_input.strip().lower()) and udata["password"] == password_input:
                        matched_user = uname
                        break
                
                if matched_user:
                    shrink_signin_url = shorten_with_shrinkme(f"https://ytdodo.app/login?user={matched_user}")
                    st.markdown(
                        f'<div style="background:{card_bg}; padding:15px; border-radius:12px; border:1px solid #dc2626; margin-bottom:15px;">'
                        f'<p style="color:{text_color}; font-size:12px; margin-bottom:8px;"><b>🔒 Security Checkpoint:</b> Verified ID: <code>{st.session_state.users_db[matched_user]["yt_dodo_id"]}</code></p>'
                        f'<a href="{shrink_signin_url}" target="_blank" style="display:block;padding:12px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:8px;font-weight:bold;text-align:center;font-size:13px;">🚀 Click Here to Proceed to Dashboard</a>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.session_state.logged_in = True
                    st.session_state.current_user = matched_user
                    st.session_state.remember_user = username_input
                    st.session_state.remember_pass = password_input
                else:
                    st.error("Invalid Credentials!")
            
            if st.button("Go to Dashboard Directly (After Ad Click)", use_container_width=True):
                if st.session_state.logged_in:
                    st.rerun()
                else:
                    st.warning("Please complete sign in above.")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Create Account"):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
            with col_b:
                if st.button("Forgot Password?"):
                    st.session_state.auth_mode = "forgot"
                    st.rerun()

        elif st.session_state.auth_mode == "signup":
            st.markdown('<h4 style="text-align: left; color: #ff0000; font-size: 16px;">📝 Create New Account</h4>', unsafe_allow_html=True)
            with st.form("signup_form"):
                new_user = st.text_input("Choose Username", placeholder="new_user")
                new_pass = st.text_input("Create Password", type="password", placeholder="••••••••")
                confirm_pass = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                submit_signup = st.form_submit_button("Register Account")
            
            if submit_signup:
                if not new_user or not new_pass:
                    st.error("Please fill all details.")
                elif new_user in st.session_state.users_db:
                    st.error("Username already exists!")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                else:
                    unique_yt_id = f"YTDODO_{random.randint(100000, 999999)}"
                    st.session_state.users_db[new_user] = {"password": new_pass, "yt_dodo_id": unique_yt_id}
                    st.session_state.pending_yt_id = unique_yt_id
                    st.session_state.pending_pass = new_pass
                    st.session_state.pending_user = new_user
                    st.session_state.new_account_created = True
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

        elif st.session_state.auth_mode == "forgot":
            st.markdown('<h4 style="text-align: left; color: #ff0000; font-size: 16px;">🔄 Recover Password</h4>', unsafe_allow_html=True)
            with st.form("forgot_form"):
                recovery_user = st.text_input("Enter your Username or YT Dodo ID")
                submit_forgot = st.form_submit_button("Fetch Account Details")
            
            if submit_forgot:
                found = False
                for uname, udata in st.session_state.users_db.items():
                    if uname.lower() == recovery_user.strip().lower() or udata["yt_dodo_id"].lower() == recovery_user.strip().lower():
                        st.info(f"Account Found! Username: {uname} | Password: {udata['password']}")
                        found = True
                        break
                if not found:
                    st.error("User or ID not found.")
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MAIN DASHBOARD WITH SQUARE BIJLI ICON ---
    current_uid = st.session_state.users_db.get(st.session_state.current_user, {}).get("yt_dodo_id", "YTDODO_PRO")
    
    st.markdown(f"""
        <div class="main-header">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 12px; color: white; font-size: 22px; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                    ⚡
                </div>
                <div>
                    <h3 style="color: {text_color}; font-weight: bold; font-size: 17px; margin: 0;">YT DODO</h3>
                    <p style="color: {sub_text}; font-size: 11px; margin: 0;">Welcome, {st.session_state.current_user.capitalize()} | ID: <code>{current_uid}</code></p>
                </div>
            </div>
            <div>
                <span style="background-color: {card_bg}; padding: 8px 12px; border-radius: 12px; font-size: 14px; border: 1px solid {border_color};">☁️ Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

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

    # --- Search & Download Hub (Universal Video & Reels) ---
    st.markdown(f"""
        <div class="card-box" style="margin-top: 25px;">
            <h3 style="color: #dc2626; font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px;">🔍 Universal Video & Media Downloader</h3>
    """, unsafe_allow_html=True)

    target_url = st.text_input("Paste any YouTube, Instagram or Video link...", placeholder="https://www.youtube.com/watch?v=...")
    format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio"])

    if st.button("Search & Prepare Download", use_container_width=True) and target_url:
        try:
            if "MP3" in format_type.upper():
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
                info = ydl.extract_info(target_url, download=False)
                direct_url = info.get("url")
                title = info.get("title", "Media_Video")

            if direct_url:
                shortened_url = shorten_with_shrinkme(direct_url)
                
                st.success("Media Ready for Playback & Download!")
                
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
                
                # Monetized Ad Download Link Button
                st.markdown(
                    f'<a href="{shortened_url}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.4); margin-top: 15px; margin-bottom: 12px;">📥 Download (Via Ad Link)</a>',
                    unsafe_allow_html=True,
                )
                
                # Direct Stream Downloader link with proper filename attribute
                st.markdown(
                    f'<a href="{direct_url}" download="{filename}" style="display:block;padding:14px 20px;background:linear-gradient(135deg, #21262d, #161b22);color:#9ca3af;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:14px;border: 1px solid #30363d;">⬇️ Direct Video Download ({filename[:40]}...)</a>',
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
            <h4 style="color: #dc2626; font-size: 14px; font-weight: bold; margin-bottom: 8px;">📁 Gallery & Active Downloads Status: Ready to manage your downloaded media</h4>
            <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.6;">
                No active downloads right now. Completed items will appear here!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Final Footer
st.markdown(f"<hr style='border-color: {border_color}; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {sub_text}; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | Created by Sagar Shukla</p>", unsafe_allow_html=True)
