import requests
import random
from bs4 import BeautifulSoup

class OfficeQuotes(object):
    base_url = 'http://www.officequotes.net'

    def __init__(self, season):
        self.season = season
        self.quotes = {}
    
    def quotes_from_episode(self, episode):
        if episode in self.quotes:
            return self.quotes[episode]

        soup = BeautifulSoup(self.get_html(episode), 'html.parser')
        quote_divs = soup.find_all('div', class_='quote')

        lines = {}
        for block in quote_divs:
            # https://stackoverflow.com/a/9942822/8109239
            text = block.text.encode('utf-8').strip()
            for line in text.split("\n"):
                if ':' not in line:
                    continue

                character, words = line.split(':')[0].lower(), line.split(':')[1]

                # fix typos
                if character == 'michel':
                    character = "michael"

                # encoding corrections
                words = words.replace('\xe2\x80\x94', '-')
                words = words.replace('\xe2\x80\x99', "'")
                words = words.replace('\xe2\x80\x98', "'")
                words = words.replace("\'", "'")
                words = words.strip()

                if character not in lines:
                    lines[character] = []

                # TODO: split lines by individual sentences
                if len(words) > 0: lines[character].append(words)

        self.quotes[episode] = lines
        return lines

    def quotes_from_character(self, episode, character):
        quotes = self.quotes_from_episode(episode)
        return quotes[character]

    def random_quote(self, episode=None):
        if episode is None:
            episode = 1 if len(self.quotes) == 0 else random.choice(self.quotes.keys())
        episode_quotes = self.quotes_from_episode(episode)
        character = random.choice(episode_quotes.keys())
        line = random.choice(episode_quotes[character])
        return character, line

    def get_html(self, episode):
        headers = {
            'Accept-Charset' : 'utf-8'
        }
        url = '{base_url}/no{season}-{episode}.php'.format(
            base_url=OfficeQuotes.base_url,
            season=self.season,
            episode=('%02d' % episode)
        )
        res = requests.get(url, headers=headers)

        return res.text if res.status_code == 200 else ""

    def __repr__(self):
        return 'Quotes from "The Office", Season {}'.format(self.season)