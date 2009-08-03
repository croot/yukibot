#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xmpp
import os
import time
sys.path.append("./core")
from bot import bot
#from func import get_local_time


def main():
    print "init..."
    yuki = bot()
    print "connecting..."
    yuki.connect()
    print "auth..."
    yuki.auth()
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


    # Main cycle
    while yuki.running == True:
        yuki.client.Process(1)
    print u"Отключаемся..."
    yuki.disconnect()
    print u"Выходим..."
    sys.exit(0)

#начало
main()