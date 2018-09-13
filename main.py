# Bibliotecas padrão
import sys
import time
# Telegram bot
import telepot
from telepot.loop import MessageLoop
# Chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from settings import *


# Configurações do bot
chatterbot = ChatBot(
    'Velho Vini',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    #input_adapter='chatterbot.input.TerminalAdapter',
    input_adapter='chatterbot.input.VariableInputTypeAdapter',
    #output_adapter='chatterbot.output.TerminalAdapter',
    output_adapter='chatterbot.output.OutputAdapter',
    output_format='text',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        #'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    database='./db.sqlite3'
)

# Configura treinamento do chatterbot
chatterbot.set_trainer(ChatterBotCorpusTrainer)
chatterbot.train(
    'chatterbot.corpus.portuguese'
)

# Função do chatterbot
def conversaBot(mensagem):
    """
    Chatterbot recebe mensagem e responde
    """
    try:
        bot_input = chatterbot.get_response(mensagem)
        return str(bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        return "Ocorreu um erro!"

# Cria objeto telebot e habilita com token do Telegram
telebot = telepot.Bot(TELEGRAM['TOKEN'])

# Método do telebot
def handle(msg):
    """
    Recebe a mensagem do usuário no Telegram, envia ao chatterbot e retorna ao Telegram
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        fraseusuario = str(msg['text'])
        respostabot = conversaBot(fraseusuario)
        msg['text'] = respostabot
        telebot.sendMessage(chat_id, msg['text'])
    else:
        msg['text'] = "Não entendi sua mensagem, eu só compreendo textos."
        telebot.sendMessage(chat_id, msg['text'])

# Loop do telebot
MessageLoop(telebot, handle).run_as_thread()

print('Listening...')

while 1:
    time.sleep(10)
































# FIM
