import traceback
from okx.Trade import TradeAPI
from general.exchange.type_enum import OKX
from general.exchange.exchange_handler import ExchangeHandler
from general.exchange.type_enum import (
    GTC
)
from .utils import to_symbol, to_side


class OKXHandler(ExchangeHandler):
    NAME = OKX

    def __init__(self, api_key='', api_secret='', passphrase='', logger=None):
        super().__init__(logger)
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = passphrase
        self.okx_trade_demo = TradeAPI('30fb4bfc-d3ed-43ca-9656-ced5ea3e7a41',
                                       '9BFD52327F88CD251CE1FCEC0BFF495A',
                                       '2rYHFKwhxvtBKBZ$$', False, '1', debug=False)
        self.okx_trade = TradeAPI(api_key, api_secret, passphrase, False, '0',
                                  domain='https://aws.okx.com', debug=False)

    def create_market_order(self, base, quote, side, qty, dry_run=False):
        try:
            if dry_run:
                res = self.okx_trade_demo.place_order(to_symbol(base, quote), 'cross', to_side(side), 'market', qty)
            else:
                res = self.okx_trade.place_order(to_symbol(base, quote), 'cross', to_side(side), 'market', qty)
            return res
        except Exception as e:
            self.logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")

    def create_limit_order(self, base, quote, side, qty, price, time_in_force=GTC, dry_run=False):
        try:
            if dry_run:
                res = self.okx_trade_demo.place_order(to_symbol(base, quote), 'cross', to_side(side), 'limit', qty, px=price)
            else:
                res = self.okx_trade.place_order(to_symbol(base, quote), 'cross', to_side(side), 'limit', qty, px=price)
            return res
        except Exception as e:
            self.logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")

    @staticmethod
    def to_market_price(data):
        data = data['data'][0]
        return {
            '_id': data['seqId'],
            'ex': OKXHandler.NAME,
            'b': data['bids'][0][0],    
            'a': data['asks'][0][0],
            't': int(data['ts'])
        }
