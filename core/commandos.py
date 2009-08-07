#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append("./addons")
import weather

#import bot
from weather import weather_informer

class allcommands():
    def __init__(self):
        self.commands_list = [u"echo",u"exit",u"хуита",u"about",u"say_conf",u"count",u"weather"]
        self.commands_dict = {
            u"echo":command_echo,
            u"exit":command_exit,
            u"about":command_about,
            u"say_conf":command_say_conf,
            u"count":command_count,
            u"weather":command_weather}







def command_weather(bot,sender,argument,mtype):
    informer = weather_informer(u"tokyo",u"ru")
    #print informer.weather()
    bot.send(sender,unicode(informer.weather()),mtype)

def command_echo(bot,sender,argument,mtype):
    if argument == None:
        bot.send(sender, u"Эхо будет молчать, если никто с ним не заговорит.",mtype)
    else:
        bot.send(sender, (u"Эхо: "+argument),mtype)

def command_exit(bot,sender,argument,mtype):
    bot.send(sender, u"Прощайте!",mtype)
    bot.running = False

def command_about(bot,sender,argument,mtype):
    bot.send(sender,"Юки-бот, версия 0.1 \n"+"Автор: Антон Мельников \n"+"Вступайте и компилируйте! \n"+"В месте мы сила!",mtype)

def command_say_conf(bot,sender,argument,mtype):
    conference = "yukibottest@conference.jabber.ru"
    bot.send(conference,argument,"groupchat")

def command_count(bot,sender,argument,mtype):
    conference = "yukibottest@conference.jabber.ru"
    i = 10
    while i>0:
        bot.send(conference,unicode(i),"groupchat")
        i = i - 1
        time.sleep(1)


