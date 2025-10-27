# assistant_bot.py
"""
Консольний бот з обробкою помилок через декоратор input_error.
Команди:
  hello
  add <name> <phone>
  change <name> <new_phone>
  phone <name>
  all
  close / exit
"""

def parse_input(user_input: str):
    """
    Розбирає рядок користувача на команду та аргументи.
    Повертає (command, args_list), де command у нижньому регістрі.
    """
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.strip().lower(), args


# ---------- Декоратор для обробки помилок ---------- #
def input_error(func):
    """
    Ловить типові помилки вводу і повертає дружні повідомлення,
    не перериваючи роботу бота.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command"
        except ValueError as e:
            # якщо хендлер підняв ValueError з текстом — повертаемо його
            return str(e) if str(e) else "Give me name and phone please."
    return wrapper


# ---------- Хендлери команд ---------- #
@input_error
def add_contact(args, contacts: dict) -> str:
    """
    Додає контакт. Очікує: add <name> <phone>
    """
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts: dict) -> str:
    """
    Змінює телефон існуючого контакту. Очікує: change <name> <new_phone>
    """
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, new_phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = new_phone
    return "Contact updated."

@input_error
def show_phone(args, contacts: dict) -> str:
    """
    Повертає телефон за ім'ям. Очікує: phone <name>
    """
    if len(args) != 1:
        # нема аргумента імені
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError(name)
    return contacts[name]

@input_error
def show_all(contacts: dict) -> str:
    """
    Повертає всі контакти у вигляді рядків "name: phone".
    """
    if not contacts:
        return ""
    return "\n".join(f"{n}: {p}" for n, p in contacts.items())


# ---------- Взаємодія з користувачем ---------- #
def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
