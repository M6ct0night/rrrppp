import tkinter as tk
import random
import subprocess
import time
import os
import threading  # Çoklu iş parçacığı (threading) kullanımı için ekledik

def read_card():
    """Kart adını card.txt dosyasından okur."""
    print("Kart adı dosyadan okunuyor...")
    try:
        with open("card.txt", "r") as file:
            card_value = file.read().strip()  # Dosyadan değeri oku ve boşlukları temizle
        if not card_value:
            print("Hata: Dosya boş!")
            return None
        return card_value
    except FileNotFoundError:
        print("Hata: 'card.txt' dosyası bulunamadı.")
        return None

arayuz = read_card()

def change_family_members_back(event):
    new_members = ["5", "10", "15", "30"]
    current_text = label.cget("text")
    if current_text in new_members:
        prev_index = (new_members.index(current_text) - 1) % len(new_members)
        new_text = new_members[prev_index]
    else:
        new_text = new_members[0]
    label.config(text=new_text)

def change_family_members(event):
    new_members = ["5", "10", "15", "30"]
    current_text = label.cget("text")
    if current_text in new_members:
        next_index = (new_members.index(current_text) + 1) % len(new_members)
        new_text = new_members[next_index]
    else:
        new_text = new_members[0]
    label.config(text=new_text)

def generate_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def macChanger(arayuz):
    mac = generate_mac()
    try:
        subprocess.call(["ifconfig", arayuz, "down"])
        subprocess.call(["ifconfig", arayuz, "hw", "ether", mac])
        subprocess.call(["ifconfig", arayuz, "up"])
    except Exception as e:
        print(f"Hata: MAC adresi değiştirilemedi. Detay: {e}")
        exit(1)

def countdown(minutes):
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        time.sleep(1)
        seconds -= 1

def stagame(event):
    current_text = label.cget("text")
    z = int(current_text)
    label.config(text="MAC değiştiriliyor...")
    def run_mac_change():
        while True:
            macChanger(arayuz)
            countdown(z * 60)
    thread = threading.Thread(target=run_mac_change)  # Yeni iş parçacığı başlatıyoruz
    thread.start()

def stgame(event):
    label.config(text="5")

root = tk.Tk()
root.title("MAC Changer")
root.minsize(height=320, width=480)

# Arka plan resmini yükleme ve ekleme
try:
    resim = tk.PhotoImage(file="BADBMMOO.png")
    background_label = tk.Label(root, image=resim)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Resim yüklenemedi: {e}")

label = tk.Label(root, text="", font=("Arial", 24), fg="black", bg="#C6E4C0")
label.pack(side="bottom", pady=20)

root.bind("<Return>", stgame)
root.bind("<a>", change_family_members_back)
root.bind("<A>", change_family_members_back)
root.bind("<d>", change_family_members)
root.bind("<D>", change_family_members)
root.bind("<w>", stagame)
root.bind("<W>", stagame)
root.bind("Z", lambda event: os.system("python badbmo.py"))
root.bind("s", lambda event: root.quit())

root.mainloop()
