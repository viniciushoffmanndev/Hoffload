from pytubefix import YouTube
import os

def baixar_video(url, pasta_destino="."):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Baixando: {yt.title}")
        caminho = stream.download(output_path=pasta_destino)
        print(f"Download concluído: {caminho}")
    except Exception as e:
        print(f"Erro ao baixar vídeo: {str(e)}")

if __name__ == "__main__":
    # Cole o link do vídeo aqui
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Pasta onde salvará o vídeo
    pasta = os.path.join(os.getcwd(), "downloads")
    os.makedirs(pasta, exist_ok=True)

    baixar_video(url, pasta)











