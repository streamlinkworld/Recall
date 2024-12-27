import requests

def download_and_save_m3u8(m3u8_url, output_file, base_url):
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
        response = requests.get(m3u8_url, headers=headers)
        response.raise_for_status()
        print(f"DEBUG: Erfolgreicher Zugriff auf {m3u8_url}")

        lines = response.text.split('\n')
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.startswith("#") or line.strip() == "":
                    file.write(line + "\n")
                else:
                    file.write(base_url + line + "\n")
        print(f"DEBUG: M3U8-Datei wurde in {output_file} gespeichert.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Fehler beim Herunterladen der Datei: {e}")

if __name__ == "__main__":
    m3u8_url = "https://nowtv-live-ad.ercdn.net/nowtv/playlist.m3u8?st=fNnuSeiTM-71rJB5MFfSFg&e=1735317265"
    output_file = "result/List/NOW.m3u8"
    base_url = "https://nowtv.daioncdn.net/nowtv/"
    download_and_save_m3u8(m3u8_url, output_file, base_url)
