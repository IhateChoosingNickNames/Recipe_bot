from recipes.queries import get_user

commands = [
    "/get_recipe",
    "/add_recipe",
    "/menu",
    "/start",
    "/get_random_recipe",
    "/my_recipes",
]

DATA = {
    "get": None,
    "category": None,
    "type_": None,
    "amount": None,
    "title": None,
    "text": None,
}

ADMIN_DATA = {
    "action": None,
    "to_delete_title": None,
    "to_delete_model": None
}

admin_add_cmds = [
    "/add_category",
    "/add_type"
]

admin_delete_cmds = [
    "/delete_type",
    "/delete_category",
    "/delete_recipe"
]

def correct_author_fields(initial_data):
    """Удаление пустых ключей."""
    validated_data = {}
    for key, value in initial_data.items():
        if value is not None:
            validated_data[key] = value
    return validated_data


def show_result(bot, result, request):
    """Отправка результата в чат."""

    if result.count() > 0:
        for index, elem in enumerate(result):
            bot.send_message(
                request.chat.id,
                f"***{index + 1}. Название рецепта: {elem.title}***",
                parse_mode="MARKDOWN",
            )
            bot.send_message(
                request.chat.id,
                (f"Автор рецепта: <i>{elem.author.last_name} "
                 f"{elem.author.first_name}</i>, никнейм - <b>"
                 f"{elem.author.username}</b>"),
                parse_mode="HTML",
            )
            bot.send_message(
                request.chat.id, f"Рецепт: {elem.text}", parse_mode="HTML"
            )
    else:
        bot.send_message(
            request.chat.id,
            (
                "К сожалению, у нас пока нет рецепта с такими параметрами, "
                "попробуйте ввести другие параметры"
            ),
            parse_mode="HTML",
        )


def clear(data):
    """Обнуление вспомогательного словаря."""
    for elem in data:
        data[elem] = None


def is_command(data):
    """Проверка наличия команды в начале сообщения."""
    for elem in commands + admin_add_cmds + admin_delete_cmds:
        if data.startswith(elem):
            return True
    return False


def is_admin(bot, request):
    data = {
        "username": request.from_user.username,
        "first_name": request.from_user.first_name,
        "last_name": request.from_user.last_name,
    }
    user = get_user(correct_author_fields(data))
    bot.delete_message(request.chat.id, request.message_id)

    if not user.is_admin:
        return False

    return True
