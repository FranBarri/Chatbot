from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def iniciar_chatbot():
    bot = ChatBot("Chatbot bancario")
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.spanish")
    trainer.train("./data")
    return bot

def obtener_respuesta(bot, pregunta):
    return bot.get_response(pregunta)
