from scapy.all import *
from threading import Thread
import os

card_value=""
def read_card2():
    try:
        with open("card2.txt", "r") as file:
            global card_value
            card_value = file.read().strip()  # Dosyadan değeri oku ve boşlukları temizle
        return card_value
    except FileNotFoundError:
        print("değer bulunamadı")# Eğer dosya bulunamazsa, bir hata yerine bir varsayılan değer döndür
        return None

interface=card_value

# Bulunan ağları tutmak için bir set
found_networks = set()

def packet_handler(packet):
    """Wi-Fi paketlerini işler."""
    if packet.haslayer(Dot11Beacon):
        ssid = packet[Dot11Elt].info.decode()
        bssid = packet[Dot11].addr2
        if (ssid, bssid) not in found_networks:
            found_networks.add((ssid, bssid))
            print(f"SSID: {ssid}, BSSID: {bssid}")

def start_sniffing(interface):
    """Belirtilen arayüzde paketleri dinler."""
    print(f"[+] Wi-Fi taraması başlatılıyor ({interface})...")
    sniff(iface=interface, prn=packet_handler, store=False)

if __name__ == "__main__":

    read_card2()
    global interface
    # Monitor modunu aktif et
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")

    try:
        # Taramayı başlat
        sniff_thread = Thread(target=start_sniffing, args=(interface,))
        sniff_thread.start()
        sniff_thread.join()
    except KeyboardInterrupt:
        print("\n[!] Çıkış yapılıyor...")
    finally:
        # Arayüzü eski haline getir
        os.system(f"sudo ip link set {interface} down")
        os.system(f"sudo iw dev {interface} set type managed")
        os.system(f"sudo ip link set {interface} up")
