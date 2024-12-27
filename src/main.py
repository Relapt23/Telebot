from sqlalchemy import create_engine, select, insert, delete, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Chat
import telebot
import os
from gpt import perform_request_chatGPT

engine = create_engine("postgresql://user:password@postgres:5432/bot_db",echo=True)
sess = sessionmaker(engine)

engine.echo = False
Base.metadata.create_all(engine)
engine.echo = True


bot = telebot.TeleBot(os.environ['TG_TOKEN'])

commands = [
  telebot.types.BotCommand("start", "Запустить бота"),
  telebot.types.BotCommand("clear", "Очистить историю запросов")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, "Давай начнем общение")

@bot.message_handler(commands=["help"])
def show_commands(message):
    command_list = bot.get_my_commands()
    response = "Доступные команды:\n"
    for command in command_list:
        response += f"/{command.command} - {command.description}\n"
    bot.reply_to(message, response)

@bot.message_handler(commands=['clear'])
def clear_message(message):
  id = message.from_user.id

  with sess() as session:
    session.execute(delete(Chat).where(id == Chat.user_id))
    session.commit()

  bot.send_message(message.chat.id, "История диалога удалена")

@bot.message_handler(content_types='text')
def request(message):
    id = message.from_user.id

    with sess() as session:
       history = session.execute(select(Chat.request, Chat.response).where(id == Chat.user_id).order_by(desc(Chat.id)).limit(50)).all()
       history = list(reversed(history))
       response = perform_request_chatGPT(history, message.text)       
       session.execute(insert(Chat).values({"user_id": id, "request": message.text, "response": response}))
       session.commit()

    bot.send_message(message.chat.id, response)

bot.polling()
