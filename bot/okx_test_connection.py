from okx import Trade, MarketData

api_key = "6740dd2c-4633-42e4-bfa4-dc88017f2bb6"
secret_key = "F488131492F1A58B67285BAAC9FE7517"
passphrase = "milkyllx7353454A!"

trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, False, '0')
market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, False, '0')

def get_current_price(inst_id):
    try:
        order_book = market_api.get_orderbook(instId=inst_id, sz=1)
        if "code" in order_book and order_book["code"] == "0":
            price = float(order_book["data"][0]["asks"][0][0])
            print(price)
    except Exception as e:
        print(f"Failed to fetch current price: {e}")
    return 0


if __name__ == "__main__":
    get_current_price("BTC-USDT")
