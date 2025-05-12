from okx import Trade

apiKey = "a0e09b8d-defd-4162-86c1-d814f8ec8b53"
secretKey = "537374F30510C3F957D4A13AB229E2D5"
passphrase = "milkyllx7353454A!"

tradeApi = Trade.TradeAPI(apiKey, secretKey, passphrase, False, '0')

#期权--OK
result = tradeApi.place_order(
        instId="ETH-USD-250627-2800-C", #期权
        tdMode="isolated", #逐仓
        clOrdId="O20250523005",
        side='buy',
        ordType="limit", #注意：期权不支持市价单
        sz="1", #合约张数
        px="0.033"#委托价格
       )
print(result)
