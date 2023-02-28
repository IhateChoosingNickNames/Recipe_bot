import datetime

from recipes.exceptions import WrongInputError
from recipes.queries import get_categories, get_types

TIME_OUT = {"last_time_called": None, "delay": datetime.timedelta(seconds=30)}


def validate_author_fields(initital_data):
    validated_data = {}
    for key, value in initital_data.items():
        if value is not None:
            validated_data[key] = value
    return validated_data


def parse_input(data):
    data = data.split("*")
    result = {"category": None, "type_": None, "amount": None, "title": None}
    try:
        tmp = int(data[-1])
    except ValueError:
        pass
    else:
        result["amount"] = tmp
        del data[-1]

    if not data:
        raise WrongInputError

    result["category"] = data[0]
    del data[0]

    if data:
        result["type_"] = data[0]
        del data[0]

    if data:
        result["title"] = data[0]
        del data[0]

    return result


def show_available_cats_and_types(bot, self):
    if (
        TIME_OUT["last_time_called"] is not None
        and datetime.datetime.now() - TIME_OUT["last_time_called"]
        < TIME_OUT["delay"]
    ):
        return

    TIME_OUT["last_time_called"] = datetime.datetime.now()

    cats = get_categories()
    recipe_types = get_types()

    bot.send_message(
        self.chat.id, "<b>Список доступных категорий</b>:", parse_mode="HTML"
    )
    for index, elem in enumerate(cats):
        bot.send_message(
            self.chat.id,
            f"{index + 1}. <i>{elem.title}</i>",
            parse_mode="HTML",
        )

    bot.send_message(
        self.chat.id, "<b>Список доступных типов</b>:", parse_mode="HTML"
    )
    for index, elem in enumerate(recipe_types):
        bot.send_message(
            self.chat.id,
            f"{index + 1}. <i>{elem.title}</i>",
            parse_mode="HTML",
        )


def show_result(bot, result, request):
    if result:
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
