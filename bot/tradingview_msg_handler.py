import imaplib
import email
import json
from datetime import datetime

import requests

from okx import Trade, MarketData
from config import option_config, API_KEY, SECRET_KEY, PASSPHRASE, IMAP_SERVER, EMAIL, PASSWORD, TELEGRAM_BOT_TOKEN, \
    TELEGRAM_CHAT_ID, margin_config, swap_config, spot_config

# 初始化 OKX API
tradeApi = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
marketApi = MarketData.MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

# 发送消息到 Telegram
def send_to_telegram(message):
    try:
        # Telegram API URL
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        # 请求参数
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"  # 支持 HTML 格式化
        }

        # 发起 POST 请求
        response = requests.post(url, json=payload)

        # 打印调试信息
        print(f"Request URL: {url}")
        print(f"Payload: {payload}")
        print(f"Response: {response.text}")

        # 检查响应状态
        if response.status_code == 200:
            print(f"Message sent to Telegram successfully: {message}")
        else:
            print(f"Failed to send message to Telegram. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

# 发送消息到 Twitter (X)
def send_to_x(message):
    try:
        # TODO: 根据实际需求实现 Twitter 消息发送逻辑
        print(f"Sending message to Twitter (X): {message}")
    except Exception as e:
        print(f"Error sending to Twitter (X): {e}")

# 轮询邮箱
def poll_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")

        if status != "OK":
            print("No new messages.")
            return []

        email_ids = messages[0].split()[:10]
        result = []

        for num in email_ids:
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_address = msg.get("From")
                    date_header = msg.get("Date")
                    print(f"Email from: {from_address}, received at: {date_header}")

                    if "@tradingview.com" not in from_address:
                        continue

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True).decode()
                                try:
                                    email_data = json.loads(payload)
                                    if validate_email_content(email_data):
                                        result.append(email_data)
                                except json.JSONDecodeError:
                                    print("Invalid JSON format in email.")
                    else:
                        if msg.get_content_type() == "text/plain":
                            payload = msg.get_payload(decode=True).decode()
                            try:
                                email_data = json.loads(payload)
                                if validate_email_content(email_data):
                                    result.append(email_data)
                            except json.JSONDecodeError:
                                print("Invalid JSON format in email.")

            mail.store(num, '+FLAGS', '\\Seen')
        mail.logout()
        return result

    except Exception as e:
        print(f"Error polling email: {e}")
        return []

# 验证邮件内容是否包含必要字段
def validate_email_content(email_data):
    required_fields = ["action", "instrument", "signalToken"]
    return all(field in email_data for field in required_fields)

# 将 TradingView 格式的 instrument 转换为 OKX 格式
def convert_to_okx_instrument(tv_instrument):
    if tv_instrument.endswith(".P"):
        tv_instrument = tv_instrument[:-2]
    for stablecoin in ["USDT", "USDC", "USD"]:
        if tv_instrument.endswith(stablecoin):
            return tv_instrument.replace(stablecoin, f"-{stablecoin}")
    return tv_instrument

# 将 TradingView 格式的 instrument 转换为 BITGET 格式
def convert_to_bitget_instrument(tv_instrument):
    if tv_instrument.endswith(".P"):
        tv_instrument = tv_instrument[:-2]
    # for stablecoin in ["USDT", "USDC", "USD"]:
    #     if tv_instrument.endswith(stablecoin):
    #         return tv_instrument.replace(stablecoin, f"-{stablecoin}")
    return tv_instrument

# 获取当前价格
def get_current_price(instId):
    try:
        order_book = marketApi.get_orderbook(instId=instId, sz=1)

        if "code" in order_book and order_book["code"] == "0":
            return float(order_book["data"][0]["asks"][0][0])
    except Exception as e:
        print(f"Failed to fetch current price: {e}")
        return 0
#是否为合约
def check_perpetual_contract(tv_instrument):
    if tv_instrument.endswith(".P"):
        return True
    return False

# 查询最优买入价格
def get_best_bid_price(instId):
    order_book = marketApi.get_orderbook(instId=instId, sz=5)
    if order_book.get("code") == "0" and order_book.get("data"):
        bids = order_book["data"][0]["bids"]
        if bids:
            return float(bids[0][0])
    raise Exception("Failed to fetch best bid price")

# 执行交易
def execute_trade(instId, size):
    best_price = get_best_bid_price(instId)
    price_increment = 0.0005
    limit_price = round(best_price + price_increment, 4)
    print(f"Best bid price: {best_price}, Order price: {limit_price}")
    # TODO: 添加实际下单逻辑

# 解析 extend 字段
def parse_extend(extend):
    stop_loss_price = "N/A"
    target_prices = ["N/A", "N/A", "N/A"]

    if extend:
        try:
            parts = extend.split(", ")
            for part in parts:
                if "Stop Loss" in part:
                    stop_loss_price = part.split(":")[1].strip()
                elif "Take Profit" in part:
                    target_price = part.split(":")[1].strip()
                    target_prices = [target_price, target_price, target_price]  # 假设 3 个目标价格相同
        except Exception as e:
            print(f"Error parsing extend field: {e}")

    return stop_loss_price, target_prices

# 格式化消息
def format_message(action, instrument, timeframe, price,stop_loss_price, target_prices):
    return f"""
❤️❤️❤️ Trading Signal ❤️❤️❤️ 
🚨Symbol: {instrument}
🚨Timeframe: {timeframe}
🚨Action: {action}
🚨Price: {price} 
🚨Stop loss Price: {stop_loss_price}
🚨Target1 Price: {target_prices[0]}
🚨Target2 Price: {target_prices[1]}
🚨Target3 Price: {target_prices[2]}
"""

