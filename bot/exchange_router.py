from bot.exchange_config import EXCHANGE_OKX
from okx_exchange import OKXExchange
from bitget_exchange import BitgetExchange
from binance_exchange import BinanceExchange

class ExchangeRouter:
    def __init__(self, config):
        self.config = config
        self.exchanges = {
            "OKX": OKXExchange(config["OKX"]["api_key"], config["OKX"]["secret_key"], config["OKX"]["passphrase"]),
            "BITGET": BitgetExchange(config["BITGET"]["api_key"], config["BITGET"]["secret_key"], config["BITGET"]["passphrase"]),
            "BINANCE": BinanceExchange(config["BINANCE"]["api_key"], config["BINANCE"]["secret_key"])
        }


    def route_message(self, message):
        exchange_name = message.get("exchange")
        if exchange_name is None:
            exchange_name = EXCHANGE_OKX

        if exchange_name in self.exchanges:
            exchange = self.exchanges[exchange_name]
            exchange.process_trade_message(message)
        else:
            print(f"Unsupported exchange: {exchange_name}")
