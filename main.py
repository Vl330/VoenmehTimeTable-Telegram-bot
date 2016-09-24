#!/usr/bin/env python3
# -*- coding: utf-8 -*

import logging
from telegram.ext import Updater, CommandHandler
import core
from storer import Storer
from user import UserInfo

users = {}
TOKEN_FILENAME = 'token.lst'
DATABASE_FILE = 'database.db'

storer = Storer('database.db')

logging.basicConfig(
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='''Привет. Для того, чтобы начать пользоваться ботом\
                          нужно указать свой номер группы. Для этого\
                          воспользуйтесь функцией /setgroup.\nПример:\
                          \n/setgroup и153''')


def help(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text='''Доступные команды:\
                         \n/today - Расписание на сегодня\
                         \n/week - Расписание на текущую неделю''')


def log_params(method_name, update):
    logger.debug("Method: %s\nFrom: %s\nchat_id: %d\nText: %s",
                 method_name,
                 update.message.from_user,
                 update.message.chat_id,
                 update.message.text)


def week(bot, update):
    log_params('week', update)
    telegram_user = update.message.from_user
    if telegram_user.id not in users:
        bot.sendMessage(update.message.chat_id,
                        text="Укажите ваш номер группы с помощью команды \
                              /setgroup.\nПример:\n/setgroup и153")
        return
    user = users[telegram_user.id]
    group = user.group
    schedule = core.get_day(core.get_week(group))
    bot.sendMessage(update.message.chat_id,
                    text='Расписание группы {} на текущую неделю:\
                          \n{}'.format(group, schedule))


def today(bot, update):
    log_params('today', update)
    telegram_user = update.message.from_user
    if telegram_user.id not in users:
        bot.sendMessage(update.message.chat_id,
                        text="Укажите ваш номер группы с помощью команды\
                              /setgroup.\nПример:\n/setgroup и153")
        return
    user = users[telegram_user.id]
    group = user.group
    schedule = core.get_day(core.today(group))
    bot.sendMessage(update.message.chat_id,
                    text='Расписание группы {} на сегодня:\
                    \n{}'.format(group, schedule))


def set_group(bot, update, args):
    log_params('setgroup', update)
    if len(args) != 1:
        bot.sendMessage(update.message.chat_id,
                        text="Пример команды:\n/setgroup и153")
        return
    group = args[0]
    telegram_user = update.message.from_user
    users[telegram_user.id] = UserInfo(telegram_user, group)
    storer.store('users', users)
    bot.sendMessage(update.message.chat_id,
                    text="Принято")


def read_token():
    token_file = open(TOKEN_FILENAME)
    token = token_file.readline().strip()
    token_file.close()
    return token


def main():
    global users
    users = storer.restore('users')
    if users is None:
        users = {}
    token = read_token()
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("setgroup", set_group, pass_args=True))
    dispatcher.add_handler(CommandHandler("today", today))
    dispatcher.add_handler(CommandHandler("week", week))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

