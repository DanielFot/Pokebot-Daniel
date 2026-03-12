import telebot
from config import token
from logic import Pokemon, Wizard, Fighter
from random import randint

bot = telebot.TeleBot(token)
bot.infinity_polling(none_stop=True)

@bot.message_handler(commands=['go'])
def go(message):

    if message.from_user.username not in Pokemon.pokemons.keys():

        chance = randint(1, 10)

        if chance == 1:
            pokemon = Wizard(message.from_user.username)
        elif chance == 2:
            pokemon = Fighter(message.from_user.username)
        else:
            pokemon = Pokemon(message.from_user.username)

        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())

    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['battle'])
def battle(message):

    users = message.text.split()

    if len(users) != 2:
        bot.send_message(message.chat.id, "Use: /battle @username")
        return

    attacker = message.from_user.username
    defender = users[1].replace("@", "")

    if attacker not in Pokemon.pokemons or defender not in Pokemon.pokemons:
        bot.send_message(message.chat.id, "Both trainers must have Pokémon!")
        return

    pokemon1 = Pokemon.pokemons[attacker]
    pokemon2 = Pokemon.pokemons[defender]

    result = pokemon1.attack(pokemon2)

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['info'])
def info(message):
    username = message.from_user.username

    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")


@bot.message_handler(commands=['attack'])
def attack(message):

    if message.reply_to_message:

        attacker = message.from_user.username
        defender = message.reply_to_message.from_user.username

        if attacker not in Pokemon.pokemons:
            bot.send_message(message.chat.id, "You don't have a Pokémon. Use /go")
            return

        if defender not in Pokemon.pokemons:
            bot.send_message(message.chat.id, "The opponent has no Pokémon.")
            return

        pokemon1 = Pokemon.pokemons[attacker]
        pokemon2 = Pokemon.pokemons[defender]

        result = pokemon1.attack(pokemon2)

        bot.send_message(message.chat.id, result)

    else:
        bot.send_message(
            message.chat.id,
            "Reply to a user's message with /attack to start a battle."
        )


@bot.message_handler(commands=['heal'])
def heal_pokemon(message):

    username = message.from_user.username

    if username not in Pokemon.pokemons:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")
        return

    pokemon = Pokemon.pokemons[username]

    pokemon.heal()

    bot.send_message(
        message.chat.id,
        f"{pokemon.name} restored health!\nHP: {pokemon.hp}"
    )

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    username = message.from_user.username

    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        pokemon.feed()

        bot.send_message(
            message.chat.id,
            f"You fed {pokemon.name} 🍖\nLevel: {pokemon.level}\nEXP: {pokemon.exp}"
        )
    else:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")

@bot.message_handler(commands=['achievements'])
def achievements(message):
    username = message.from_user.username

    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pokemon.show_achievements())
    else:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")

bot.infinity_polling(none_stop=True)
