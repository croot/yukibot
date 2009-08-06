import sys
sys.path.append("../addons")
from weather import weather_informer

#import bot
from weather import weather_informer

def command_weather(bot,sender,argument,mtype):
    informer = weather_informer(u"tokyo",u"ru")
    #print informer.weather()
    bot.send(sender,unicode(informer.weather()),mtype)