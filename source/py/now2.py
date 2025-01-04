import json

# JSON-Datei lesen
with open('source/json/now.json', 'r') as f:
    data = json.load(f)

# M3U8-Playlist generieren
m3u8_playlist = "#EXTM3U\n"
m3u8_playlist += "#EXT-X-VERSION:{}\n".format(data['playlist']['#EXT-X-VERSION'])
m3u8_playlist += "#EXT-X-INDEPENDENT-SEGMENTS\n"

for stream in data['variantStreams']:
    m3u8_playlist += "#EXT-X-STREAM-INF:PROGRAM-ID=2850,AVERAGE-BANDWIDTH={},BANDWIDTH={},RESOLUTION={}\n".format(
        stream['#EXT-X-STREAM-INF']['AVERAGE-BANDWIDTH'],
        stream['#EXT-X-STREAM-INF']['BANDWIDTH'],
        stream['#EXT-X-STREAM-INF']['RESOLUTION']
    )
    m3u8_playlist += "{}\n".format(stream['URI'])

# M3U8-Datei speichern
with open('playlist.m3u8', 'w') as f:
    f.write(m3u8_playlist)

print("M3U8-Playlist erfolgreich generiert!")
