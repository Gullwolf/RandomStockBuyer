import math
from alpaca_trade_api.rest import REST
import time
from datetime import datetime
from random import randint
import atexit


BASE_URL = "https://paper-api.alpaca.markets"
KEY_ID = ""
SECRET_KEY = ""

# Instantiate REST API Connection
api = REST(key_id=KEY_ID,secret_key=SECRET_KEY,base_url=BASE_URL, api_version = "v2")


def checkDay():
    currentDayAsInt = datetime.today().weekday()
    #print(currentDayAsInt)

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
    print("Time: " + str(currentTimeAsInt))

    return currentTimeAsInt

def chooseStock():
    value =  randint(1, 10998)
    #print(value)

    fp = open(r'.\finalStocks.txt', 'r')
    

    with open(r".\finalStocks.txt", 'r') as fp:
        # lines to read
        line_numbers = [value]
        # To store lines
        lines = []
        for i, line in enumerate(fp):
            if (i in line_numbers):
                lines.append(line.strip())
            elif (i > value):
                break
    #print(lines)
    print("Stock to buy: " + str(lines[0]))

    api.get_asset

    return str(lines[0])

def buyStock(chosenStock):

    account = api.get_account()
    moneyInAccount = account.equity

    asset = api.get_latest_trade(chosenStock)
    #print(asset)
    #print(asset.p)

    totalBuy = (float(moneyInAccount) / float(asset.p))
    #print(totalBuy)
    totalBuy = math.floor(totalBuy)
    print("Ammount bought: " + str(totalBuy))



    api.submit_order(
    symbol= chosenStock,
    qty= totalBuy,
    side= 'buy',
    type= 'market',
    time_in_force= 'gtc'
    )

    print("Bought")

    return checkFilledPrice()

def sellStock(chosenStock):

    position = api.get_position(chosenStock)
    totalSell = position.qty_available
    #print(position.qty)
    print("Ammount sold: " + position.qty_available)

    api.submit_order(
    symbol= chosenStock,
    qty= totalSell,
    side= 'sell',
    type= 'market',
    time_in_force= 'gtc'
    )

    print("SOLD!")

def checkPrice(chosenStock):
    position = api.get_position(chosenStock)
    print("Current Price: " + position.current_price)

    return float(position.current_price)

def checkPositions():
    position = api.get_position()
    position

def checkFilledPrice():
    time.sleep(2)

    activities = api.list_orders(status='all', 
                                nested='False', 
                                direction='desc',
                                limit=1)
    #print(activities)

    filledPrice = activities[0]
    #print(filledPrice)
    #print(filledPrice.filled_avg_price)

    return float(filledPrice.filled_avg_price)

def main():
    chosenStock = ""
    sold = False
    currentPrice = 0.00
    profitPrice = 0.00
    lossPrice = 0.00
    daysOfTheWeek = [0, 1, 2, 3, 4]

    while(True):
        atexit.register(sellStock, chosenStock)
        #print("WRONG DAY!")
        if(checkDay() in daysOfTheWeek):
            #print("WRONG TIME!")
            if((checkTime() >= 1430) and (checkTime() <= 2100)):
                chosenStock = chooseStock()
                #buyStock(chosenStock)
                account = api.get_account()
                moneyInAccount = account.equity
                currentPrice = buyStock(chosenStock)
                print("BOUGHT!")
                print("Price bought at: " + str(currentPrice))
                profitPrice = round((currentPrice + ((currentPrice / 100) * 0.1)), 2)
                print("Profit at: " + str(profitPrice))
                lossPrice = round((currentPrice - ((currentPrice / 100) * 0.2)), 2)
                print("Loss at: " + str(lossPrice))
                f = open("orders.txt", "a")
                f.write("Bought: " + chosenStock + ", Fill Price: " + str(currentPrice) + ", Profit Price: " + str(profitPrice) + ", Loss Price: " + str(lossPrice) + ", Equity: " + moneyInAccount + "\n")
                f.close()
                sold = False
                while(not sold):
                    time.sleep(0.1)
                    currentPrice = checkPrice(chosenStock)
                    if(currentPrice >= profitPrice):
                        sellStock(chosenStock)
                        account = api.get_account()
                        moneyInAccount = account.equity
                        f = open("orders.txt", "a")
                        f.write("Sold: " + chosenStock + ", Fill Price: " + str(currentPrice) + ", Equity: " + moneyInAccount + ", PROFIT" + "\n")
                        f.close()
                        sold = True
                        print("SOLD!")
                    elif(currentPrice <= lossPrice):
                        sellStock(chosenStock)
                        account = api.get_account()
                        moneyInAccount = account.equity
                        f = open("orders.txt", "a")
                        f.write("Sold: " + chosenStock + ", Fill Price: " + str(currentPrice) + ", Equity: " + moneyInAccount + ", LOSS" + "\n")
                        f.close()
                        sold = True
                        print("SOLD!")
                    elif(checkTime() == 1625):
                        sellStock(chosenStock)
                        sold = True
                        print("SOLD!")

main()