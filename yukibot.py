#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xmpp
#import os
#import time
sys.path.append("./core")
from bot import bot
#from func import get_local_time
sys.path.append("./addons")
#from weather import weather_informer
#import weather

def main():
    print "init..."
    yuki = bot()
    print "connecting..."
    yuki.connect()
    print "auth..."
    yuki.auth()
    #TODO:Это и начальный статус пренести в отдельную функцию start или как-то там
    #Устанавливаем функцию-обработчик сообщений
    yuki.client.RegisterHandler('message', yuki.process_message)
    yuki.client.RegisterDisconnectHandler(yuki.process_disconnect)
    yuki.client.RegisterHandler('presence', yuki.process_presence)
    yuki.client.sendInitPresence()

    #TODO: Создать функцию подключения к конференции
    room = "yukibottest@conference.jabber.ru/yuki"
    print "Joining " + room
    presence = xmpp.Presence(to=room)
    #presence.setTag('x',namespace=xmpp.NS_MUC).setTagData('password','helloandwelcome')
    yuki.client.send(presence)
    #Начальный статус
    yuki.set_status(u"available",u"Привет, мир!")
    # Main cycle
    while yuki.running == True:
        yuki.client.Process(1)
    print u"Отключаемся..."
    yuki.disconnect()
    print u"Выходим..."
    sys.exit(0)

#начало
main()