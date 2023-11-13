import argparse
import random
import requests
import json
import re

from playsound import playsound
from termcolor import colored

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def query_wiktionary_summary(word):
    url = f"https://en.wiktionary.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "extracts",
        "explaintext": True,
    }

    response = requests.get(url, params=params)
    data = response.json()

    print(json.dumps(data, indent=3))

    return data

def query_wiktionary(word):
    url = f"https://en.wiktionary.org/w/api.php"
    params = {
        "action": "parse",
        "page": word,
        "format": "json",
        "prop": "text",
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    try:
        content = data['parse']['text']['*']

        ipa_match = re.search(r'<span class="IPA">(.*?)</span>', content)
        audio_match = re.search(r'src="(\/\/upload.wikimedia.org\/wikipedia\/commons\/.*?\.ogg)"', content)

        ipa = ipa_match.group(1) if ipa_match else None
        audio = f"https:{audio_match.group(1)}" if audio_match else None
    except KeyError:
        ipa, audio = None, None

    return ipa, audio

def download_audio(url, filename):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return filename

def rainbow_colours(word):
    colours = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    rainbow = ''

    for letter in word:
        rainbow += colored(letter, random.choice(colours))

    return rainbow

def main():
    parser = argparse.ArgumentParser(prog="Verbose", description="Retrieve the pronunciation and audio file for a given word.")
    parser.add_argument("word", help="A word to search on Wiktionary")
    args = parser.parse_args()
    
    print("Welcome to Verbose!")

    ipa, audio = query_wiktionary(args.word)

    rainbow = rainbow_colours(ipa) if ipa is not None else "None"

    print(f"{args.word}: {rainbow}, {audio}")

    if audio is not None:
        download_audio(audio, f"src/audio/{args.word}.ogg")
        playsound(f"src/audio/{args.word}.ogg")

if __name__ == "__main__":
    main()
