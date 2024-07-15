import discord
import datetime 
import time
import asyncio
import json
# import os
# from dotenv import load_dotenv, dotenv_values 
# load_dotenv() 

#needs to be hosted somewhere


global allRemindersDict 
allRemindersDict = {}


def text_parse(user_message):
    user_message = user_message.lower()
    msgList = user_message.split(',')
    acc_message = msgList[0].strip('r')
    if acc_message[0] == ' ':
        acc_message = acc_message[1:]
    date = msgList[1].strip()
    timeofday = msgList[2].strip()
    return acc_message, date, timeofday

def hour_parse(rawtime):
    #4:30pm
    #4pm
    #430pm
    isam,ispm = False, False
    rawtime = rawtime.strip()
    if ':' in rawtime:
        rawtime = rawtime[:rawtime.find(':')] + rawtime[rawtime.find(':')+1:]
    if 'am' in rawtime:
        isam = True
        rawtime = rawtime[:rawtime.find('am')]
    elif 'pm' in rawtime:
        ispm = True
        rawtime = rawtime[:rawtime.find('pm')]

    if len(rawtime) == 4:
        hour = int(rawtime[:2])
        min = int(rawtime[2:])
    if len(rawtime) == 3:
        hour = int(rawtime[:1])
        min = int(rawtime[1:])
    if len(rawtime) == 1 or len(rawtime) == 2:
        hour = int(rawtime)
        min = '00'
    
    if isam == False and ispm == False and hour < 8:  #operating on the assumption that if i say 7, it's likely 7pm
        ispm = True
    if ispm == True:
        hour += 12
    
    return str(hour), str(min)

#rhi,monday, 4:30pm
#rhi,1/5/24, 2pm

async def send_message(message, user_message, guilds, msgID, is_private):
    isSlash = False
    try:
        dayofweekdict = {'mon':0, 'tue':1, 'wed':2, 'thur':3, 'fri':4, 'sat':5, 'sun':6, 'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
        properspelldict = {'mon':'Monday', 'tue':'Tuesday', 'wed':'Wednesday', 'thur':'Thursday', 'fri':'Friday', 'sat':'Saturday', 'sun':'Sunday'}
        
        for guild in guilds: 
            
            # if guild.name == 'King DeedleP\'s server':
                acc_message, date, timeofday = text_parse(user_message)
                now = datetime.datetime.now()
                hour, min = hour_parse(timeofday)
                await message.channel.send(f'{message.author} set a reminder to do {acc_message} at {hour}:{min}')
                
                
                if '/' in date:
                    isSlash = True
                    
                    date = date.split('/')
                    month = int(date[0])
                    day = int(date[1])
                    year = int(date[2]) + 2000
                    
                    later = datetime.datetime(year,month,day,int(hour),int(min))
                    
                else:
                    
                    date = date.strip()
                    daynum = dayofweekdict[date]
                  
                    if daynum < now.weekday():
                        daynum += 7
                    daydiff = daynum-now.weekday()
                    daylater = now.day + daydiff
                    later = datetime.datetime(now.year,now.month,daylater,int(hour), int(min))
                    #got seconds for how many days
                    #got how many hours until
                    
                #message
                difference = later - now
                
                #need to get months...
                
                text_log = await guild.fetch_channel(1247378604321538129)    
                if isSlash:
                    textLogMsg = f'{message.author.mention} / {message.author} set up a reminder to {acc_message} at {hour}:{min} for {month}/{day}/{year}'
                    allRemindersDict[msgID] = f'{message.author} - {acc_message} at {hour}:{min} for {month}/{day}/{year}'
                else:
                    if len(date) > 3:
                        date = date.title()
                    else:
                        date = properspelldict[date]
                    textLogMsg = f'{message.author.mention} / {message.author} set up a reminder to {acc_message} at {hour}:{min} for {date}'
                    allRemindersDict[msgID] = f'{message.author} - {acc_message} at {hour}:{min} for {date}'
                await text_log.send(textLogMsg)
                

                seconds = int(difference.total_seconds())
                if seconds < 0:
                    seconds += 604800
                
                
                if seconds > 604800:
                    sleeptime = seconds-604800
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 1 week until you need to do {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 172800:
                    sleeptime = seconds-300
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 2 days until you need to do {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 86400:
                    sleeptime = seconds-86400
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 1 day until you need to do {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 18000:
                    sleeptime = seconds-18000
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 5 hours until you need to {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 7200:
                    sleeptime = seconds-7200 
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 2 hours until you need to {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 3600:
                    sleeptime = seconds-3600
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 1 hour until you need to {acc_message}...remember, it\'s at {timeofday}')
                if seconds > 1800:
                    sleeptime = seconds-60
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, half an hour until you need to {acc_message}...remember, it\'s at {timeofday}')
                if seconds > 300:
                    sleeptime = seconds-300
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 5 minutes until you need to {acc_message}...remember, it\'s at {timeofday}')
                if seconds > 120:
                    sleeptime = seconds-120
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, 2 minutes until you need to {acc_message}...remember, it\'s at {timeofday}')
                if seconds > 60:
                    sleeptime = seconds-60
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    await message.author.send(f'{message.author.mention} Hey, one minute until you need to {acc_message}...remember, it\'s at {timeofday}')
                
                if seconds > 5:
                    del allRemindersDict[msgID]
                    sleeptime = seconds-5
                    await asyncio.sleep(sleeptime)
                    seconds -= sleeptime
                    for i in range(8):
                        await message.author.send(f'{message.author.mention} Hey, it\'s happening RIGHT NOW! You need to {acc_message.upper()} right NOW at {timeofday}!!!!')
                        time.sleep(.5)
                            
    except Exception as e:
        print(e, 1)

def see_all():
    all = '```'
    print(allRemindersDict)
    for key in allRemindersDict:
        all += f'{allRemindersDict[key]}\n'
    all += '```'
    return all

def run_discord_bot():
    intents=discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    # Opens the file in read-only mode and assigns the contents to the variable cfg to be accessed further down
    with open('config.json', 'r') as cfg:
    # Deserialize the JSON data (essentially turning it into a Python dictionary object so we can use it in our code) 
        data = json.load(cfg) 
    TOKEN = data["token"]
    #token goes here
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content).lower()
            channel = str(message.channel)
            split = user_message.split()
            if split[0][0] == 'r':
                user_message = user_message[1:]
                await send_message(message, user_message, client.guilds, message.id, is_private=True)
            elif split[0][0] == '!':
                all = see_all()
                await message.channel.send(all)
                
                
    client.run(TOKEN)        
                