#!/usr/bin/python
# -*- coding: utf-8 -*-
#Главный класс бота
import sys
import xmpp
import time
from func import get_local_time
from time import strftime

sys.path.append("./addons")
#from weather import weather_informer
#import thread
#import threading
import commandos
#import weather
import codecs

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
        #Еще свойства
        self.controlled = False


    def connect(self):
        """test"""
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

        #Пишем сообщение в лог
        #TODO: Сделать _нормальную_ систему логирования!
        #log_message = unicode(timestamp+u" "+sender+u" "+text+"\n")
        #self.write_log(log_message)

        #Корректируем отправителя в зависимости от типа сообщения
        #Т.е. чтобы из конференции приходили в конференцию сообщения
        #TODO Сделать sender'a изменяемым
        if mtype == u"groupchat":
            sender = "yukibottest@conference.jabber.ru"
        elif mtype == u"chat":
            pass
        else:
            return 0


        #Маркер команд - первый символ решетка #

        #Временный костыль для записи истории в конференции
        #TODO: Костыль убрать. Когда-нибудь :)
        if mtype == u"groupchat":
            log_message = unicode(strftime("%Y-%m-%d %H:%M:%S")+u" | "+sender+u" | "+text+"\n")
            self.write_log(log_message)

        #Игнорируем сообщения без маркера в групчате
        if ((mtype == u"groupchat") and not( text[0] == u"#" )):
            return 0




        #Удаляем маркер, если есть
        if text[0] == u"#":
            text = text[1:]

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

        #Ищем команду в списке, выполняем. Если нет - ничего не делаем.
        for task in commandos.commands_dict:
            if command == task:
                #self.send(sender, u"Принята команда " + command,mtype)
                #print sender
                time.sleep(1)
                function = commandos.commands_dict.get(command)
                #Проверяем функцию на вызываемость и вызываем её
                if callable(function):
                    function(self,sender,argument,mtype)
                break
        else:
            #self.send(sender, u"Команда не найдена")
            return 0


    def process_presence(self,conn,msg):
        #TODO: Разобраться с этой хренью!
        #Думаю, эту хрень можно использовать с большей пользой
        msg_type = unicode(msg.getType())
        sender = unicode(msg.getFrom())
        presence = sender + u" " + msg_type
        print presence


    def process_disconnect(self):
        #TODO: Разобраться  как следует с дисконнектом
        print u"Потеряно соединение, переподключаюсь"
        self.connect()
        self.auth()

    def set_status(self,show,status):
        priority = 5
        #Индусокод, но щто поделать ^_^
        pres = xmpp.Presence(priority = priority, show = show, status = status)
        self.client.send(pres)

    def write_log(self,message):
        """Простая функция записи сообщений в лог"""
        try:
            logfile = codecs.open("log.txt", "a","utf-8")
            try:
                logfile.write(message)
            finally:
                logfile.close()
        except IOError, error:
            print error

    def set_priority(self,priority):
        pres = xmpp.Presence(priority = priority)
        self.client.send(pres)