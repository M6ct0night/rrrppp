from scapy.all import *
from threading import Thread, Event
import os
import tkinter as tk


def read_card2():
    try:
        with open("card2.txt", "r") as file:
            global card_value
            card_value = file.read().strip()  # Dosyadan değeri oku ve boşlukları temizle
        return card_value
    except FileNotFoundError:
        print("değer bulunamadı")  # Eğer dosya bulunamazsa, bir hata yerine bir varsayılan değer döndür
        return None


interface = read_card2()

# Bulunan ağları tutmak için bir liste
found_networks = []
stop_sniffing_event = Event()


def packet_handler(packet):
    """Wi-Fi paketlerini işler."""
    if stop_sniffing_event.is_set():
        return  # Eğer durdurma isteği varsa, paketi işlemeden çık

    if packet.haslayer(Dot11Beacon):
        # SSID'yi al ve boşsa 'Gizli Ağ' olarak ayarla
        ssid = packet[Dot11Elt].info.decode() if packet[Dot11Elt].info else "Gizli Ağ"

        # BSSID'yi kontrol et ve 'Gizli Ağ' olarak ayarla
        bssid = packet[Dot11].addr2 if packet[Dot11].addr2 else "Gizli Ağ"

        channel = ord(packet[Dot11Elt:3].info)  # Kanal bilgisini al

        if (ssid, bssid, channel) not in found_networks:
            found_networks.append((ssid, bssid, channel))

            # Bulunan ağları sıralayıp yazdır
            sorted_networks = sorted(found_networks, key=lambda x: (x[0], x[1], x[2]))
            display_networks(sorted_networks)
            print_networks(sorted_networks)

            # Bulunan ağları sıralayıp scanlist.txt'ye yaz
            with open("scanlist.txt", "w") as file:
                # `scanlist` adlı liste içinde ağları yaz
                file.write(f"scanlist = {repr(sorted_networks)}\n")


def display_networks(sorted_networks):
    """Tkinter penceresinde ağları sadece SSID ve sırası ile gösterir."""
    # Pencereyi temizle
    for widget in network_list_frame.winfo_children():
        widget.destroy()

    # Her ağ için bir etiket oluştur, ve sola hizalı yaz
    for idx, (ssid, _, _) in enumerate(sorted_networks, 1):
        label = tk.Label(network_list_frame, text=f"[{idx}] SSID: {ssid}", font=("Helvetica", 12), fg="green",
                         bg="black", anchor="w")
        label.pack(fill="x")  # Etiketlerin tam genişlikte hizalanmasını sağlar

    # "Ağlar taranıyor. Taramayı sonladırmak için 'W' tuşuna basabilirsiniz." mesajını göster
    info_label = tk.Label(network_list_frame,
                          text="Ağlar taranıyor. Taramayı sonlandirabilmek için 'W' tuşuna basabilirsiniz.",
                          font=("Helvetica", 10), fg="yellow", bg="black", anchor="w")
    info_label.pack(fill="x")


def print_networks(sorted_networks):
    """Terminalde ağları sadece SSID ve sırası ile gösterir."""
    print("\n[+] Bulunan ağlar (sıralanmış):")
    for idx, (ssid, _, _) in enumerate(sorted_networks, 1):
        print(f"[{idx}] SSID: {ssid}")


def start_sniffing(interface):
    """Belirtilen arayüzde paketleri dinler."""
    print(f"[+] Wi-Fi taraması başlatılıyor ({interface})...")
    sniff(iface=interface, prn=packet_handler, store=False)


def on_close():
    """Pencereyi kapatırken yapılacak işlemler."""
    print("[!] Program sonlandırılıyor...")
    stop_sniffing_event.set()  # Tarama durdurulacak
    root.quit()


def on_key_press(event):
    """W tuşuna basıldığında taramayı durdur."""
    if event.char == 'w' or event.keysym == 'w':
        print("[!] Tarama durduruluyor...")
        stop_sniffing_event.set()  # Tarama durdurulacak
        stop_message_label.config(text="Tarama sonlandırıldı.")  # 'Tarama sonlandırıldı' mesajını göster


if __name__ == "__main__":

    # Tkinter penceresini başlat
    root = tk.Tk()
    root.title("Wi-Fi Ağ Tarayıcı")

    # Pencere boyutunu ayarla
    root.geometry("480x320")

    # Arka plan rengini siyah ve yazı rengini yeşil yap
    root.config(bg="black")

    # Tkinter'de ağları gösterecek bir frame
    network_list_frame = tk.Frame(root, bg="black")
    network_list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Tarama durdurulduğunda görülecek mesaj için bir etiket
    stop_message_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red", bg="black")
    stop_message_label.pack()

    # Pencereyi kapatma olayını bağla
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Tuş basıldığında 'w' tuşuna basıldığında taramayı durdurmak için
    root.bind("<KeyPress>", on_key_press)

    # Kartı okuma ve monitor modunu başlatma
    read_card2()
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")

    try:
        # Taramayı başlat
        sniff_thread = Thread(target=start_sniffing, args=(interface,))
        sniff_thread.start()

        # Tkinter penceresini sürekli açık tut
        root.mainloop()

    except KeyboardInterrupt:
        print("\n[!] Çıkış yapılıyor...")
    # Monitor modunu kapatmayı kaldırdık
