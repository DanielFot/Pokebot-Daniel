from random import randint
import requests


class Pokemon:
    pokemons = {}


    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)

        data = self.get_data()

        self.name = data["name"]
        self.img = data["img"]
        self.type = data["type"]
        self.height = data["height"]
        self.weight = data["weight"]
        self.hp = data["hp"]
        self.attack = data["attack"]
        self.defense = data["defense"]

        Pokemon.pokemons[pokemon_trainer] = self


    def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            pokemon_data = {
                "name": data["name"],
                "img": data["sprites"]["other"]["dream_world"]["front_default"],
                "type": data["types"][0]["type"]["name"],
                "height": data["height"],
                "weight": data["weight"],
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"]
            }

            return pokemon_data

        return {
            "name": "pikachu",
            "img": "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png",
            "type": "electric",
            "height": 4,
            "weight": 60,
            "hp": 100,
            "attack": 50,
            "defense": 40
        }


    def info(self):
        return (
            f"Your Pokémon: {self.name}\n"
            f"Type: {self.type}\n"
            f"Height: {self.height}\n"
            f"Weight: {self.weight}\n"
            f"HP: {self.hp}\n"
            f"Attack: {self.attack}\n"
            f"Defense: {self.defense}"
        )


    def show_img(self):
        return self.img

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    # heal pokemon
    def heal(self, amount):
        self.hp += amount


