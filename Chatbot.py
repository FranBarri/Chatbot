from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


bot = ChatBot(
    "Chatbot bancario"
)

trainer = ChatterBotCorpusTrainer(bot)

trainer.train("chatterbot.corpus.spanish")
trainer.train('./data')

# Mensaje de bienvenida
print("Bot: ¡Bienvenido al Chatbot del Banco!")

while True:
    try:
        entrada = input('Tú: ')
        if(entrada=="salir"):
            break
        bot_input = bot.get_response(pedido)
        print("Bot: ", bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break