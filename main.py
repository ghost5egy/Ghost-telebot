import requests, json,  datetime
from time import sleep

class GhostTeleBot:
    def __init__(self, apikey, commands,adminchatid):
        self.adminchatid = adminchatid
        self.commands = commands
        self.offset = 0
        self.lastsent = dict()
        self.webhookurl = 'https://api.telegram.org/bot{}/'.format(apikey)

    def sendtext(self, data, chatid = False):
        chatid = chatid if chatid is not False else self.adminchatid
        telegramwebhookurl = self.webhookurl + 'sendMessage?chat_id={}&text='.format(chatid) + data
        result = requests.get(telegramwebhookurl)
        try:
            result.raise_for_status()
            print('Sent ....')
        except requests.exceptions.HTTPError as e:
            print(e)
        else:
            print("Telegram: sent with code {}.".format(result.status_code))

    def getupdates(self):
        headers = {'Accept': 'application/json'}
        telegramupdatesurl = self.webhookurl + 'getUpdates'
        params = {
            "offset": self.offset
        }
        result = requests.get(telegramupdatesurl, headers=headers, params=params).text
        rjson = json.loads(result)
        for message in rjson['result']:
            if (datetime.datetime.now() - datetime.datetime.fromtimestamp(message['message']['date'])).total_seconds() > 10:
                continue
            if message['message']['text'][1:] in list(self.commands.keys()):
                if  not self.lastsent.__contains__(message['message']['from']['id']) or message['message']['date'] > self.lastsent[message['message']['from']['id']]:
                    self.commands[message['message']['text'][1:]]['func'](message['message']['from']['id'])
                    print('{} sent {}'.format(message['message']['from']['id'],message['message']['text']))
                    self.lastsent[message['message']['from']['id']] = message['message']['date']
        print(self.offset)
        self.offset = self.offset + 1

def chatid_cmd(chatid):
    telebot.sendtext('your chat id is : {}'.format(chatid), chatid)

def testclose_cmd(chatid):
    telebot.sendtext('{} you requested close bot.'.format(chatid), chatid)

if __name__ == '__main'__:
    apikey = "<telegram-apikey>"
    chatid = "<admin-chatid>"
    commands = {
        'chatid': { 'func': chatid_cmd},
        'testclose': { 'func': testclose_cmd},
    }
    telebot = GhostTeleBot(apikey, commands, chatid)
    while True:
        telebot.getupdates()
        sleep(5)
          
