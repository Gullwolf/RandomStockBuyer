from alpaca_trade_api.rest import REST, TimeFrame
#import pandas as pd
import time
from datetime import datetime
from random import randint

BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = "PKM029F6M9UPTKURU3QS"
SECRET_KEY = "fiIAe9lbKCbt5LYo1sracYxsVeJZtIzdk8A5qk52"

# Instantiate REST API Connection
api = REST(key_id=KEY_ID,secret_key=SECRET_KEY,base_url=BASE_URL)


def checkDay():
    currentDayAsInt = datetime.today().weekday()
    print(currentDayAsInt)
    return currentDayAsInt

def checkTime():
    now = datetime.now()
    currentHour = now.hour
    #print(currentHour)
    currentMinute = now.minute
    #print(currentMinute)
    if(len(str(currentMinute)) <= 1 ):
        currentTime = "" + str(currentHour) + "0" + str(currentMinute)
    else:
        currentTime = "" + str(currentHour) + str(currentMinute)
    currentTimeAsInt = int(currentTime)
    #print(currentTime)
    print(currentTimeAsInt)
    return currentTimeAsInt

def chooseStock():
    value =  randint(0, 1000)
    

    return "TSLA"

def buyStock(chosenStock):

    api.submit_order(
    symbol= chosenStock,
    qty= 1,
    side= 'buy',
    type= 'market',
    time_in_force= 'gtc'
    )

    print("Bought")

    return checkPrice(chosenStock)

def sellStock(chosenStock):

    api.submit_order(
    symbol= chosenStock,
    qty= 1,
    side= 'sell',
    type= 'market',
    time_in_force= 'gtc'
    )

    print("SOLD!")

def checkPrice(chosenStock):

    time.sleep(1)

    position = api.get_position(chosenStock)
    print("Current Price: " + position.current_price)

    return float(position.current_price)

def checkPositions():
    position = api.get_position()
    position

def main():
    chosenStock = ""
    sold = False
    currentPrice = 0.00
    profitPrice = 0.00
    lossPrice = 0.00
    daysOfTheWeek = [0, 1, 2, 3, 4]

    while(True):
        #print("WRONG DAY!")
        if(checkDay() in daysOfTheWeek):
            #print("WRONG TIME!")
            if((checkTime() >= 830) and (checkTime() <= 2100)):
                chosenStock = chooseStock()
                #buyStock(chosenStock)
                currentPrice = buyStock(chosenStock)
                print("BOUGHT!")
                profitPrice = currentPrice + ((currentPrice / 100) * 0.1)
                print(profitPrice)
                lossPrice = currentPrice - ((currentPrice / 100) * 0.1)
                print(lossPrice)
                sold = False
                while(not sold):
                    time.sleep(0.1)
                    currentPrice = checkPrice(chosenStock)
                    if(currentPrice >= profitPrice):
                        sellStock(chosenStock)
                        sold = True
                        print("SOLD!")
                    elif(currentPrice <= lossPrice):
                        sellStock(chosenStock)
                        sold = True
                        print("SOLD!")
                    elif(checkTime() == 1625):
                        sellStock(chosenStock)
                        sold = True
                        print("SOLD!")

main()
