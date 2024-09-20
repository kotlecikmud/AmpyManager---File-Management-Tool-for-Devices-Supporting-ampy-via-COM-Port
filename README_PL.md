### **AmpyManager**

#### **Informacje o programie**

- **Nazwa skryptu:** `AM_main.py`
- **Autor:** *Filip Pawłowski*
- **Kontakt:** [filippawlowski2012@gmail.com](mailto:filippawlowski2012@gmail.com)
- **Wersja:** `01.01.21.00`

---

#### **Opis**

Skrypt `ampy_manager.py` to narzędzie do zarządzania plikami na urządzeniach kompatybilnych z **ampy**, takich jak *
*Raspberry Pi Pico** z wgranym firmwarem **MicroPython**. Umożliwia wykonywanie następujących operacji:

- **Wyświetlanie zawartości plików** (nie dekoduje danych binarnych – wyświetla surowe dane)
- **Przesyłanie i pobieranie plików**
- **Usuwanie plików**
- I inne funkcje zarządzania plikami na urządzeniu.

*Uwaga*: Skrypt był testowany wyłącznie z Raspberry Pi Pico.

---

#### **Instrukcja użycia**

Skrypt uruchamia się z linii poleceń za pomocą komendy:

    python ampy_manager.py

Po uruchomieniu, na ekranie pojawi się menu z poniższymi opcjami do wyboru:

- **Wyświetlanie zawartości pliku:** Wyświetla zawartość wybranego pliku na urządzeniu (surowe dane, bez dekodowania).
- **Przesłanie pojedynczego pliku:** Przesyła jeden plik z lokalnego komputera na urządzenie.
- **Przesłanie wielu plików:** Przesyła wiele plików z lokalnego katalogu na urządzenie.
- **Pobranie pojedynczego pliku:** Pobiera wybrany plik z urządzenia na komputer lokalny.
- **Pobranie wielu plików:** Pobiera wszystkie pliki z wybranego katalogu na urządzeniu do lokalnego katalogu.
- **Usunięcie pojedynczego pliku:** Usuwa wybrany plik z urządzenia.
- **Usunięcie plików wg rozszerzenia:** Usuwa wszystkie pliki z określonym rozszerzeniem (np. .txt, .py) z urządzenia.
- **Usuń wszystko:** Usuwa wszystkie pliki z urządzenia.
- **Przeskanuj porty COM:** Skanuje dostępne porty COM, umożliwiając wybór innego portu do połączenia z urządzeniem.
- **Wyjście:** Zamyka skrypt.
- **Pomoc:** Wyświetla szczegółową dokumentację i pomoc dotyczącą używania skryptu.

**Kontakt**  
W razie jakichkolwiek pytań lub problemów, prosimy o kontakt:

- **Autor:** Filip Pawłowski
- **Email:** filippawlowski2012@gmail.com

---
