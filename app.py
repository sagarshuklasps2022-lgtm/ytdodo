from flask import Flask, render_template, request, jsonify
import yt_dlp
import requests

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    data = request.json
    target_url = data.get('url')
    format_type = data.get('format', '720p')
    
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
            title = info.get("title", "YT Dodo Media Stream")

        if direct_url:
            shortened_download_link = shorten_with_shrinkme(direct_url)
            shortened_ad_link = shorten_with_shrinkme(target_url)
            
            return jsonify({
                "success": True,
                "title": title,
                "direct_url": direct_url,
                "download_link": shortened_download_link,
                "ad_link": shortened_ad_link
            })
        else:
            return jsonify({"success": False, "error": "Could not extract link."})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)