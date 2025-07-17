import os
import subprocess
import re
from tkinter import filedialog, messagebox
from utils import verificar_ffmpeg

# ----- Conversão para MP3 com barra de progresso -----


def converter_para_mp3_ffmpeg(caminho_video, convert_bar):
    if not verificar_ffmpeg():
        messagebox.showerror("Erro", "ffmpeg não está instalado no sistema.")
        return None

    mp3_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")],
        title="Salvar como"
    )

    if not mp3_path:
        return None

    try:
        ffmpeg_cmd = "ffmpeg"
        ffprobe_cmd = "ffprobe"

        comando_duracao = [
            ffprobe_cmd, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            caminho_video
        ]
        duracao = float(subprocess.check_output(comando_duracao).decode().strip())

        comando = [
            ffmpeg_cmd, "-i", caminho_video,
            "-vn", "-acodec", "libmp3lame",
            "-y", mp3_path
        ]

        processo = subprocess.Popen(comando, stderr=subprocess.PIPE, universal_newlines=True)

        for linha in processo.stderr:
            if "time=" in linha:
                match = re.search(r"time=(\d+):(\d+):(\d+).(\d+)", linha)
                if match:
                    h, m, s, ms = map(int, match.groups())
                    tempo_atual = h * 3600 + m * 60 + s + ms / 100
                    progresso = min((tempo_atual / duracao), 1.0) * 100
                    convert_bar["value"] = progresso
                    convert_bar.update()

        processo.wait()
        convert_bar["value"] = 0
        os.remove(caminho_video)
        return mp3_path

    except Exception as e:
        convert_bar["value"] = 0
        messagebox.showerror("Erro", f"Erro na conversão:\n{str(e)}")
        return None
