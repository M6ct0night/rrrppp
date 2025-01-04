import os
import subprocess

card_value=""
print("1 monitor işlemi başlatıldı")
def read_card():
    print("2 kart okutuluyot")
    try:
        with open("card.txt", "r") as file:
            card_value = file.read().strip()  # Dosyadan değeri oku ve boşlukları temizle
        return card_value
    except FileNotFoundError:
        print("değer bulunamadı")# Eğer dosya bulunamazsa, bir hata yerine bir varsayılan değer döndür
        return None


def chkill ():
    print("3 kill atılıyor")
    try:
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Süreçleri sonlandırırken hata: {e}")

def monitor():
    print("4 monitor moda alınıyor")
    # Airmon-ng ile arayüzü monitör moduna alma
    global card_value
    try:
        subprocess.run(["sudo", "airmon-ng", "start", card_value], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: 'airmon-ng' komutunu çalıştırırken bir sorun oluştu: {e}")
        exit(1)

    new_interface_name = ""

    # iwconfig komutunu çalıştırarak arayüzü kontrol etme
    result = subprocess.run(["iwconfig", card_value], capture_output=True, text=True)

    # Arayüz monitör modunda mı kontrol et
    if "Mode:Monitor" in result.stdout:
        print(f"{card_value} şu anda monitör modunda.")

        # Monitör modunda olan kartın adını kontrol et
        new_interface = [line for line in result.stdout.splitlines() if "Monitor" in line]
        if new_interface:
            new_interface_name = new_interface[0].split()[0]
            print(f"Yeni ağ adaptörü adı: {new_interface_name}")
    else:
        print(f"{card_value} monitör modunda değil.")

    with open("card2.txt", "w") as file:
        file.write(new_interface_name)

    os.system("python wifiscan.py")