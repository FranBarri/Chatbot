from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


bot = ChatBot(
    "Chatbot bancario"
)

trainer = ChatterBotCorpusTrainer(bot)

trainer.train('./data')

while True:
    try:
        entrada= input()
        if(entrada=="salir"):
            break
        
        else:
            bot_input = bot.get_response(entrada)
            print(bot_input)
        

    except(KeyboardInterrupt, EOFError, SystemExit):
        break