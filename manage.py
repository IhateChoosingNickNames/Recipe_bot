import sys
from recipes import services
from bot import bot
from recipes.exceptions import WrongInputError


commands_db = ["create_db", "populate_db"]
commands_bot = ["start_bot"]

def main():

    try:
        command = sys.argv[1]
    except IndexError:
        print("Введите команду")
    else:
        if command in commands_db:
            getattr(services, command)()
        elif command in commands_bot:
            getattr(bot, command)()
        else:
            raise WrongInputError("Введена некорретная команда")


if __name__ == '__main__':
    main()
