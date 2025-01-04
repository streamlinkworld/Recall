import json

# JSON-Datei lesen
with open('source/json/test.json', 'r') as f:
    data = json.load(f)

# M3U8-Playlist generieren
m3u8_playlist = data['playlist']

# M3U8-Datei speichern
with open('source/json/test.m3u8', 'w') as f:
    f.write(m3u8_playlist)

print("M3U8-Playlist erfolgreich generiert!")
