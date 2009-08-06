#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
#import urllib
import xml.parsers.expat
#import sys
import chardet

class weather_informer():
    def __init__(self,place,lang):
        #Место и язык
        self.place = place.encode('utf-8')
        self.lang = lang.encode('utf-8')
        #Переменные для обработчика
        self.curcon = False
        self.forcon = False
        self.i=0
        self.service_error = False
        self.network_error = False
        #Пустые кривые структуры для хранения данных о прогнозах
        self.weather_now = {}
        self.weather_forecast=[{},{},{},{}]

    def get_google_weather(self):
        #Формируем URL
        url = "http://www.google.com/ig/api?weather="+self.place+"&hl="+self.lang
        #TODO: обрабатывать ошибки сети
        #Делаем запрос
        request = urllib2.Request(url)
        #Обрабатываем ошибки сети
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, error:
            self.network_error = u"Ошибка сети: "+unicode(error.code)
            return False

        self.page = response.read()
        #Определяем кодировку
        encoding = chardet.detect(self.page)
        encoding = encoding["encoding"]
        #Перекодируем в Юникод
        self.page = self.page.decode(encoding).encode('utf-8')
        return 0


    def start_element(self, name, attrs):
        #TODO: Исправить!
        if name == "problem_cause":
            self.service_error = True

        if name == "current_conditions":
            self.curcon = True

        if self.curcon == True:
            try:
                self.weather_now[name] = attrs["data"]
            except:
                pass

        if name == "forecast_conditions":
            self.forcon = True

        if self.forcon == True:
            try:
                self.weather_forecast[self.i][name] = attrs["data"]
            except:
                pass

    def end_element(self,name):
        if name == "current_conditions":
            self.curcon = False
        if name == "forecast_conditions":
            self.forcon == False
            self.i = self.i+1

    def char_data(self,data):
        pass

    def parse(self):
        #Создаем объект парсера
        parser = xml.parsers.expat.ParserCreate()
        #Регистрируем обработчики
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
        #Начинаем парсить
        parser.Parse(self.page)

    def show_weather_now(self):
        title = u"Прогноз погоды на сегодня: \n"
        temp = u"Температура: " + self.weather_now[u'temp_c'] + u"°C \n"
        hum = self.weather_now[u'humidity'] + u"\n"
        wind = self.weather_now[u'wind_condition'] + u"\n"
        cond = self.weather_now[u'condition'] + u"\n"
        return title+temp+cond+hum+wind

    def show_weather_tomorrow(self):
        title = u"Прогноз погоды на завтра: \n"
        temp = u"Температура: от " + self.weather_forecast[1][u'low'] + u"°C до "+self.weather_forecast[1][u'high'] +u"°C \n"
        cond = self.weather_forecast[1][u'condition'] + u"\n"
        return title + temp + cond

    def show_weather_forecast(self):
        title = u"Прогноз погоды на три дня вперед: \n\n"
        weather = ""
        for i in range (1,4):
            temp = u"Температура: от " + self.weather_forecast[i][u'low'] + u"°C до "+self.weather_forecast[i][u'high'] +u"°C \n"
            cond = self.weather_forecast[i][u'condition'] + u"\n"
            day = u"День: " + self.weather_forecast[i][u'day_of_week'] + u"\n"
            weather = weather + day + temp + cond + u"\n"
        return title + weather



    def weather(self, argument=None):
        self.get_google_weather()
        if self.network_error != False:
            return self.network_error

        self.parse()
        if self.service_error == True:
            return u"Ошибка сервиса. Проверьте имя города."

        if (argument == "now") or (argument == None):
            return self.show_weather_now()
        elif argument == "tomorrow":
            return self.show_weather_tomorrow()
        elif argument == "forecast":
            return self.show_weather_forecast()
        else:
            return "Oops!"




##########################################
#informer = weather_informer(u"tokyo",u"ru")
#print informer.weather()

###########################################
"""
print informer.weather_now
print informer.weather_forecast
#print "HUITA", informer.i
for element in informer.weather_now:
    print informer.weather_now[element]
for huita in xrange(4):
    print "---------------------------"
    for element in informer.weather_forecast[huita]:
        print informer.weather_forecast[huita][element]

print "###############################"
print informer.weather_forecast

print "###############################"
print informer.show_weather_now()
print "###############################"
print informer.show_weather_tomorrow()
print "###############################"
print informer.show_weather_forecast()
"""