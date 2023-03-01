import telebot
from telebot import types

from recipes.queries import (add_recipe, create_type_or_category,
                             get_categories, get_my_recipes, get_random_recipe,
                             get_recipes, get_types)
from settings import TOKEN

from .utils import (DATA, clear, commands, correct_author_fields, is_admin,
                    is_command, show_result)

bot = telebot.TeleBot(TOKEN)


def start_bot():
    """Инициализация бота."""
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()


@bot.message_handler(commands=["start"])
def bot_start(request):
    """Приветствия."""
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


@bot.message_handler(commands=["my_recipes"])
def bot_my_recipes(request):
    """Вывод рецептов текущего пользователя."""
    bot.delete_message(request.chat.id, request.message_id)
    result = get_my_recipes(request.from_user.username)
    bot.send_message(
        request.chat.id,
        f"Вывожу посты пользователя {request.from_user.first_name}!",
        parse_mode="HTML",
    )
    show_result(bot, result, request)


@bot.message_handler(commands=["get_random_recipe"])
def bot_get_random_recipe(request):
    """Вывод рандомного рецепта."""
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
    """Отображение меню из доступных команд."""
    bot.delete_message(request.chat.id, request.message_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(*[types.KeyboardButton(text=elem) for elem in commands])
    bot.send_message(request.chat.id, "Доступные команды:", reply_markup=kb)


@bot.message_handler(commands=["get_recipe", "add_recipe"])
def bot_choose_type(request):
    """Запуск логики получения или добавления рецепта.
    Выводит список всех текущих типов. Пользователь должен
    будет выбрать один из типов для продолжения.

    Добавлять можно рецепты только в уже имеющиеся категории/типы.
    """
    if request.text != "/get_recipe":
        DATA["get"] = False

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


@bot.callback_query_handler(func=lambda call: DATA["type_"] is None)
def bot_choose_cat(call):
    """Запись полученного ранее типа и вывод категорий."""

    if is_command(call.data):
        clear(DATA)
        return

    DATA["type_"] = call.data
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


@bot.callback_query_handler(func=lambda call: DATA["category"] is None)
def bot_set_amount(call):
    """Запись полученной категории и запрос на ввод кол-ва."""
    if is_command(call.data):
        clear(DATA)
        return

    DATA["category"] = call.data

    if DATA["get"]:
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
    """Вывод всех рецептов, удовлетворяющих условиям."""
    if is_command(request.text):
        clear(DATA)
        return

    DATA["amount"] = int(request.text)
    result = get_recipes(DATA)
    show_result(bot, result, request)
    clear(DATA)


def bot_set_title(request):
    """Запись названия рецепта и запрос на получение текста."""
    if is_command(request.text):
        clear(DATA)
        return

    DATA["title"] = request.text
    sent = bot.send_message(
        request.chat.id, "Введите рецепт:", parse_mode="HTML"
    )
    bot.register_next_step_handler(sent, bot_add_recipe)


def bot_add_recipe(request):
    """Запись текста, получение автора и добавления нового рецепта."""
    if is_command(request.text):
        clear(DATA)
        return

    DATA["text"] = request.text
    DATA["author"] = {
        "username": request.from_user.username,
        "first_name": request.from_user.first_name,
        "last_name": request.from_user.last_name,
    }
    DATA["author"] = correct_author_fields(DATA["author"])

    add_recipe(DATA)
    bot.send_message(request.chat.id, "Рецепт успешно добавлен!")
    clear(DATA)


@bot.message_handler(commands=["admin"])
def test(request):
    """Вход в админку."""

    if not is_admin(bot, request):
        bot.send_message(request.chat.id, "У вас нет прав администратора.")
        return

    cmds = ["/add_category", "/add_type"]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(*[types.KeyboardButton(text=elem) for elem in cmds])
    bot.send_message(request.chat.id, "Доступные команды:", reply_markup=kb)


@bot.message_handler(commands=["add_category", "add_type"])
def admin(request):
    """Вывод действия для админа."""
    if request.text.startswith("/add_type"):
        DATA["is_type"] = True
    else:
        DATA["is_type"] = False

    bot.delete_message(request.chat.id, request.message_id)

    sent = bot.send_message(
        request.chat.id, "Введите название:", parse_mode="HTML"
    )
    bot.register_next_step_handler(sent, bot_create_cat_or_type)


def bot_create_cat_or_type(request):
    """Создание запись названия и запуск создания."""
    if is_command(request.text):
        clear(DATA)
        return

    DATA["title"] = request.text
    create_type_or_category(DATA)
    bot.send_message(request.chat.id, "Создано.")


@bot.message_handler(func=lambda x: x not in commands)
def bot_wrong(request):
    """Отбойник - ответ на некорректно введенную команду."""
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
