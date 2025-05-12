from okx import Trade, MarketData

# API密钥配置
apiKey = "a0e09b8d-defd-4162-86c1-d814f8ec8b53"
secretKey = "537374F30510C3F957D4A13AB229E2D5"
passphrase = "milkyllx7353454A!"

# 初始化交易和市场API
tradeApi = Trade.TradeAPI(apiKey, secretKey, passphrase, False, '0')
marketApi = MarketData.MarketAPI(apiKey, secretKey, passphrase, False, '0')

# 查询最优买入价格
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


# 下单函数
def place_option_order_with_best_price(instId, tdMode, clOrdId, side, ordType, sz, price_increment):
    try:
        # 获取最优买入价格
        best_price = get_best_bid_price(instId)
        # 在最优价格基础上加一档
        limit_price = round(best_price + price_increment, 4)  # 保留6位小数
        print(f"最优买入价：{best_price}, 下单价：{limit_price}")

        # 下单
        # result = tradeApi.place_order(
        #     instId=instId,
        #     tdMode=tdMode,
        #     clOrdId=clOrdId,
        #     side=side,
        #     ordType=ordType,
        #     sz=sz,
        #     px=str(limit_price)  # 限价
        # )
        # return result
    except Exception as e:
        print(f"下单失败：{e}")
        return None

# 示例调用
if __name__ == "__main__":
    instId = "ETH-USD-250725-2800-C"  # 期权合约ID
    tdMode = "isolated"  # 逐仓模式
    clOrdId = "O20250523005"  # 自定义订单ID
    side = "buy"  # 买入
    ordType = "limit"  # 限价单
    sz = "1"  # 合约张数
    price_increment = 0.0005  # 在最优价格基础上加一档

    # 下单
    result = place_option_order_with_best_price(instId, tdMode, clOrdId, side, ordType, sz, price_increment)
    print(result)
