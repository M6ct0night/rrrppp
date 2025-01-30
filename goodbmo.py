import subprocess
import tkinter as tk
from games.games import spacewariors
import os
from gamestarter import flappyHusein, dino, mushroom, tetris, snake, ikdört


def change_family_members_back(event):
    # Aile üyeleri listesini belirleyin
    new_members = ["space wariors", "Flappy Huseyin", "dino", "mushroom", "mushroom",
                   "tetris", "snake", "2048"]

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in new_members:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir önceki üyeye geç
        prev_index = (new_members.index(current_text) - 1) % len(new_members)
        new_text = new_members[prev_index]
    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = new_members[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)

def zz():
    os.system("python wificard.py")
    root.destroy()


def change_family_members(event):
    # Aile üyeleri listesini belirleyin
    new_members = ["space wariors", "Flappy Huseyin", "dino", "mushroom", "mushroom",
                   "tetris", "snake", "2048"]

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in new_members:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir sonraki üyeye geç
        next_index = (new_members.index(current_text) + 1) % len(new_members)
        new_text = new_members[next_index]
    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = new_members[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)

def stagame(event):
    current_text = label.cget("text")

    if not current_text:  # Eğer metin boşsa, varsayılan olarak space wariors başlat
        current_text = "space wariors"
        pass
    if current_text == "space wariors":
        spacewariors()
    elif current_text == "Flappy Huseyin":
        flappyHusein()
    elif current_text == "dino":
        dino()
    elif current_text == "mushroom":
        mushroom()
    elif current_text == "tetris":
        tetris()
    elif current_text == "snake":
        snake()
    elif current_text == "2048":
        ikdört()


def stgame(event):
    # Yazıyı eklemek için label'ı güncelle
    label.config(text="space wariors")  # Başlangıçta görülecek yazı


# Ana pencereyi oluştur
root = tk.Tk()
root.title("bmoo")
root.minsize(height=320, width=480)



try:
    resim = tk.PhotoImage(file="BMMOO.png")
    # Arka plan resmi eklemek için bir Label widget'ı oluştur
    background_label = tk.Label(root, image=resim)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Etiketin pencereye tam oturmasını sağlar
except Exception as e:
    print(f"Resim yüklenemedi: {e}")


# Label widget'ını oluştur ve yazıyı ekle
label = tk.Label(root, text="", font=("Arial", 24), fg="black",
                 bg="#C6E4C0")  # bg ekleyerek daha görünür yapabilirsiniz

label.pack(side="bottom", pady=20, )


# 'Enter' tuşu ile yazıyı ekle
root.bind("<Return>", stgame)


# 'A' tuşu ile bir önceki oyunu seç
root.bind("<a>", change_family_members_back)
root.bind("<A>", change_family_members_back)


# 'D' tuşu ile bir sonraki oyunu seç
root.bind("<d>", change_family_members)
root.bind("<D>", change_family_members)


# 'W' tuşu ile seçilen oyunu başlat
root.bind("<w>", stagame)
root.bind("<W>", stagame)


root.bind("Z", zz )
root.bind("S", lambda event: root.quit)
root.mainloop()
