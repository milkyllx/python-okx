from base_exchange import BaseExchange
from binance.um_futures import UMFutures
from bot.config import margin_config, swap_config, spot_config
from bot.exchange_config import EXCHANGE_BINANCE
#!/usr/bin/env python
import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.DEBUG)

class BinanceExchange(BaseExchange):
    def __init__(self, api_key, secret_key):
        super().__init__(api_key, secret_key, None)
        # 初始化Binance API
        # self.trade_api = ...
        self.um_futures_client = UMFutures(key=api_key, secret=secret_key)

    # def place_order(self, message):
    #     instrument = message["instrument"]
    #     print(f"Placing order on Binance: {instrument}")
    #     # 示例下单逻辑
    #     # try:
    #     #     self.trade_api.place_order(...)
    #     # except Exception as e:
    #     #     print(f"Error placing order on Binance: {e}")

    def process_trade_message(self, message):
        signal_token = message.get("signalToken")
        tv_instrument = message.get("instrument")
        # 如果是OKX交易所
        instrument = self.convert_instrument(tv_instrument)
        timeframe = message.get("timeframe")
        action = message.get("action")
        is_contract = self.check_perpetual_contract(tv_instrument)

        if is_contract:  # 永续合约
            self.execute_swap_trade(signal_token, instrument, message)
            pass

        else:
            self.execute_spot_trade(signal_token, instrument, message)
            self.execute_margin_trade(signal_token, instrument, message)
            pass
        pass

        # 执行合约交易

    def execute_swap_trade(self, signal_token, instrument, message):

        for config in swap_config:
            if (config["exchange"] == EXCHANGE_BINANCE
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument):
                # and config["timeframe"] == timeframe)\
                # TODO: 来源于配置还是来源于信号？
                # 优先来源于配置
                size = config["size"]  #
                if size <= 0:
                    size = message.get("amount")  # 代币数量

                action = message.get("action")
                marketPosition = message.get("marketPosition")
                prevMarketPosition = message.get("prevMarketPosition")

                side = "BUY"
                if action == "buy":
                    side = "BUY"  # 交易方向 buy: 单向持仓时代表买入，双向持仓时代表多头方向 sell: 单向持仓时代表卖出，双向持仓时代表空头方向

                    if marketPosition == "long":
                        # 开多单
                        positionSide = "LONG"

                    if marketPosition == "short" or marketPosition == "flat":
                        # 平空单
                        positionSide = "SHORT"
                if action == "sell":
                    side = "SELL"

                    if marketPosition == "short":
                        # 开空单
                        positionSide = "SHORT"
                    if marketPosition == "long" or marketPosition == "flat":
                        # 平多单
                        positionSide = "LONG"
                print(
                    f"Executing SWAP trade: {instrument}, side:{side}, positionSide: {positionSide},size: {size}")
                try:
                    response = self.um_futures_client.new_order(
                        symbol=instrument,
                        side=side,
                        positionSide=positionSide,
                        type="MARKET",
                        quantity=size,

                    )
                    logging.info(response)
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )

        # 执行现货交易

    def execute_spot_trade(self, signal_token, instrument, message):
        for config in spot_config:
            if (config["exchange"] == EXCHANGE_BINANCE
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument):
                size = config["size"]
                print(f"Executing SPOT trade: {instrument}, size: {size}, price: ")
                action = message.get("action")
                #
                if action == "buy":
                    pass
                else:
                    pass
                # 调用现货交易API
                # try:
                #     tradeApi.place_order(instId=instrument, tdMode="cash", side="buy", ordType="market", sz=size)
                # except Exception as e:
                #     print(f"Error executing SPOT trade: {e}")
        pass

        # 执行杠杆交易

    def execute_margin_trade(self, signal_token, instrument, timeframe, current_price):
        for config in margin_config:
            if (config["exchange"] == EXCHANGE_BINANCE
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument):
                size = config["size"]
                td_mode = config["tdMode"]
                print(
                    f"Executing MARGIN trade: {instrument}, size: {size}, mode: {td_mode}, price: {current_price}")
                # 调用杠杆交易API
                # try:
                #     tradeApi.place_order(instId=instrument, tdMode=td_mode, side="buy", ordType="market", sz=size)
                # except Exception as e:
                #     print(f"Error executing MARGIN trade: {e}")
        pass
