import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

from bot.config import swap_config, margin_config, spot_config
from bot.exchange_config import EXCHANGE_OKX
from okx import Trade, MarketData
from base_exchange import BaseExchange

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="okx_trade_log.log",
    filemode="a"
)

class OKXExchange(BaseExchange):
    def __init__(self, api_key, secret_key, passphrase):
        super().__init__(api_key, secret_key, passphrase)
        self.trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, False, '0')
        self.market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, False, '0')

    def convert_instrument(self, instrument):
        if instrument.endswith(".P"):
            instrument = instrument[:-2]
        for stablecoin in ["USDT", "USDC", "USD"]:
            if instrument.endswith(stablecoin):
                return instrument.replace(stablecoin, f"-{stablecoin}")
        return instrument

    def get_current_price(self, inst_id):
        try:
            order_book = self.market_api.get_orderbook(instId=inst_id, sz=1)
            if "code" in order_book and order_book["code"] == "0":
                return float(order_book["data"][0]["asks"][0][0])
        except Exception as e:
            logging.error(f"Failed to fetch current price: {e}")
        return 0

    """
    交易数量，表示要购买或者出售的数量。
    当币币/币币杠杆以限价买入和卖出时，指交易货币数量。
    当币币杠杆以市价买入时，指计价货币的数量。
    当币币杠杆以市价卖出时，指交易货币的数量。
    对于币币市价单，单位由 tgtCcy 决定
    当交割、永续、期权买入和卖出时，指合约张数。 
     """
    def execute_spot_trade(self, signal_token, instrument, current_price, message):
        for config in spot_config:
            if (config["exchange"] == EXCHANGE_OKX and
                config["signalToken"] == signal_token and
                config["instrument"] == instrument):
                action = message.get("action")
                size = message.get("amount") #交易货币的数量，来源于信号
                #size = config["size"] #来源于配置
                tgtCcy = "base_ccy" #交易货币（例如ETH、BTC）
                side = "buy" if action == "buy" else "sell"
                #if side=="buy":
                #   size = size * current_price
                #    tgtCcy = ""
                #else:

                logging.info(f"Preparing SPOT trade: {instrument}, side: {side}, size: {size}, price: {current_price}")
                try:
                    response = self.trade_api.place_order(
                        instId=instrument,
                        tdMode="cash",
                        side=side,
                        ordType="market",
                        sz=size,
                        tgtCcy = tgtCcy
                    )
                    logging.info(f"SPOT trade executed successfully: {response}")
                    if response and response.get('code') == '0':
                        try:
                            ordId = response['data'][0]['ordId']
                            logging.info(f"Waiting 1 second before querying order details for ordId: {ordId}")
                            time.sleep(1)
                            order_details = self.trade_api.get_order(instId=instrument, ordId=ordId)
                            logging.info(f"SPOT trade order details: {order_details}")
                        except Exception as e:
                            logging.error(f"Error querying SPOT order details: {e}")
                except Exception as e:
                    logging.error(f"Error executing SPOT trade: {e}")

    def execute_margin_trade(self, signal_token, instrument, current_price, message):
        for config in margin_config:
            if (config["exchange"] == EXCHANGE_OKX and
                config["signalToken"] == signal_token and
                config["instrument"] == instrument):
                action = message.get("action")
                # 市价买入时，为计价货币的数量，市价卖出时，为交易货币数量
                size = message.get("amount")#交易数量（交易货币的数量）
                td_mode = config["tdMode"]
                side = "buy" if action == "buy" else "sell"
                if side=="buy":
                    #市价买入时，为计价货币的数量，市价卖出时
                    size = float(size) * current_price

                logging.info(f"Preparing MARGIN trade: {instrument}, side: {side}, size: {size}, mode: {td_mode}, price: {current_price}")
                try:
                    response = self.trade_api.place_order(
                        instId=instrument,
                        tdMode=td_mode,
                        side=side,
                        ordType="market",
                        sz=size
                        #reduceOnly=True
                    )
                    logging.info(f"MARGIN trade executed successfully: {response}")
                    if response and response.get('code') == '0':
                        try:
                            ordId = response['data'][0]['ordId']
                            logging.info(f"Waiting 1 second before querying order details for ordId: {ordId}")
                            time.sleep(1)
                            order_details = self.trade_api.get_order(instId=instrument, ordId=ordId)
                            logging.info(f"MARGIN trade order details: {order_details}")
                        except Exception as e:
                            logging.error(f"Error querying MARGIN order details: {e}")

                except Exception as e:
                    logging.error(f"Error executing MARGIN trade: {e}")

    def execute_swap_trade(self, signal_token, instrument, current_price, message):
        for config in swap_config:
            if (config["exchange"] == EXCHANGE_OKX and
                config["signalToken"] == signal_token and
                config["instrument"] == instrument):
                action = message.get("action")
                size = config["size"]
                marketPosition = message.get("marketPosition")
                prevMarketPosition = message.get("prevMarketPosition")
                pos_side = "long" if action == "buy" else "short"

                # posSide = "long"
                # if action == "buy":
                #     if marketPosition == "long":
                #         # 开多单
                #         posSide = "long"
                #     if marketPosition == "short" or marketPosition == "flat":
                #         # 平空单
                #         posSide = "short"
                #
                # if action == "sell":
                #     if marketPosition == "short":
                #         # 开空单
                #         posSide = "short"
                #         pass
                #     if marketPosition == "long" or marketPosition == "flat":
                #         # 平多单
                #         posSide = "long"
                #         pass

                logging.info(f"Preparing SWAP trade: {instrument}, action: {action}, posSide: {pos_side}, size: {size}, price: {current_price}")
                try:
                    response = self.trade_api.place_order(
                        instId=f"{instrument}-SWAP",
                        tdMode="cross",
                        side=action,
                        ordType="market",
                        sz=size,
                        posSide=pos_side
                    )
                    logging.info(f"SWAP trade executed successfully: {response}")
                    if response and response.get('code') == '0':
                        try:
                            ordId = response['data'][0]['ordId']
                            instId = f"{instrument}-SWAP"
                            logging.info(f"Waiting 1 second before querying order details for ordId: {ordId}")
                            time.sleep(1)
                            order_details = self.trade_api.get_order(instId=instId, ordId=ordId)
                            logging.info(f"SWAP trade order details: {order_details}")
                        except Exception as e:
                            logging.error(f"Error querying SWAP order details: {e}")
                except Exception as e:
                    logging.error(f"Error executing SWAP trade: {e}")

    def process_trade_message(self, message):
        signal_token = message.get("signalToken")
        instrument = self.convert_instrument(message.get("instrument"))
        action = message.get("action")

        try:
            current_price = self.get_current_price(instrument)
        except Exception as e:
            logging.error(f"Error fetching price for {instrument}: {e}")
            return

        logging.info(f"Processing trade message: {message}")

        self.execute_spot_trade(signal_token, instrument, current_price, message)
        self.execute_margin_trade(signal_token, instrument, current_price, message)
        self.execute_swap_trade(signal_token, instrument, current_price, message)


# 配置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建日志目录
os.makedirs('logs', exist_ok=True)

handler = TimedRotatingFileHandler(
    filename=os.path.join('logs', 'okx_trade_log.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)