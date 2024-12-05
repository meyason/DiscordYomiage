from yt_dlp import YoutubeDL

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
         'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://youtu.be/_KpYws49HWk?si=9lwMFoaGWnJt_I9H'])

