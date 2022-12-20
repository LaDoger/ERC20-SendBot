import web3
import time
import datetime
import constants as c # From constants.py file
from sendbot import SendBot # From sendbot.py file
from wallets import WALLETS # From wallets.py file


def main():
    sendbot = SendBot(
            # init
        )

    while True:
        try:
            today: datetime.date = datetime.datetime.utcnow().date() # UTC time

            if today > sendbot.last_sent_date:
                # Send the token if the bot hasn't sent the token today yet
                sendbot.send()
                print("Sent")

                sendbot.last_sent_date = today
                print(f'Latest sent date: {today}')

            time.sleep(3600)

        except:
            print('Error! Will try again in 600 seconds...\n')
            time.sleep(600) # Wait 600 seconds then try again


if __name__ == '__main__':
    main()