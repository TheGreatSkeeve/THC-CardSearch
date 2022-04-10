import requests
import json
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()
telegram = os.getenv('telegram')
group = os.getenv('group')

id='89631139'

class card:
    def __init__(self,data):
        self.raw = data
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.desc = data['desc']
        self.card_images = data['card_images']
        if self.type == "Normal Monster" or self.type == "Effect Monster" or self.type == "Flip Effect Monster":
            self.atk = data['atk']
            self.defens = data['def']
            self.race = data['race']
            self.attribute = data['attribute']
    def getInfo(self):
        if "Monster" in self.type:
            response = "{} - {}\nAttack: {}\nDefense: {}\nDescription: {}\n\n{}".format(self.name,self.type,self.atk,self.defens,self.desc,self.card_images[0]['image_url'])
        else:
            response = "{} - {}\nDescription: {}\n\n{}".format(self.name,self.type,self.desc,self.card_images[0]['image_url'])

        return response

def getAllCards():
    data = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    raw = data.text.encode()
    allCards_raw = json.loads(raw.decode('utf-8'))['data']
    allCards = []
    for temp in allCards_raw:
        newCard = card(temp)
        allCards.append(newCard)
    return allCards

cards = getAllCards()

# Help command
def cardGet(update, context):
    print(context.args)
    id = context.args[0]
    for card in cards:
        if card.id == int(id):
            update.effective_message.reply_text(card.getInfo())


def main():
    updater = Updater(token=telegram, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("card", cardGet))
    print("Started.")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



