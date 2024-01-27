import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json

TOKEN="TOKEN"
bot=telebot.TeleBot(TOKEN)

where_you={}

photos={"location1":"location1.jpg",
        "calm-grove":"calm_grove.jpg",
        "church":"church.jpg",
        "green_ball":"green_ball.jpg",
        "red_ball":"red_ball.jpg",
        "cave":"cave.jpg",
        "enter_cave":"enter_cave.jpg",
        "go_ahead":"win.jpg",
        "forest":"forest.jpg",
        "river":"bridge.jpg",
        "bridge":"win.jpg",
        "swim":"swim.jpg",
        "top_tree":"top_tree.jpg",
        "mountains":"mountains.jpg",
        "devils":"devils.jpg",
        "watch":"win.jpg",
        "sweet":"lose.jpg",
        "swamp":"swamp.jpg",
        "light":"win.jpg",
        "yourself":"lose.jpg"}

with open("DESCRIPTION_BOT_QUEST.json","r",encoding='utf8') as f:
    location=json.load(f)

def send_photo(message):
    try:
        user_id=str(message.from_user.id)
        photo_path = photos[where_you[user_id]]
        bot.send_photo(message.chat.id, open(photo_path, "rb"))
    except:
        bot.send_message(message.chat.id,"Извините, картинка не найдена.")

def safe_user_data():
    with open("user_data.json","w") as f:
        json.dump(where_you,f)


def load_user_data(user_id):
    global where_you
    try:
        with open("user_data.json","r") as f:
            where_you=json.load(f)
    except:
        where_you[user_id]="location1"
    return where_you

@bot.message_handler(commands=["start"])
def start_dialogue(message):
    start_mes="Вам предстоит пройти текстовый квест.Вам будут предложены варианты действий,а в зависимости от выбора, сюжет будет развиваться по-разному."
    bot.send_message(message.chat.id, start_mes)
    bot.send_message(message.chat.id,"Если хотите начать, напишите /begin")

@bot.message_handler(commands=["again"])
def again(message):
    user_id=str(message.from_user.id)
    where_you[user_id]="location1"
    safe_user_data()
    say_locations(message)

@bot.message_handler(commands=["help"])
def help_user(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                                      "/start - начать диалог\n"
                                      "/begin - начать квест\n"
                                      "/help - список команд\n"
                                      "/again - начать сначала")
@bot.message_handler(commands=["begin"])
def say_locations(message):
    user_id=str(message.from_user.id)
    global where_you
    where_you=load_user_data(user_id)
    if user_id not in where_you:
        where_you[user_id] = "location1"
        safe_user_data()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if location["locations"][where_you[user_id]]["actions"] != "lose" and location["locations"][where_you[user_id]]["actions"] != "win":
        for action in location["locations"][where_you[user_id]]["actions"]:
            markup.add(KeyboardButton(action))
    bot.send_message(message.chat.id, location["locations"][where_you[user_id]]["description"],reply_markup=markup)
    send_photo(message)
    if location["locations"][where_you[user_id]]["actions"]=="win":
        bot.send_message(message.chat.id,"Ура, вы выбрались из леса. Вы победили!")
        bot.send_message(message.chat.id, "Если хотите сыграть ещё раз, напишите /again !")
    if location["locations"][where_you[user_id]]["actions"]=="lose":
        bot.send_message(message.chat.id,"Увы, вам не удалось выбраться из леса. Вы проиграли!")
        bot.send_message(message.chat.id, "Если хотите сыграть ещё раз, напишите /again !")


@bot.message_handler()
def check_answer(message):
    try:
        user_id = str(message.from_user.id)
        where_you[user_id]=location["locations"][where_you[user_id]]["actions"][message.text]
        safe_user_data()
        say_locations(message)
    except:
        bot.send_message(message.chat.id, "Скорее всего, такого варианта ответа нет. Используйте кнопки. Нажмите /begin")


bot.polling()