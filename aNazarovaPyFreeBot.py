import telebot
import random

todos = dict()

HELP = """Доступные команды:
/help - справка о командах
/todo - добавить задачу
/random - добавить случайную задачу
/print - вывести все задачи
"""

RANDOM_TASK = ['Позвонить родителям', 'Выгулять собаку', 'Почитать книгу']

token = '****************'

bot = telebot.TeleBot(token)


def todo_add(date, task):
    if date in todos:
        todos[date].append(task)
    else:
        todos[date] = [task]
    print(f"Задача '{task}' запланирована на {date}")


print('Start telegram bot')


# /random
@bot.message_handler(commands=['random'])
def random_task(message):
    date = 'сегодня'
    task = random.choice(RANDOM_TASK)
    todo_add(date, task)
    bot.send_message(message.chat.id, f'Случайная задача "{task}" добавлена на {date}')


# /help
@bot.message_handler(commands=['help'])
def help_todo(message):
    bot.send_message(message.chat.id, HELP)


# /print date
@bot.message_handler(commands=['print'])
def print_todo(message):
    date = message.text.split()
    date = date[1]
    date.lower()
    if date in todos:
        tasks = todos[date]
        text = ''
        for task in tasks:
            text = text + f"\n[ ] {task}"
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, f"На {date} нет задач")


# /todo
@bot.message_handler(commands=['todo'])
def todo(message):
    commands = message.text.split(maxsplit=2)
    date = commands[1]
    date = date.lower()
    task = commands[2]
    if len(task) < 3:
        bot.send_message(message.chat.id, 'Задача не может быть меньше 3х символов')
    else:
        todo_add(date, task)
        bot.send_message(message.chat.id, f'Задача "{task}" добавлена на {date}')


@bot.message_handler(content_types=['text'])
def echo(message):
    if "Ангелина" in message.text:
        bot.send_message(message.chat.id, "Ба! Знакомые все лица!")
    else:
        bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
