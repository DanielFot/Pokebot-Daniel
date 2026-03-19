from random import randint
import requests
from datetime import datetime, timedelta  # 1. REQUIRED IMPORT


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1, 1000)

        self.name = self.get_name()
        self.img = self.get_img()

        self.hp = randint(80, 120)
        self.power = randint(10, 20)

        #  2. last feeding time
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self

    def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["name"]

        return "pikachu"

    def get_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()['sprites']['other']['dream_world']['front_default']

        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"

    def info(self):
        return (
            f"Pokemon name: {self.name}\n"
            f"HP: {self.hp}\n"
            f"Power: {self.power}"
        )

    def show_img(self):
        return self.img

    #  3. FIXED FEED METHOD

    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)

        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_time = self.last_feed_time + delta_time
            return f"Следующее время кормления покемона: {next_time}"

    def attack(self, enemy):

        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "The Wizard Pokémon used a magical shield!"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"@{self.pokemon_trainer} battles @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            self.power += 2
            self.hp += 5
            return f"@{self.pokemon_trainer} defeats @{enemy.pokemon_trainer}!"


#  4. WIZARD (MORE HEAL)
class Wizard(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp += 30

        self.feed_interval = 10
        self.feed_bonus = 20

    def info(self):
        return "You have a Wizard Pokémon\n" + super().info()

    def feed(self):
        now = datetime.now()

        if now - self.last_feed_time >= timedelta(seconds=self.feed_interval):
            self.hp += self.feed_bonus
            self.last_feed_time = now
            return f"{self.name} (Wizard) was fed! HP: {self.hp}"
        else:
            remaining = self.feed_interval - int((now - self.last_feed_time).total_seconds())
            return f"Wait {remaining} seconds to feed again."


#  5. FIGHTER (SHORTER COOLDOWN)
class Fighter(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += 10

        self.feed_interval = 5
        self.feed_bonus = 10

    def info(self):
        return "You have a Fighter Pokémon\n" + super().info()

    def feed(self):
        now = datetime.now()

        #  shorter cooldown (5 seconds)
        if now - self.last_feed_time >= timedelta(seconds=5):
            self.hp += 10
            self.last_feed_time = now
            return f"{self.name} (Fighter) was fed! HP: {self.hp}"
        else:
            remaining = 5 - int((now - self.last_feed_time).total_seconds())
            return f"Wait {remaining} seconds to feed again."