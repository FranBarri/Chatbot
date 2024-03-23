from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    "Chatbot bancario"
)

trainer = ChatterBotCorpusTrainer(bot)

trainer.train('./data')

while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break