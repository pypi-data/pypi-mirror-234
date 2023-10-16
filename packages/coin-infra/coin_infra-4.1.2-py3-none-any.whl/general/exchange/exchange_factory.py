from general.exchange.type_enum import BINANCEUM, OKX
from general.exchange.binance_um import BinanceUMHandler
from general.exchange.okx import OKXHandler


class ExchangeFactory:
    @staticmethod
    def get_handler(exchange: str, *api_args, **kwargs):
        if not api_args:
            api_args = ['', '', '']  # walk around undetermined api_args
        if exchange == BINANCEUM:
            return BinanceUMHandler(api_args[0], api_args[1], kwargs.get('logger', None))
        elif exchange == OKX:
            return OKXHandler(api_args[0], api_args[1], api_args[2], kwargs.get('logger', None))
        else:
            raise ValueError(f"{exchange} not implemented yet")
