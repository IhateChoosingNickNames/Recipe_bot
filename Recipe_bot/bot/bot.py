import telebot
from telebot import types

from recipes.queries import (add_recipe, get_categories, get_my_recipes,
                             get_random_recipe, get_recipes, get_types)
from settings import TOKEN

from .help_stuff import show_result

bot = telebot.TeleBot(TOKEN)


commands = [
    "/get_recipe",
    "/add_recipe",
    "/menu",
    "/start",
    "/get_random_recipe",
    "/my_recipes",
]

res = {
    "get": True,
    "category": None,
    "type_": None,
    "amount": None,
    "title": None,
    "text": None,
}


def start_bot():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()


@bot.message_handler(commands=["my_recipes"])
def bot_my_recipes(request):
    """Фунция приветствия."""
    bot.delete_message(request.chat.id, request.message_id)
    result = get_my_recipes(request.from_user.username)
    bot.send_message(
        request.chat.id,
        f"Вывожу посты пользователя {request.from_user.first_name}!",
        parse_mode="HTML",
    )
    show_result(bot, result, request)


@bot.message_handler(commands=["start"])
def bot_start(request):
    """Фунция приветствия."""
    user = request.from_user.first_name or request.from_user.username
    bot.delete_message(request.chat.id, request.message_id)
    bot.send_message(
        request.chat.id, f"Приветствую, {user}!", parse_mode="HTML"
    )
    bot.send_message(
        request.chat.id,
        "Для продолжения работы введите: /menu",
        parse_mode="HTML",
    )


@bot.message_handler(commands=["get_random_recipe"])
def bot_get_random_recipe(request):
    bot.delete_message(request.chat.id, request.message_id)
    rnd_recipe = get_random_recipe()
    bot.send_message(
        request.chat.id,
        f"***Рандомный рецепт - {rnd_recipe.title}.***",
        parse_mode="MARKDOWN",
    )
    bot.send_message(
        request.chat.id,
        (f"Автор рецепта: <i>{rnd_recipe.author.last_name} "
         f"{rnd_recipe.author.first_name}</i>, "
         f"никнейм - <b>{rnd_recipe.author.username}</b>"),
        parse_mode="HTML",
    )
    bot.send_message(request.chat.id, f"{rnd_recipe.text}", parse_mode="HTML")


@bot.message_handler(commands=["menu"])
def bot_menu(request):
    """Функция получения списка доступных команд."""
    bot.delete_message(request.chat.id, request.message_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(*[types.KeyboardButton(text=elem) for elem in commands])
    bot.send_message(request.chat.id, "Доступные команды:", reply_markup=kb)


@bot.message_handler(commands=["get_recipe", "add_recipe"])
def bot_choose_type(request):
    if request.text != "/get_recipe":
        res["get"] = False
    bot.delete_message(request.chat.id, request.message_id)
    types_ = get_types()
    keyboard = types.InlineKeyboardMarkup()
    for elem in types_:
        button = types.InlineKeyboardButton(
            f"{elem.title}", callback_data=f"{elem.title}"
        )
        keyboard.add(button)

    bot.send_message(
        request.chat.id, text="Выберите тип:", reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: res["type_"] is None)
def bot_choose_cat(call):
    res["type_"] = call.data
    types_ = get_categories()
    keyboard = types.InlineKeyboardMarkup()
    for elem in types_:
        button = types.InlineKeyboardButton(
            f"{elem.title}", callback_data=f"{elem.title}"
        )
        keyboard.add(button)

    bot.send_message(
        call.json["message"]["chat"]["id"],
        text="Выберите категорию:",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: res["category"] is None)
def bot_set_amount(call):
    res["category"] = call.data
    if res["get"]:
        sent = bot.send_message(
            call.json["message"]["chat"]["id"],
            "Введите количество рецептов:",
            parse_mode="HTML",
        )
        bot.register_next_step_handler(sent, bot_get_recipes)
    else:
        sent = bot.send_message(
            call.json["message"]["chat"]["id"],
            "Введите название рецепта:",
            parse_mode="HTML",
        )
        bot.register_next_step_handler(sent, bot_set_title)


def bot_get_recipes(request):
    res["amount"] = int(request.text)
    result = get_recipes(res)
    show_result(bot, result, request)


def bot_set_title(request):
    res["title"] = request.text
    sent = bot.send_message(
        request.chat.id, "Введите рецепт:", parse_mode="HTML"
    )
    bot.register_next_step_handler(sent, bot_add_recipe)


def bot_add_recipe(request):
    res["text"] = request.text
    res["author"] = {
        "username": request.from_user.username,
        "first_name": request.from_user.first_name,
        "last_name": request.from_user.last_name,
    }
    add_recipe(res)
    bot.send_message(request.chat.id, "Рецепт успешно добавлен!")


@bot.message_handler(func=lambda x: x not in commands)
def bot_wrong(request):
    """Функция ответа на некорретно введенную команду."""
    bot.reply_to(request, "Введена некорретная команда.")


# def bot_get_photo(request):
#     url = f"https://api.telegram.org/bot{SECRET_KEY}/getFile?file_id={request.photo[-1].file_id}"
#
#     res = requests.get(url)
#
#     file_path = json.loads(res.content)["result"]["file_path"]
#
#     template = f"https://api.telegram.org/file/bot{SECRET_KEY}/{file_path}"
#
#     res = requests.get(template)
#
#     with open("tmp.png", "wb") as file:
#         file.write(res.content)
#
#     sent = bot.send_message(request.chat.id, f'Введите рецепт:', parse_mode='HTML')
#     bot.register_next_step_handler(sent, bot_recipe_maker)
