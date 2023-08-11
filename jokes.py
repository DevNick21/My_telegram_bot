import requests
import random

NORMAL_JOKE_API = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist&type=single"
JOKE_API = "https://official-joke-api.appspot.com/jokes/random"


class Jokes:
    def __init__(self):
        pass

    def normal_joke(self):
        normals = [self.generate_normal_jokes, self.generate_joke]
        choice = random.choice(normals)
        return choice

    def generate_normal_jokes(self):
        res = requests.get(NORMAL_JOKE_API)
        data = res.json()
        joke = data["joke"]
        return joke

    def generate_joke(self):
        res = requests.get(JOKE_API)
        data = res.json()
        joke = f"{data['setup']}\n\n\n{data['punchline']}"
        return joke
