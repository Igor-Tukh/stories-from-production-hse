import logging
import numpy as np
import string
import re

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from enum import Enum

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

GREETING_TOKENS = {
    'hello', 'hi', 'hey', 'good', 'привет', 'здравствуйте', 'добрый', 'доброе', 'доброй', 'hallo', 'servus', 'guten',
    'gute',
}
FAREWELL_TOKENS = {
    'goodbye', 'bye', 'see', 'пока', 'свидания', 'wiedersehen', 'bis', 'tschuss',
}


class Intent(Enum):
    GREETING = 0
    FAREWELL = 1
    GREETING_FAREWELL = 2
    PYTHON_EVAL = 3
    UNKNOWN = 4


class NLUModule:
    @staticmethod
    def parse_intent(message):
        original_message = message
        message = message.lower()
        for c in string.punctuation:
            message = message.replace(c, ' ')
        greeting = False
        farewell = False
        for token in message.split(' '):
            greeting = greeting or token in GREETING_TOKENS
            farewell = farewell or token in FAREWELL_TOKENS
        if greeting and not farewell:
            return Intent.GREETING
        elif farewell and not greeting:
            return Intent.FAREWELL
        elif greeting:
            return Intent.GREETING_FAREWELL
        try:
            eval(original_message)
            return Intent.PYTHON_EVAL
        except:
            return Intent.UNKNOWN


class DMModule:
    @staticmethod
    def make_decision_as_text(intent, message):
        if intent == Intent.GREETING:
            return 'Hello!'
        elif intent == Intent.FAREWELL:
            return 'Goodbye!'
        elif intent == Intent.GREETING_FAREWELL:
            return 'Hello and/or goodbye!'
        elif intent == Intent.UNKNOWN:
            return f'I don\'t know how to respond to a message \'{message}\', sorry :('
        result = eval(message)
        return f'Result: \'{result}\'. At your service :)'


def start(update, _):
    update.message.reply_markdown_v2(
        fr'Hello, {update.effective_user.mention_markdown_v2()}\!')


def on_message(update, _):
    message = update.message.text
    update.message.reply_text(DMModule.make_decision_as_text(
        NLUModule.parse_intent(message), message))


def main():
    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, on_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
