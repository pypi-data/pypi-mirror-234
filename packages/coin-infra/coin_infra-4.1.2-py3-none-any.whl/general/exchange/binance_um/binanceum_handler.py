from general.exchange.type_enum import BINANCEUM
from general.exchange.exchange_handler import ExchangeHandler
from binance.um_futures import UMFutures
from binance.error import ClientError
from general.exchange.type_enum import (
    MARKET, LIMIT,
    GTC
)
from .utils import to_side, to_symbol


class BinanceUMHandler(ExchangeHandler):
    NAME = BINANCEUM

    def __init__(self, api_key='', api_secret='', logger=None):
        super().__init__(logger)
        self.um_futures = UMFutures(key=api_key, secret=api_secret)

    def create_market_order(self, base, quote, side, qty, dry_run=False):
        try:
            if dry_run:
                ret = self.um_futures.new_order_test(symbol=to_symbol(base, quote), side=to_side(side), type=MARKET,
                                                     quantity=qty)
            else:
                ret = self.um_futures.new_order(symbol=to_symbol(base, quote), side=to_side(side), type=MARKET,
                                                quantity=qty)
            return ret
        except ClientError as error:
            self.logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def create_limit_order(self, base, quote, side, qty, price, time_in_force=GTC, dry_run=False):
        try:
            if dry_run:
                ret = self.um_futures.new_order_test(symbol=to_symbol(base, quote), side=to_side(side), type=LIMIT, quantity=qty, price=price,
                                                     timeInForce=time_in_force)
            else:
                ret = self.um_futures.new_order(symbol=to_symbol(base, quote), side=to_side(side), type=LIMIT, quantity=qty, price=price,
                                                timeInForce=time_in_force)
            return ret
        except ClientError as error:
            self.logger.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    @staticmethod
    def to_market_price(data):
        return {
            '_id': data['E'],
            'ex': BinanceUMHandler.NAME,
            'b': data['b'][0][0],
            'a': data['a'][0][0],
            't': data['T']
        }
