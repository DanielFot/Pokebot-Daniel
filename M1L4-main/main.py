import telebot
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username

    if username not in Pokemon.pokemons:
        pokemon = Pokemon(username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "You already have a Pokémon!")


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
    username = message.from_user.username

    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        pokemon.take_damage(10)
        bot.send_message(message.chat.id, f"{pokemon.name} took damage! HP: {pokemon.hp}")
    else:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")


@bot.message_handler(commands=['heal'])
def heal(message):
    username = message.from_user.username

    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        pokemon.heal(10)
        bot.send_message(message.chat.id, f"{pokemon.name} healed! HP: {pokemon.hp}")
    else:
        bot.send_message(message.chat.id, "Create a Pokémon first using /go")


bot.infinity_polling(none_stop=True)
