import threading
from tkinter import filedialog, messagebox
from pytubefix import YouTube
from pytubefix.exceptions import (VideoUnavailable, RegexMatchError, LiveStreamError, AgeRestrictedError, LoginRequired)
from utils import limpar_url, abrir_pasta
from convert import converter_para_mp3_ffmpeg

# ----- Download de vídeo com tratamento de erros -----

def atualizar_barra(stream, chunk, bytes_remaining, progress_bar):
    total = stream.filesize
    baixado = total - bytes_remaining
    progress_bar["maximum"] = total
    progress_bar["value"] = baixado

def baixar_video(url_var, mp3_var, status_var, pasta_var, progress_bar, convert_bar):
    try:
        url = limpar_url(url_var.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um link válido do YouTube.")
        return

    converter = mp3_var.get()
    status_var.set("Iniciando download...")

    def processo():
        try:
            yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: atualizar_barra(stream, chunk, bytes_remaining, progress_bar))
            stream = yt.streams.get_highest_resolution()

            pasta_destino = filedialog.askdirectory(title="Escolher pasta para salvar o vídeo")
            if not pasta_destino:
                status_var.set("Download cancelado.")
                return

            pasta_var.set(f"Pasta escolhida: {pasta_destino}")
            status_var.set(f"Baixando: {yt.title}")
            caminho = stream.download(output_path=pasta_destino)

            if converter:
                status_var.set("Convertendo para MP3...")
                mp3_path = converter_para_mp3_ffmpeg(caminho, convert_bar)
                if not mp3_path:
                    status_var.set("Conversão cancelada.")
                    return
                status_var.set("Download e conversão concluídos!")
                abrir_pasta(pasta_destino)
            else:
                status_var.set("Download concluído!")
                abrir_pasta(pasta_destino)

        except VideoUnavailable:
            status_var.set("Erro: Vídeo indisponível.")
            messagebox.showerror("Erro", "Este vídeo não está disponível no YouTube.")
        except AgeRestrictedError:
            status_var.set("Erro: Vídeo com restrição de idade.")
            messagebox.showerror("Erro", "Este vídeo possui restrição de idade.")
        except LiveStreamError:
            status_var.set("Erro: É uma transmissão ao vivo.")
            messagebox.showerror("Erro", "Não é possível baixar transmissões ao vivo.")
        except RegexMatchError:
            status_var.set("Erro: Link inválido.")
            messagebox.showerror("Erro", "O link inserido não é válido.")
        except LoginRequired:
            status_var.set("Erro: Login necessário.")
            messagebox.showerror("Erro", "Este vídeo requer login para ser acessado.")
        except Exception as e:
            status_var.set("Erro ao baixar")
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{str(e)}")

    threading.Thread(target=processo).start()
