import os
import time

from .binance import Binance

import logging
logger = logging.getLogger('stoptrail')


class StopTrail():

    def __init__(self, market, order_type, stop_size, interval):
        self.binance = Binance(
            api_key=os.environ.get('API_KEY'),
            api_secret=os.environ.get('API_SECRET')
        )
        self.market = market
        self.type = order_type
        self.stopsize = stop_size
        self.interval = interval
        self.running = False
        self.stoploss = self.initialize_stop()

    def initialize_stop(self):
        if self.type == "buy":
            return (self.binance.get_price(self.market) + self.stopsize)
        else:
            return (self.binance.get_price(self.market) - self.stopsize)

    def update_stop(self):
        price = self.binance.get_price(self.market)
        if self.type == "sell":
            if (price - self.stopsize) > self.stoploss:
                self.stoploss = price - self.stopsize
                logger.info(f"Current Price: {price:.8f}. Update stop loss to {self.stoploss:.8f}.")
            elif price <= self.stoploss:
                self.running = False
                amount = self.binance.get_balance(self.market.split("/")[0])
                price = self.binance.get_price(self.market)
                self.binance.sell(self.market, amount, price)
                logger.warn("Sell triggered | Price: %.8f | Stop loss: %.8f" % (price, self.stoploss))
        elif self.type == "buy":
            if (price + self.stopsize) < self.stoploss:
                self.stoploss = price + self.stopsize
                logger.info("New low observed: Updating stop loss to %.8f" % self.stoploss)
            elif price >= self.stoploss:
                self.running = False
                balance = self.binance.get_balance(self.market.split("/")[1])
                price = self.binance.get_price(self.market)
                amount = (balance / price) * 0.999 # 0.10% maker/taker fee without BNB
                self.binance.buy(self.market, amount, price)
                logger.warn("Buy triggered | Price: %.8f | Stop loss: %.8f" % (price, self.stoploss))

    def status(self):
        last = self.binance.get_price(self.market)
        return f"type: {self.type}, market: {self.market}, last: {last:.8f}, stop: {self.stoploss:.8f}"

    def run(self):
        self.running = True
        while (self.running):
            logger.info(self.status())
            self.update_stop()
            time.sleep(self.interval)
