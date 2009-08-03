#!/usr/bin/python
# -*- coding: utf-8 -*-
#Главный класс бота
import sys
import xmpp
import os
import time
from func import get_local_time


class bot():
    def __init__(self):
        #Connection settings
        #TODO: Перенести параметры подключения в текст. конфиг
        self.JID = "yuki_nagato@jabber.ru"
        self.PASS = "something"
        self.RES = "Matrix"
        #Convert JID
        self.jid = xmpp.protocol.JID(self.JID)
        #Create "Client" instanse
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])
        #Выполняется ли главный цикл
        self.running = True
        #Запоминаем время подключения
        self.connect_time = get_local_time()
        self.name = u"yuki"

    def connect(self):
        if self.client.connect() != 0:
            print "Can not connect"

    def auth(self):
        if not self.client.auth(self.jid.getNode(), self.PASS, self.RES):
            print "Authentification failed"
            return False
        else:
            return True

    def send(self,recipient,msg,mtype):
        self.client.send(xmpp.protocol.Message(recipient,msg,mtype))

    def disconnect(self):
        self.client.disconnect()

    def process_message(self,conn,msg):
        #Сбрасываем команду
        command = None
        #Опеределяем отправителя, текст сообщения, время и тип
        sender = unicode(msg.getFrom())
        text = unicode(msg.getBody())
        timestamp = unicode(msg.getTimestamp())
        mtype = unicode(msg.getType())
        # Игнорируем сообщения из прошлого
        if timestamp < self.connect_time:
            return 0


        #Корректируем отправителя в зависимости от типа сообщения
        if mtype == u"groupchat":
            sender = "yukibottest@conference.jabber.ru"
        elif mtype == u"chat":
            pass
        else:
            return 0


        #Маркеры команд - имя бота и решетка
        #TODO: Объеденить поиск маркеров и их удаление

        #Игнорируем сообщения без маркеров в групчате
        if ((mtype == u"groupchat") and not( (text[0] == u"#") or ( text[0:len(self.name)] == self.name))):
            return 0

        #Удаляем маркеры
        if text[0] == u"#":
            text = text[1:]
        if text[0:len(self.name)] == self.name:
            try:
                text = text.split(None,1)
                text = text[1]
            except:
                pass

        #Разбиваем строку на первое слово и все остальное
        try:
            text=text.split(None,1)
        except:
            pass
        #Первое слово - это команда
        try:
            command = text[0]
        except:
            command = None
            return 0
        #Команду - в нижний регистр
        command = command.lower()
        #Пытаемся получить аргумент команды
        try:
            argument = text[1]
        except:
            argument = None

        #print argument;
        #TODO: перенести список команд в инит
        commands_list = [u"echo",u"exit",u"хуита",u"about","say_conf","count"]
        commands_dict = {
            u"echo":self.command_echo,
            u"exit":self.command_exit,
            u"about":self.command_about,
            u"say_conf":self.command_say_conf,
            u"count":self.command_count}

        #Ищем команду в списке, выполняем. Если нет - посылаем.
        for task in commands_list:
            if command == task:
                #self.send(sender, u"Принята команда " + command,mtype)
                #print sender
                time.sleep(1)
                function = commands_dict.get(command)
                #Проверяем функцию на вызываемость и вызываем её
                if callable(function):
                    function(sender,argument,mtype)
                break
        else:
            #self.send(sender, u"Команда не найдена")
            return 0








    def command_echo(self,sender,argument,mtype):
        if argument == None:
            self.send(sender, u"Эхо будет молчать, если никто с ним не заговорит.",mtype)
        else:
            self.send(sender, (u"Эхо: "+argument),mtype)


    def command_exit(self,sender,argument,mtype):
        self.send(sender, u"Прощайте!",mtype)
        self.running = False

    def process_presence(self,conn,msg):
        msg_type = unicode(msg.getType())
        sender = unicode(msg.getFrom())
        presence = sender + u" " + msg_type
        print presence


    def process_disconnect(self):
        print u"Потеряно соединение, переподключаюсь"
        self.connect()
        self.auth()

    def command_about(self,sender,argument,mtype):
        self.send(sender,"Юки-бот, версия 0.1 \n"+"Автор: Антон Мельников \n"+"Вступайте и компилируйте! \n"+"В месте мы сила!",mtype)

    def command_say_conf(self,sender,argument,mtype):
        conference = "yukibottest@conference.jabber.ru"
        self.send(conference,argument,"groupchat")
        print "debug"


    def command_count(self,sender,argument,mtype):
        conference = "yukibottest@conference.jabber.ru"
        i = 10
        while i>0:
            self.send(conference,unicode(i),"groupchat")
            i = i - 1
            time.sleep(1)






