from random import randint
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1, 1000)

        self.name = self.get_name()
        self.img = self.get_img()


        self.hp = randint(80, 120)
        self.power = randint(10, 20)

        Pokemon.pokemons[pokemon_trainer] = self

    def heal(self):
        self.hp += 20

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

        return None

    def info(self):
        return (
            f"Pokemon name: {self.name}\n"
            f"HP: {self.hp}\n"
            f"Power: {self.power}"
        )

    def show_img(self):
        return self.img

    # attack method
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

class Wizard(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)


        self.hp += 30

    def info(self):
        parent_info = super().info()
        return "You have a Wizard Pokémon\n" + parent_info

    def attack(self, enemy):
        return super().attack(enemy)

class Fighter(Pokemon):

    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)


        self.power += 10

    def info(self):
        parent_info = super().info()
        return "You have a Fighter Pokémon\n" + parent_info

    def attack(self, enemy):
        super_strength = randint(5, 15)
        self.power += super_strength
        result = super().attack(enemy)
        self.power -= super_strength
        return result + f"\nThe fighter used a super attack with strength: {super_strength}"

if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(wizard.info())
    print()
    print(fighter.info())
    print()
    print(fighter.attack(wizard))