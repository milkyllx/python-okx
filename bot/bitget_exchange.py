import logging
import bitget.v2.mix.order_api as maxOrderApi
from base_exchange import BaseExchange
from bitget.exceptions import BitgetAPIException
from bot.config import swap_config, spot_config, margin_config
from bot.exchange_config import EXCHANGE_BITGET

# 配置日志
from logging.handlers import TimedRotatingFileHandler
import os

# 确保日志目录存在
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 配置日志处理器
log_file = os.path.join(log_dir, 'bitget_trade_log.log')
handler = TimedRotatingFileHandler(
    filename=log_file,
    when='midnight',  # 每天午夜切换新文件
    interval=1,  # 间隔为1天
    backupCount=30,  # 保留30天的日志文件
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 获取根日志记录器并添加处理器
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class BitgetExchange(BaseExchange):
    def __init__(self, api_key, secret_key, passphrase):
        super().__init__(api_key, secret_key, passphrase)
        self.maxOrderApi = maxOrderApi.OrderApi(self.api_key, self.secret_key, self.passphrase)
        # 初始化Bitget API
        # self.trade_api = ...

    def convert_instrument(self, instrument):
        if instrument.endswith(".P"):
            instrument = instrument[:-2]
        return instrument

    # def place_order(self, message):
    #     instrument = self.convert_instrument(message["instrument"])
    #     print(f"Placing order on BITGET: {instrument}")
    #     # 示例下单逻辑
    #     # try:
    #     #     self.trade_api.place_order(...)
    #     # except Exception as e:
    #     #     print(f"Error placing order on Bitget: {e}")

    def process_trade_message(self, message):
        signal_token = message.get("signalToken")
        tv_instrument = message.get("instrument")
        # 如果是OKX交易所
        instrument = self.convert_instrument(tv_instrument)
        timeframe = message.get("timeframe")
        action = message.get("action")
        is_contract = self.check_perpetual_contract(tv_instrument)

        if is_contract: #永续合约
            self.execute_swap_trade(signal_token,instrument,message)
            pass

        else:
            self.execute_spot_trade(signal_token,instrument,message)
            self.execute_margin_trade(signal_token,instrument,message)
            pass
        pass

    # 执行合约交易
    def execute_swap_trade(self, signal_token, instrument, message):

        for config in swap_config:
            if (config["exchange"] == EXCHANGE_BITGET
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument):
                # and config["timeframe"] == timeframe)\
                #TODO: 来源于配置还是来源于信号？
                # 优先来源于配置
                size = config["size"]  #
                if size <= 0:
                    size = message.get("amount") #代币数量

                td_mode = config["tdMode"] #
                action = message.get("action")
                marketPosition = message.get("marketPosition")
                prevMarketPosition = message.get("prevMarketPosition")

                params = {}
                params["symbol"] = instrument
                params["productType"] = "USDT-FUTURES"  #
                params["marginMode"] = td_mode  # 仓位模式isolated: 逐仓 crossed: 全仓
                params["marginCoin"] = "USDT"  # 保证金币种 USDT
                params["size"] = size  # 下单数量(基础币数量)
                params["orderType"] = "market"  # 订单类型 limit: 限价单，market: 市价单

                if action == "buy":
                    params["side"] = "buy"  # 交易方向 buy: 单向持仓时代表买入，双向持仓时代表多头方向 sell: 单向持仓时代表卖出，双向持仓时代表空头方向

                    if marketPosition == "long":
                        # 开多单
                        params["tradeSide"] = "open"  # 交易类型(仅限双向持仓)双向持仓模式下必填，单向持仓时不要填，否则会报错 open: 开仓 close: 平仓
                    if marketPosition == "short" or marketPosition == "flat":
                        # 平空单
                        params["tradeSide"] = "close"
                if action == "sell":
                    params["side"] = "sell"

                    if marketPosition == "short":
                        # 开空单
                        params["tradeSide"] = "open"
                    if marketPosition == "long" or marketPosition == "flat":
                        # 平多单
                        params["tradeSide"] = "close"
                tradeSide = params["tradeSide"]
                logging.info(f"Executing SWAP trade: {instrument}, side:{action}, tradeSide: {tradeSide},size: {size}, mode: {td_mode}")
                try:
                    # params[\"clientOid\"] = \"\"
                    response = self.maxOrderApi.placeOrder(params)
                    logging.info(f"SWAP trade executed successfully: {response}")
                except BitgetAPIException as e:
                    logging.error(f"Error executing SWAP trade: {e.message}")


    #执行现货交易
    def execute_spot_trade(self, signal_token, instrument, message):
        for config in spot_config:
            if (config["exchange"] == EXCHANGE_BITGET
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument) :
                size = config["size"]
                logging.info(f"Executing SPOT trade: {instrument}, size: {size}")
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
    def execute_margin_trade(self,signal_token, instrument, timeframe, current_price):
        for config in margin_config:
            if (config["exchange"] == EXCHANGE_BITGET
                    and config["signalToken"] == signal_token
                    and config["instrument"] == instrument):
                size = config["size"]
                td_mode = config["tdMode"]
                logging.info(
                    f"Executing MARGIN trade: {instrument}, size: {size}, mode: {td_mode}")
                    # 调用杠杆交易API
                    # try:
                    #     tradeApi.place_order(instId=instrument, tdMode=td_mode, side="buy", ordType="market", sz=size)
                    # except Exception as e:
                    #     print(f"Error executing MARGIN trade: {e}")
        pass