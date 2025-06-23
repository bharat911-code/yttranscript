from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import os

# ----------- USER INPUT -------------
playlist_url = "https://youtube.com/playlist?list=PL5g3ONxcyva_9Y50NpzxVRlB7g_R-PCZO&si=9Dt0uCupC74lDxV_"  # Replace this
output_folder = "hindi_transcripts"
# -------------------------------------

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get all video URLs from the playlist
playlist = Playlist(playlist_url)
video_urls = playlist.video_urls

print(f"Found {len(video_urls)} videos in the playlist.")

for index, video_url in enumerate(video_urls, start=1):
    video_id = video_url.split("v=")[-1].split("&")[0]

    try:
        # Try fetching Hindi transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        transcript_text = "\n".join([entry['text'] for entry in transcript])

        # Save transcript to file
        file_name = f"video_{index:02d}_{video_id}_hi.txt"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        print(f"✓ Saved Hindi transcript for video {index}: {video_id}")

    except TranscriptsDisabled:
        print(f"✗ Transcripts are disabled for video {index}: {video_id}")
    except NoTranscriptFound:
        print(f"✗ No Hindi transcript found for video {index}: {video_id}")
    except Exception as e:
        print(f"⚠️ Error with video {index}: {video_id} — {str(e)}")

print("\n🎉 Finished fetching Hindi transcripts.")

from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/transcript", methods=["GET"])
def transcript():
    video_id = request.args.get("video_id")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
        text = " ".join([t["text"] for t in transcript])
        return jsonify({"transcript": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
