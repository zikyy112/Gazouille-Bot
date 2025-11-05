# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 22:53:26 2025

@author: zikyy112
"""
import requests
from apscheduler.schedulers.background import BackgroundScheduler

import time
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

#%%
class GasPriceInfo(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GasPriceInfo, self).__init__(*args, **kwargs)
        self.previous_value = 0.0
        self.chat_id = 8187409056 #by default, I have put my own
        self.schedul = BackgroundScheduler()
        self.schedul.add_job(self.update_gas_info, 'interval', minutes=2)
        self.schedul.start()

    def on_chat_message(self, msg):
        self.chat_id = msg['chat']['id']
        greetings = ['hey','hello','coucou','bonjour','good morning']
        if msg['text'].lower() in greetings : 
            self.bot.sendMessage(self.chat_id, 'Howdy, I am GazouilleBot, here for your daily gas price update !')
        self.update_gas_info()
            
    def update_gas_info(self):
        """
            this function send the updating message of the gasprice info 
        """
        r = requests.get('https://api.etherscan.io/api'
                     +'?module=gastracker'
                     +'&action=gasoracle'
                     +'&apikey=censorship_of_my_APIKey')
        try :
            gas_info = r.json()['result']
            fgp = float(gas_info['FastGasPrice'])
            gur = float(gas_info['gasUsedRatio'].split(',')[0]) #to obtain only the first value
            change = fgp - self.previous_value
            message = f'FastGasPrice : {fgp:.2f}, GasUsedRatio : {gur:.2f}, Change : {change:.2f}'
            self.previous_value = fgp #and I update the previous value
        except requests.exceptions.JSONDecodeError:
            message = 'I have noticed some error during finding the content... (204) :/'
        
        self.bot.sendMessage(self.chat_id,message)

    def on_close(self, ex):
        """
            the function that stops the schedul if the chatbox is closed
        """
        self.schedul.shutdown(wait=False)

bot = telepot.DelegatorBot('8018674828:AAHA1lyYDxnOo5V0F9xllSSK1LnvFJG4xi4', [
    pave_event_space()(
        per_chat_id(), create_open, GasPriceInfo, timeout=10),
])

MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(1)
    
#%%

class GasPriceInfo(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GasPriceInfo, self).__init__(timeout = 10, *args, **kwargs)
        
        self.previous_value = 0.0
        self.running = True  #so that the bot will stop updating gasprice when user says "stop"
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.update_gas_info, 'interval', seconds = 10)
        self.scheduler.start()

    def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        text = msg['text'].lower().strip()

        if text in ['hey', 'hello', 'coucou', 'bonjour', 'good morning']:
            self.sender.sendMessage("Howdy! I'm GazouilleBot, here for your daily gas price updates! -\\_(^u ^)-\\_ "
                                    "\nIf you want me to stop, simply write \'\\stop\'. ")
        
        elif text == "/stop":
            self.running = False  #stop updating
            self.sender.sendMessage("Goodbye ! :) ")

    def update_gas_info(self):
        if not self.running:
            return

        r = requests.get('https://api.etherscan.io/api'
                         '?module=gastracker'
                         '&action=gasoracle'
                         '&apikey=censorship_of_my_APIKey')

        try:
            gas_info = r.json()['result']
            fgp = float(gas_info['FastGasPrice'])
            gur = float(gas_info['gasUsedRatio'].split(',')[0])  #only the two first digit of the first value of the list
            change = fgp - self.previous_price
            message = f'FastGasPrice: {fgp:.2f}, GasUsedRatio: {gur:.2f}, Change: {change:.2f}'
            self.previous_price = fgp  
        except requests.exceptions.JSONDecodeError:
            message = "Error retrieving gas price data. (204)"

        self.sender.sendMessage(message)

    def on_close(self, ex):
        self.scheduler.shutdown()
        self.close()

bot = telepot.DelegatorBot('8103769253:AAEHBBnVVBWELyDuvaypQmcoxr4wVzH3fYE', [
    pave_event_space()(per_chat_id(), create_open, GasPriceInfo),
])

MessageLoop(bot).run_forever()

while True:
    time.sleep(1)




