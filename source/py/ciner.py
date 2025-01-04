import requests
import re
import json
import streamlink
import os
from datetime import datetime

# Basis-URLs für ShowTV, ShowTürk, ShowMax und Habertürk
showtv_url = "https://www.showtv.com.tr/canli-yayin/showtv"
showturk_url = "https://www.showturk.com.tr/canli-yayin/showturk"
showmax_url = "http://www.showmax.com.tr/canliyayin"
haberturk_url = "https://www.haberturk.com/canliyayin"

def fetch_and_save_showtv():
    try:
        response = requests.get(showtv_url)
        response.raise_for_status()
        content = response.text

        # Suchen nach der m3u8-URL im Quellcode der Seite
        match = re.search(r'ht_stream_m3u8":"(https?://[^\s]+\.m3u8)', content)
        if match:
            m3u8_url = match.group(1)
            m3u8_base_url = m3u8_url.rsplit("/", 1)[0]
            m3u8_content = f"""
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=2200000,AVERAGE-BANDWIDTH=2000000,RESOLUTION=1920x1080
{m3u8_base_url}/showtv_1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1050000,AVERAGE-BANDWIDTH=950000,RESOLUTION=1280x720
{m3u8_base_url}/showtv_720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=800000,AVERAGE-BANDWIDTH=700000,RESOLUTION=854x480
{m3u8_base_url}/showtv_480p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=550000,AVERAGE-BANDWIDTH=500000,RESOLUTION=640x360
{m3u8_base_url}/showtv_360p.m3u8
            """

            with open("result/List/SHOWTV.m3u8", "w") as f:
                f.write(m3u8_content.strip())
            print("m3u8-Inhalt für ShowTV erfolgreich erstellt.")
        else:
            print("m3u8-URL im Seiteninhalt nicht gefunden.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ShowTV: {e}")

def fetch_and_save_showturk():
    url = "https://www.showturk.com.tr/canli-yayin/showturk"

    def fetch_website_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Fehler beim Abrufen des Website-Inhalts.")

    def extract_stream_url(content):
        match = re.search(r'ht_stream_m3u8":"(.*?)"', content)
        if match:
            json_data = match.group(1).replace("\\/", "/")
            try:
                ht_data = json.loads(f'{{"ht_stream_m3u8":"{json_data}"}}')
                return ht_data.get('ht_stream_m3u8')
            except json.JSONDecodeError as e:
                raise Exception(f"JSON-Dekodierungsfehler: {e}")
        else:
            raise Exception("Live URL-Muster im Inhalt nicht gefunden.")

    def create_m3u8_content(stream_url):
        stream_url_1080p = stream_url.replace("playlist.m3u8", "showturk_1080p.m3u8")
        stream_url_720p = stream_url.replace("playlist.m3u8", "showturk_720p.m3u8")
        stream_url_576p = stream_url.replace("playlist.m3u8", "showturk_576p.m3u8")
        stream_url_360p = stream_url.replace("playlist.m3u8", "showturk_360p.m3u8")
        
        m3u8_content = [
            "#EXTM3U",
            "#EXT-X-VERSION:3",
            "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,RESOLUTION=1920x1080",
            stream_url_1080p,
            "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1500000,RESOLUTION=1280x720",
            stream_url_720p,
            "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1200000,RESOLUTION=1024x576",
            stream_url_576p,
            "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=600000,RESOLUTION=640x360",
            stream_url_360p
        ]
        return "\n".join(m3u8_content)

    try:
        site_content = fetch_website_content(url)
        stream_url = extract_stream_url(site_content)
        
        m3u8_content = create_m3u8_content(stream_url)

        with open("result/List/SHWTR.m3u8", "w") as f:
            f.write(m3u8_content)
        
        print("m3u8-Inhalt für ShowTürk erfolgreich erstellt.")
    except Exception as e:
        print(e)

def fetch_and_save_haberturk():
    # Pfad zur Ausgabe-Datei
    output_file_path = "result/List/HT.m3u8"

    # Löschen der alten Datei, falls vorhanden
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        print(f"Alte Datei gelöscht: {output_file_path}")

    # Initialisierung der Streamlink-Sitzung
    session = streamlink.Streamlink()
    session.set_option("http-timeout", 60)  # Timeout auf 60 Sekunden erhöhen

    # Abrufen der Streams von Habertürk
    streams = session.streams(haberturk_url)
    erstrm = streams["best"].multivariant.uri

    # Erstellen der URLs für verschiedene Auflösungen und Bandbreiten
    urls = {
        "1080p": erstrm,  # Beste Qualität
        "720p": erstrm.replace("1080", "720"),
        "480p": erstrm.replace("1080", "480")
    }

    # Erstellen des M3U8-Inhalts ohne Zeitstempel
    output = f"""#EXTM3U
#EXT-X-VERSION:3
"""

    output += f"""#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,RESOLUTION=1920x1080
{urls["1080p"]}
"""
    output += f"""#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1500000,RESOLUTION=1280x720
{urls["720p"]}
"""
    output += f"""#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=900000,RESOLUTION=854x480
{urls["480p"]}
"""

    # Speichern des M3U8-Inhalts in einer Datei
    with open(output_file_path, "w") as f:
        f.write(output)

    print(f"{output_file_path} Datei erfolgreich erstellt.")
    print("Inhalt:")
    print(output)  # Inhalt für Debugging ausgeben

def fetch_and_save_showmax():
    base_url = "https://ciner-live.ercdn.net/showmax/"
    url = "http://www.showmax.com.tr/canliyayin"
    response = requests.get(url)

    if response.status_code == 200:
        site_content = response.text
        match = re.search(r'ht_stream_m3u8":"(.*?)"', site_content)
        
        if match:
            json_data = match.group(1)
            json_data_valid = json_data.replace("\\/", "/")  # Ersetze escapte Schrägstriche
            
            try:
                ht_data = json.loads('{"ht_stream_m3u8":"' + json_data_valid + '"}')
                ht_stream_m3u8 = ht_data.get('ht_stream_m3u8')
                
                if ht_stream_m3u8:
                    content_response = requests.get(ht_stream_m3u8)
                    
                    if content_response.status_code == 200:
                        content = content_response.text
                        lines = content.split("\n")
                        modified_content = ""
                        
                        for line in lines:
                            if line.startswith("showmax"):
                                full_url = base_url + line
                                modified_content += full_url + "\n"
                            else:
                                modified_content += line + "\n"
                        
                        with open("result/List/SHOWMAX.m3u8", "w") as f:
                            f.write(modified_content)
                        
                        print("m3u8-Inhalt für ShowMax erfolgreich erstellt.")
                    else:
                        print("Fehler beim Abrufen des Inhalts von der Live-URL.")
                else:
                    print("Live-URL im Inhalt nicht gefunden.")
            except json.JSONDecodeError as e:
                print(f"JSON-Dekodierungsfehler: {e}")
        else:
            print("Live-URL-Muster im Inhalt nicht gefunden.")
    else:
        print("Fehler: Statuscode ist nicht 200.")

def main():
    fetch_and_save_showtv()
    fetch_and_save_showturk()
    fetch_and_save_habert
