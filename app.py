import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-video-info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL missing'}), 400
    
    try:
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android_vr", "android", "web"]
                }
            },
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'YT Dodo Media Stream')
            stream_url = info.get('url', '')
            
            if not stream_url and 'formats' in info:
                for f in info['formats']:
                    if f.get('url') and f.get('vcodec') != 'none' and f.get('ext'] == 'mp4':
                        stream_url = f['url']
                        break
                if not stream_url:
                    for f in info['formats']:
                        if f.get('url') and f.get('vcodec') != 'none':
                            stream_url = f['url']
                            break

            return jsonify({
                'title': title, 
                'stream_url': stream_url
            })
    except Exception as e:
        return jsonify({
            'title': 'YT Dodo Media Stream', 
            'stream_url': ''
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
