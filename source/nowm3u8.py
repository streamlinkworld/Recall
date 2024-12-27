import requests

def download_and_save_m3u8(input_url, output_file):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.nowtv.com.tr/",
        "Cookie": "deine_cookies_hier",  # Füge die notwendigen Cookies hinzu
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "DNT": "1"  # Do Not Track-Header hinzufügen
    }

    try:
        # Lade den Inhalt der Playlist-URL herunter
        playlist_response = requests.get(input_url, headers=headers)
        playlist_response.raise_for_status()
        print(f"DEBUG: Erfolgreicher Zugriff auf {input_url}")

        # Extrahiere die M3U8-URLs aus der Playlist-Datei
        m3u8_urls = [line.strip() for line in playlist_response.text.split('\n') if line.startswith("http")]

        # Lade jede M3U8-URL herunter und speichere den Inhalt
        for m3u8_url in m3u8_urls:
            response = requests.get(m3u8_url, headers=headers)
            response.raise_for_status()
            print(f"DEBUG: Erfolgreicher Zugriff auf {m3u8_url}")

            with open(output_file, 'w', encoding='utf-8') as file:
                file.writelines(f"{line.strip()}\n" for line in response.text.split('\n'))
            print(f"DEBUG: M3U8-Datei wurde in {output_file} gespeichert.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Fehler beim Herunterladen der Datei: {e}")

if __name__ == "__main__":
    input_url = "https://raw.githubusercontent.com/streamlinkworld/Recall/refs/heads/main/result/List/playlist.m3u8"
    output_file = "result/List/NOW.m3u8"
    download_and_save_m3u8(input_url, output_file)