# 执行现货交易
def execute_spot_trade(signal_token, instrument, timeframe, current_price):
    for config in spot_config:
        if (config["signalToken"] == signal_token and
                config["instrument"] == instrument and
                config["timeframe"] == timeframe):
            size = config["size"]
            print(f"Executing SPOT trade: {instrument}, size: {size}, price: {current_price}")
            # 调用现货交易API
            try:
                tradeApi.place_order(instId=instrument, tdMode="cash", side="buy", ordType="market", sz=size)
            except Exception as e:
                print(f"Error executing SPOT trade: {e}")

# 执行杠杆交易
def execute_margin_trade(signal_token, instrument, timeframe, current_price):
    for config in margin_config:
        if (config["signalToken"] == signal_token and
                config["instrument"] == instrument and
                config["timeframe"] == timeframe):
            size = config["size"]
            td_mode = config["tdMode"]
            print(f"Executing MARGIN trade: {instrument}, size: {size}, mode: {td_mode}, price: {current_price}")
            # 调用杠杆交易API
            try:
                tradeApi.place_order(instId=instrument, tdMode=td_mode, side="buy", ordType="market", sz=size)
            except Exception as e:
                print(f"Error executing MARGIN trade: {e}")

# 执行合约交易
def execute_swap_trade(signal_token, instrument, timeframe, current_price):
    for config in swap_config:
        if (config["signalToken"] == signal_token and
                config["instrument"] == instrument) :
                #and config["timeframe"] == timeframe)\

            size = config["size"]
            td_mode = config["tdMode"]
            print(f"Executing SWAP trade: {instrument}, size: {size}, mode: {td_mode}, price: {current_price}")
            # 调用合约交易API
            try:
                tradeApi.place_order(instId=f"{instrument}-SWAP", tdMode=td_mode, side="buy", ordType="market", sz=size)
            except Exception as e:
                print(f"Error executing SWAP trade: {e}")

# 执行期权交易
def execute_option_trade(signal_token, instrument, action, current_price):
    for config in option_config:
        if config["signalToken"] == signal_token and config["instrument"] == instrument:
            actions = config["callAction"] if action == "buy" else config["putActions"]
            for option in actions:
                if (option["enable"] and
                        option["low_price"] <= current_price <= option["top_price"]):
                    inst_id = option["instId"]
                    size = option["size"]
                    print(f"Executing OPTION trade: {inst_id}, size: {size}, price: {current_price}")
                    # 调用期权交易API
                    try:
                        tradeApi.place_order(instId=inst_id, tdMode="isolated", side="buy", ordType="market", sz=size)
                    except Exception as e:
                        print(f"Error executing OPTION trade: {e}")

# 主交易处理逻辑
def process_okx_trade_message(message):
    signal_token = message.get("signalToken")
    instrument = message.get("instrument")
    #如果是OKX交易所
    instrument = convert_to_okx_instrument(instrument)

    timeframe = message.get("timeframe")
    action = message.get("action")
    try:
        current_price = get_current_price(instrument)
    except Exception as e:
        print(f"Error fetching price for {instrument}: {e}")
        return

    print(f"Processing trade message: {message}")
    # 执行现货交易
    #execute_spot_trade(signal_token, instrument, timeframe, current_price)
    # 执行杠杆交易
    #execute_margin_trade(signal_token, instrument, timeframe, current_price)
    # 执行合约交易
    execute_swap_trade(signal_token, instrument, timeframe, current_price)
    # 执行期权交易
    # execute_option_trade(signal_token, instrument, action, current_price)

# 处理交易逻辑（买入或卖出）
# def process_action(action, config, current_price):
#     for item in config:
#         if item.get("enable"):
#             top_price = item.get("top_price")
#             low_price = item.get("low_price")
#             if top_price >= current_price >= low_price:
#                 instId = item.get("instId")
#                 size = item.get("size", 1)
#                 execute_trade(instId, size)

def process_bitget_trade_message(message):
    signal_token = message.get("signalToken")
    tv_instrument = message.get("instrument")
    is_contract = check_perpetual_contract(tv_instrument)

    # 如果是OKX交易所
    instrument = convert_to_bitget_instrument(tv_instrument)

    timeframe = message.get("timeframe")
    action = message.get("action")
    if is_contract: #永续合约
        pass
    else:
        pass
    pass

def process_binance_trade_message(message):
    pass

# 主程序
def main():
    while True:
        messages = poll_email()
        if not messages:
            continue

        for message in messages:
            action = message.get("action")
            instrument = message.get("instrument")
            price = message.get("price", "0")
            timeframe = message.get("timeframe", "N/A")
            extend = message.get("extend", "")
            send_to_telegram_flag = message.get("sendToTelegram", "false") == "true"
            send_to_x_flag = message.get("sendToX", "false") == "true"

            # 解析 extend 字段
            stop_loss_price, target_prices = parse_extend(extend)

            # 格式化消息
            formatted_message = format_message(action, instrument, timeframe, price, stop_loss_price, target_prices)

            # 发送消息到 Telegram 和 Twitter
            if send_to_telegram_flag:
                send_to_telegram(formatted_message)
            if send_to_x_flag:
                send_to_x(formatted_message)
            #
            exchange = message.get("exchange")

            if exchange == "OKX":#
                process_okx_trade_message(message)

            elif exchange == "BITGET":#
                process_bitget_trade_message(message)

            elif exchange ==  "BINANCE":#
                process_binance_trade_message(message)

            else:
                pass

if __name__ == "__main__":
    main()
