from bot.config import API_KEY, SECRET_KEY, PASSPHRASE
from okx import Trade

tradeApi = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
#永续合约--OK
# result = tradeApi.place_order(
#         instId="SUI-USDT-SWAP",
#         tdMode="isolated",
#         clOrdId="O20250523001",
#         side='buy',
#         posSide="long",
#         ordType="market",
#         sz="1" #合约张数
#        )
# print(result)

#现货--OK
# result = tradeApi.place_order(
#         instId="SUI-USDT",
#         tdMode="spot_isolated", #现货 现货带单时：spot_isolated
#         clOrdId="O20250612003",
#         side='buy',
#         ordType="market",
#         sz="5" #交易金额（USDT)
#         )
# print(result)

#现货--OK
# result = tradeApi.place_order(
#         instId="SUI-USDT",
#         tdMode="cash",
#         side='buy',
#         clOrdId="O20250625001",
#         ordType="market",
#         sz="1", #交易金额（SUI)
#         tgtCcy="base_ccy"#交易货币
#         )
# print(result)

#现货--OK
# result = tradeApi.place_order(
#         instId="SUI-USDT",
#         tdMode="cash",
#         side='buy',
#         clOrdId="O20250625002",
#         ordType="market",
#         sz="3", #交易金额（USDT)
#         tgtCcy="quote_ccy"#计价货币（USDT）
#         )
# print(result)

# result = tradeApi.place_order(
#         instId="SUI-USDT",
#         tdMode="cash",
#         side='sell',
#         clOrdId="O20250625003",
#         ordType="market",
#         sz="3", #交易金额（USDT)
#         tgtCcy="quote_ccy"#计价货币（USDT）
#         )
# print(result)

# result = tradeApi.place_order(
#         instId="SUI-USDT",
#         tdMode="cash",
#         side='sell',
#         clOrdId="O20250625004",
#         ordType="market",
#         sz="1", #交易金额（SUI)
#         tgtCcy="base_ccy"#计价货币（SUI）
#         )
# print(result)

#现货杠杆--OK
result = tradeApi.place_order(
        instId="SUI-USDT",
        tdMode="isolated", #逐仓
        clOrdId="O20250627001",
        side='buy',
        ordType="market",
        sz="5" #交易金额（USDT)
        )
print(result)


