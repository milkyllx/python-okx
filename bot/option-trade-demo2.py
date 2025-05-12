import imaplib
import email
import json
from datetime import datetime, timedelta
from okx import Trade, MarketData
from config import option_config, API_KEY, SECRET_KEY, PASSPHRASE, IMAP_SERVER, EMAIL, PASSWORD  # 导入配置

# 初始化 OKX API
tradeApi = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
marketApi = MarketData.MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

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

        # 获取最多100封未读邮件
        email_ids = messages[0].split()[:10]
        result = []

        for num in email_ids:
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # 检查邮件发件人是否是 @tradingview.com
                    from_address = msg.get("From")
                    print("Email from: " + from_address)

                    # 打印邮件接收时间
                    date_header = msg.get("Date")
                    print("Email received at: " + date_header)

                    if "@tradingview.com" not in from_address:
                        continue

                    # 检查邮件是否是纯文本格式
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True).decode()
                                try:
                                    email_data = json.loads(payload)
                                    # 验证 JSON 格式是否包含必要字段
                                    if validate_email_content(email_data):
                                        result.append(email_data)
                                    else:
                                        print("Invalid email content: Missing required fields.")
                                except json.JSONDecodeError:
                                    print("Invalid JSON format in email.")
                    else:
                        if msg.get_content_type() == "text/plain":
                            payload = msg.get_payload(decode=True).decode()
                            print("Email Content: " + payload)
                            try:
                                email_data = json.loads(payload)
                                # 验证 JSON 格式是否包含必要字段
                                if validate_email_content(email_data):
                                    result.append(email_data)
                                else:
                                    print("Invalid email content: Missing required fields.")
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
    # 检查是否为永续合约交易对，例如 BTCUSDT.P
    if tv_instrument.endswith(".P"):
        # 去掉 .P 后缀
        tv_instrument = tv_instrument[:-2]

    # 支持 USDT、USDC、USD 结尾的交易对
    for stablecoin in ["USDT", "USDC", "USD"]:
        if tv_instrument.endswith(stablecoin):
            return tv_instrument.replace(stablecoin, f"-{stablecoin}")

    # 如果不匹配上述规则，返回原始值
    return tv_instrument



# 获取当前价格
def get_current_price(instId):
    order_book = marketApi.get_orderbook(instId=instId, sz=1)
    if "code" in order_book and order_book["code"] == "0":
        return float(order_book["data"][0]["asks"][0][0])  # 卖一价
    raise Exception("Failed to fetch current price")


# 查询最优买入价格
def get_best_bid_price(instId):
    # 调用订单簿API获取数据
    order_book = marketApi.get_orderbook(instId=instId, sz=5)  # 获取前5档挂单
    if order_book.get("code") == "0" and order_book.get("data"):
        # 提取bids数据
        bids = order_book["data"][0]["bids"]
        if bids:
            best_bid = float(bids[0][0])  # 获取买一价
            return best_bid
        else:
            raise Exception("订单簿中没有买单数据")
    else:
        raise Exception(f"订单簿数据获取失败：{order_book.get('msg', '未知错误')}")

# 执行交易
def execute_trade(instId, size):
    # 获取最优买入价格
    best_price = get_best_bid_price(instId)
    # 在最优价格基础上加一档
    price_increment = 0.0005  # 在最优价格基础上加一档
    limit_price = round(best_price + price_increment, 4)  # 保留4位小数
    print(f"最优买入价：{best_price}, 下单价：{limit_price}")
    #下单
    # result = tradeApi.place_order(
    #     instId=instId,
    #     tdMode="isolated",
    #     clOrdId=f"O{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
    #     side="buy",
    #     ordType="limit",
    #     sz=str(size),
    #     px=limit_price  # 示例限价
    # )
    # print(f"Trade result: {result}")
    # return result



# 主程序
def main():
    while True:
        # 轮询邮箱
        messages = poll_email()
        if not messages:
            continue

        for message in messages:
            # 解析报警消息
            action = message.get("action")
            instrument = message.get("instrument")
            signal_token = message.get("signalToken")
            tv_instrument = convert_to_okx_instrument(instrument)
            # 当前市场价格？
            try:
                current_price = get_current_price(tv_instrument)
            except Exception as e:
                print(f"Error get {tv_instrument} price: {e}")
                continue
            # 查找配置
            #config_item = None
            for config in option_config:
                config_instrument = config.get("instrument")

                #if config.get("signalToken") == signal_token and instrument == config_instrument:
                if tv_instrument == config_instrument:
                    print(f"proceess message: {message}")

                    if action == "buy":
                        for item in config["callAction"]:
                            if item.get("enable"):
                                #config_item = item
                                top_price = item.get("top_price")
                                low_price = item.get("low_price")
                                if top_price >= current_price >= low_price:
                                    #
                                    instId = item.get("instId")
                                    size = item.get("size", 1)
                                    execute_trade(instId, size)

                                #break
                    elif action == "sell":
                        for item in config["putActions"]:
                            if item.get("enable"):
                                # config_item = item
                                top_price = item.get("top_price")
                                low_price = item.get("low_price")
                                if top_price >= current_price >= low_price:
                                    #
                                    instId = item.get("instId")
                                    size = item.get("size", 1)
                                    execute_trade(instId, size)
                    else:
                        pass


if __name__ == "__main__":
    main()
