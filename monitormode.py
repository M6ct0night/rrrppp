import os
import subprocess


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


def chkill():
    """Wi-Fi ile ilgili süreçleri sonlandırır."""
    print("Wi-Fi süreçleri sonlandırılıyor...")
    try:
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: Süreçleri sonlandırırken bir sorun oluştu: {e}")


def monitor(card_value):
    """Belirtilen kartı monitör moduna alır."""
    if not card_value:
        print("Hata: Geçerli bir kart adı sağlanmadı.")
        return

    print(f"{card_value} monitör moduna alınıyor...")
    try:
        # Monitör moduna geçiş
        subprocess.run(["sudo", "airmon-ng", "start", card_value], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: 'airmon-ng' komutunu çalıştırırken bir sorun oluştu: {e}")
        return

    # Yeni arayüz adını kontrol et
    new_interface_name = ""
    try:
        result = subprocess.run(["iwconfig", card_value], capture_output=True, text=True)
        if "Mode:Monitor" in result.stdout:
            print(f"{card_value} şu anda monitör modunda.")
            new_interface_name = card_value  # Yeni ad genelde aynı kalır
        else:
            print(f"Hata: {card_value} monitör modunda değil.")
    except Exception as e:
        print(f"Hata: iwconfig komutu sırasında bir sorun oluştu: {e}")
        return

    # Yeni adı kaydet
    if new_interface_name:
        try:
            with open("card2.txt", "w") as file:
                file.write(new_interface_name)
            print(f"Yeni ağ adaptörü adı: {new_interface_name}")
        except Exception as e:
            print(f"Hata: Yeni adı kaydederken bir sorun oluştu: {e}")
    else:
        print("Hata: Yeni ağ adaptörü adı alınamadı.")


if __name__ == "__main__":
    card_value = read_card()  # Kart adını oku
    if card_value:
        chkill()  # Süreçleri sonlandır
        monitor(card_value)  # Monitör moduna al
