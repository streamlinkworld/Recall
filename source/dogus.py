import requests
import re

# Basis-URLs für NTV, STAR und EuroStar
ntv_base_url = "https://mn-nl.mncdn.com/dogusdyg_ntv/"
star_base_url = "https://mn-nl.mncdn.com/dogusdyg_star/"
eurostar_base_url = "https://mn-nl.mncdn.com/dogusdyg_eurostar/"
initial_url = "https://dygvideo.dygdigital.com/live/hls/kralpop?m3u8"

def fetch_and_save_m3u8(base_url, modified_url, output_file):
    try:
        # Abrufen des Inhalts von der modifizierten URL
        content_response = requests.get(modified_url)
        content_response.raise_for_status()
        content = content_response.text

        # Verarbeiten und Speichern des Inhalts
        lines = content.split("\n")
        modified_content = ""

        for line in lines:
            if line.startswith("live_"):
                # Basis-URL zu den Live-Stream-Zeilen hinzufügen
                full_url = base_url + line
                modified_content += full_url + "\n"
            else:
                modified_content += line + "\n"
        
        # Speichern des modifizierten Inhalts in der angegebenen Ausgabedatei
        with open(output_file, "w") as f:
            f.write(modified_content)
        print(f"Inhalt gespeichert in {output_file}")

    except requests.RequestException as e:
        print(f"Beim Abrufen von {output_file} ist ein Fehler aufgetreten: {e}")

def fetch_initial_url():
    try:
        # Abrufen der anfänglichen URL
        response = requests.get(initial_url)
        response.raise_for_status()
        return response.url
    except requests.RequestException as e:
        print(f"Beim Abrufen der anfänglichen URL ist ein Fehler aufgetreten: {e}")
        return None

def fetch_and_save_eurostar(base_url, output_file):
    eurostar_url = "https://www.eurostartv.com.tr/canli-izle"
    
    try:
        # Abrufen des Inhalts der EuroStar-Website
        response = requests.get(eurostar_url)
        response.raise_for_status()
        site_content = response.text

        # Extrahieren der Live-URL aus dem Website-Inhalt
        match = re.search(r'liveUrl = \'(.*?)\'', site_content)
        if match:
            live_url = match.group(1)
            
            # Abrufen des Live-Stream-Inhalts
            content_response = requests.get(live_url)
            content_response.raise_for_status()
            content = content_response.text

            # Verarbeiten und Speichern des Inhalts
            lines = content.split("\n")
            modified_content = ""

            for line in lines:
                if line.startswith("live_"):
                    full_url = base_url + line
                    modified_content += full_url + "\n"
                else:
                    modified_content += line + "\n"
            
            # Speichern des modifizierten Inhalts in der angegebenen Ausgabedatei
            with open(output_file, "w") as f:
                f.write(modified_content)
            print(f"Inhalt gespeichert in {output_file}")

        else:
            print("Live-URL im Inhalt nicht gefunden.")
    
    except requests.RequestException as e:
        print(f"Beim Abrufen von {output_file} ist ein Fehler aufgetreten: {e}")

def main():
    final_url = fetch_initial_url()
    if final_url:
        # Modifizieren der URL, um auf die NTV-Variante zu verweisen
        ntv_modified_url = final_url.replace("dogusdyg_kralpoptv/dogusdyg_kralpoptv.smil/playlist", "dogusdyg_ntv/live")
        # Modifizieren der URL, um auf die STAR-Variante zu verweisen
        star_modified_url = final_url.replace("dogusdyg_kralpoptv/dogusdyg_kralpoptv.smil/playlist", "dogusdyg_star/live")
        
        # Abrufen und Speichern der NTV m3u8-Datei
        fetch_and_save_m3u8(ntv_base_url, ntv_modified_url, "result/List/NTV.m3u8")
        
        # Abrufen und Speichern der STAR m3u8-Datei
        fetch_and_save_m3u8(star_base_url, star_modified_url, "result/List/STAR.m3u8")
    
    # Abrufen und Speichern der EuroStar m3u8-Datei
    fetch_and_save_eurostar(eurostar_base_url, "result/List/EuroStar.m3u8")

if __name__ == "__main__":
    main()
