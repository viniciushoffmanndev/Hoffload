import os
import platform
import shutil
import subprocess
from urllib.parse import urlparse, parse_qs

def limpar_url(url):
    parsed = urlparse(url)
    if 'youtube.com' in parsed.netloc:
        query = parse_qs(parsed.query)
        video_id = query.get('v', [None])[0]
    elif 'youtu.be' in parsed.netloc:
        video_id = parsed.path.strip('/')
    else:
        video_id = None

    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        raise ValueError("URL inválida ou não reconhecida.")

def verificar_ffmpeg():
    return shutil.which("ffmpeg") is not None

def abrir_pasta(path):
    sistema = platform.system()
    if sistema == "Linux":
        subprocess.run(["xdg-open", path])
    elif sistema == "Windows":
        os.startfile(path)
    elif sistema == "Darwin":
        subprocess.run(["open", path])
