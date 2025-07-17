import os
from tkinter import Tk, Label, Entry, Button, Checkbutton, IntVar, StringVar, messagebox, Frame, ttk
from PIL import Image, ImageTk
from downloader import baixar_video

# ----- Interface gráfica com Tkinter + Awthemes -----

def criar_interface():
    global convert_bar, progress_bar

    app = Tk()
    app.config(background="#FFFFFF")
    app.title("Hoffload - YouTube Downloader")
    app.geometry("500x300")
    app.resizable(False, False)

    # Variáveis globais
    url_var = StringVar()
    mp3_var = IntVar()
    status_var = StringVar()
    pasta_var = StringVar()

    # Barras de progresso
    progress_bar = ttk.Progressbar(app, length=400, mode='determinate')
    progress_bar.grid(row=4, column=0, columnspan=4, pady=5)

    convert_bar = ttk.Progressbar(app, length=400, mode='determinate')
    convert_bar.grid(row=5, column=0, columnspan=4, pady=5)

    # Entrada de URL
    Label(app, text="Link do vídeo:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    Entry(app, textvariable=url_var, width=50).grid(row=0, column=1, padx=10, pady=10, columnspan=2)

    # Botão de colar da área de transferência
    def colar_url():
        try:
            url_var.set(app.clipboard_get().strip())
        except:
            messagebox.showwarning("Aviso", "Não foi possível colar da área de transferência.")

    Button(app, text="Colar", command=colar_url, bg="#ffffff").grid(row=0, column=3, padx=5)

    # Checkbox de conversão
    Checkbutton(app, text="Converter para MP3", variable=mp3_var, bg="#ffffff").grid(row=1, column=1, sticky="w", padx=10)

    # Botão de download
    Button(app, text="Baixar", width=20, bg="#ffffff", command=lambda: baixar_video(url_var, mp3_var, status_var, pasta_var, progress_bar, convert_bar)).grid(row=2, column=1, pady=15)

    # Status e pasta de destino
    Label(app, textvariable=status_var, fg="blue", bg="#ffffff").grid(row=3, column=0, columnspan=4, pady=5)
    Label(app, textvariable=pasta_var, fg="gray", bg="#ffffff").grid(row=6, column=0, columnspan=4, pady=5)

    # Rodapé com créditos
    footer = Frame(app, bg="#ffffff")
    footer.grid(row=7, column=0, columnspan=4, pady=(5, 10))

    Label(footer, text="Desenvolvido por Vinicius Hoffmann", fg="gray", bg="#ffffff", font=("Arial", 8)).pack(side="left", padx=(0, 10))

    app.mainloop()
