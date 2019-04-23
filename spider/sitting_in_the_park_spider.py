from bs4 import BeautifulSoup
import sys
import requests
import json

LINK = 'http://www.sittinginthepark.com/shows.htm'
SONG_TITLES_TO_IGNORE = '?'

def main(destination_file):
    f = requests.get(LINK)
    soup = BeautifulSoup(f.text, 'html.parser')

    for br in soup.find_all("br"):
        br.replace_with("\n")

    [s.extract() for s in soup('a')]
    text = soup.text
    text = text.split('\n')

    songs = []

    for item in text:
        if '-' in item:
            item = item.split('-')
            if len(item) == 3:
                song = dict()
                song['artist'] = item[0].strip()
                song['title'] = item[1].strip()
                song['album'] = None
                song['label'] = item[2].strip()

                if song['title'] not in SONG_TITLES_TO_IGNORE:
                    songs.append(song)

    with open(destination_file, 'w') as outfile:
        json.dump(songs, outfile)


if __name__ == "__main__":
    destination_file = sys.argv[1]
    main(destination_file)
