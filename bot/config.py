# OKX API配置
API_KEY = "6740dd2c-4633-42e4-bfa4-dc88017f2bb6"
SECRET_KEY = "F488131492F1A58B67285BAAC9FE7517"
PASSPHRASE = "milkyllx7353454A!"

'''
apikey = "6740dd2c-4633-42e4-bfa4-dc88017f2bb6"
secretkey = "F488131492F1A58B67285BAAC9FE7517"
IP = ""
备注名 = "跟单0612"
权限 = "读取/交易"
 '''

# 邮箱配置
EMAIL = "616494197@qq.com"
PASSWORD = "rmxvzxhozscwbcfe"
IMAP_SERVER = "imap.qq.com"

#配置
TELEGRAM_BOT_TOKEN = "7561392980:AAFPoY-Y9oq3braE_noH0xnug6azBTGozBQ"
TELEGRAM_CHAT_ID = "-4879047817"

#现货交易配置
spot_config = [
    {
        "exchange": "OKX",
        "signalToken": "SPOT-RSI-STRATEGY",
        "instrument": "ETH-USDT",
        # "size": 10,   #买入金额10USDT
        "enableSl": False, #启用初始止损
        "enableTp": False  #开启止盈
    },
    # {
    #     "exchange": "OKX",
    #     "signalToken":"RSI-STRATEGY-20250530",
    #     "instrument": "ETH-USDT",
    #     "size": 10,  # 买入金额10USDT
    #     "enableSl": False,  # 启用初始止损
    #     "enableTp": False  # 开启止盈
    # }
]

#杠杆交易配置
margin_config = [
    {
        "exchange": "OKX", #OKX,BITGET,BINANCE
        "signalToken": "MARGIN-STRATEGY",
        "instrument": "UNI-USDT",
        #"size":10,  #数量来源于信号
        "tdMode": "isolated",#逐仓isolated,全仓cross
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    {
        "exchange": "OKX",  # OKX,BITGET,BINANCE
        "signalToken": "MARGIN-STRATEGY",
        "instrument": "APT-USDT",
        #"size": 10,  #数量来源于信号
        "tdMode": "isolated",  # 逐仓isolated,全仓cross
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    {
        "exchange": "OKX",  # OKX,BITGET,BINANCE
        "signalToken": "MARGIN-STRATEGY",
        "instrument": "SUI-USDT",
        "tdMode": "isolated",  # 逐仓isolated,全仓cross
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    # {
    #"exchange": "OKX", #OKX,BITGET,BINANCE
    #     "signalToken": "RSI-STRATEGY-20250530",
    #     "instrument": "ADA-USDT",
    #     "size": 10,  #数量来源于信号
    #     "tdMode": "cross",  # 逐仓isolated,全仓cross
    #     "enableSl": False,  # 启用初始止损
    #     "enableTp": False  # 开启止盈
    # }
]

#合约交易配置
"""
"exchange": "OKX", #OKX,BITGET,BINANCE 
"signalToken": "RSI-STRATEGY-20250530"
#对于OKX：现货为BTC-USDT,合约为BTC-USDT-SWAP
#对于BITGET，现货和合约都是BTCUSDT 
"instrument": "BTC-USDT",#BTC-USDT-SWAP
"timeframe": 60,  # 时间框架(分钟)
 
#对于OKX，size为合约张数；
#对于BITGET，size为基础代币数量 
"size": 1,  

#tdMode仓位模式
#OKX取值: 逐仓isolated, 全仓cross; 
#BITGET取值: 逐仓isolated，全仓crossed
"tdMode": "isolated", 
"enableSl": False,  # 启用初始止损
"enableTp": False  # 开启止盈
"""

swap_config = [
    # {
    #     "exchange": "BITGET", #OKX,BITGET,BINANCE
    #     "signalToken": "SWAP-BB200-RSI-STRATEGY",
    #     "instrument": "XRPUSDT",  #
    #     "size": 5,  # 基础代币数量
    #     "tdMode": "crossed",  # BITGET: 仓位模式isolated: 逐仓 crossed: 全仓
    #     "enableSl": False,  # 启用初始止损
    #     "enableTp": False  # 开启止盈
    # },
    # {
    #     "exchange": "BITGET", #OKX,BITGET,BINANCE
    #     "signalToken": "SWAP-BB200-RSI-STRATEGY",
    #     "instrument": "ADAUSDT",  #
    #     "size": 10,  # 基础代币数量，10个ADA,忽略
    #     "tdMode": "crossed",  # # 仓位模式isolated: 逐仓 crossed: 全仓
    #     "enableSl": False,  # 启用初始止损
    #     "enableTp": False  # 开启止盈
    # },
    {
        "exchange": "BITGET", #OKX,BITGET,BINANCE
        "signalToken": "BITGET-SWAP-STRATEGY",
        "instrument": "ETHUSDT",  #
        "size": 0.01,  # 基础代币数量
        "tdMode": "crossed",  # BITGET: 仓位模式isolated: 逐仓 crossed: 全仓
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    {
        "exchange": "BITGET",  # OKX,BITGET,BINANCE
        "signalToken": "BITGET-SWAP-STRATEGY",
        "instrument": "ADAUSDT",  #
        "size": 10,  # 基础代币数量
        "tdMode": "crossed",  # BITGET: 仓位模式isolated: 逐仓 crossed: 全仓
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    {#OKX合约带单
        "exchange": "OKX", #OKX,BITGET,BINANCE
        "signalToken": "SWAP-FOLLOW-STRATEGY",
        "instrument": "SOL-USDT",  # DOGE-USDT-SWAP
        "size": 0.1,  # 合约张数
        "tdMode": "cross",  # 逐仓isolated,全仓cross
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    {#OKX合约带单
        "exchange": "OKX", #OKX,BITGET,BINANCE
        "signalToken": "SWAP-FOLLOW-STRATEGY",
        "instrument": "ETH-USDT",  # ETH-USDT-SWAP
        "size": 0.1,  # 合约张数
        "tdMode": "cross",  # 逐仓isolated,全仓cross
        "enableSl": False,  # 启用初始止损
        "enableTp": False  # 开启止盈
    },
    # {
    #     "exchange": "BINANCE",  # OKX,BITGET,BINANCE
    #     "signalToken": "SWAP-BB200-RSI-STRATEGY",
    #     "instrument": "SOLUSDT",  #
    #     "size": 0.1,  # 合约张数
    #     "enableSl": False,  # 启用初始止损
    #     "enableTp": False  # 开启止盈
    # }
]

#期权交易配置
option_config = [
    # {
    #     "signalToken": "OPTION-ETH-20250529001",
    #     "instrument": "ETH-USDT",
    #     "callAction": [
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250530-2800-C",
    #             #定义有效价格区间：2750<=当前价格<=2850
    #             "top_price": 2850, #当前价格<=2850
    #             "low_price": 2750, #当前价格>=2750
    #             "size": 1
    #         },
    #         {
    #             "enable": True,
    #
    #             "instId": "ETH-USD-250530-2700-C",
    #             "top_price": 2750,
    #             "low_price": 2650,
    #             "size": 1
    #         },
    #         {
    #             "enable": True,
    #
    #             "instId": "ETH-USD-250530-2600-C",
    #             "top_price": 2650,
    #             "low_price": 2550,
    #             "size": 1
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250530-2500-C",
    #             "top_price": 2550,
    #             "low_price": 2450,
    #             "size": 1
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250530-2500-C",
    #             "top_price": 2550,
    #             "low_price": 2450,
    #             "size": 2,
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250627-2800-C",
    #             "top_price": 2850,
    #             "low_price": 2750,
    #             "size": 1,
    #             #
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250627-2700-C",
    #             "top_price": 2750,
    #             "low_price": 2650,
    #             "size": 1,
    #             #
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250627-2600-C",
    #             "top_price": 2650,
    #             "low_price": 2550,
    #             "size": 2,
    #             #
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250725-2800-C",
    #             "top_price": 2800,
    #             "low_price": 2700,
    #             "size": 1,
    #             #
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250725-2700-C",
    #             "top_price": 2700,
    #             "low_price": 2600,
    #             "size": 1,
    #             #
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250725-2600-C",
    #             "top_price": 2600,
    #             "low_price": 2500,
    #             "size": 1,
    #             #
    #         }
    #
    #     ],
    #     "putActions": [
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250530-2800-P",
    #             # 定义有效价格区间：2850<=当前价格<=2750
    #             "top_price": 2850,
    #             "low_price": 2750,
    #             "size": 1
    #         },
    #         {
    #             "enable": True,
    #             "instId": "ETH-USD-250530-2700-P",
    #             # 定义有效价格区间：2650<=当前价格<=2750
    #             "top_price": 2750,
    #             "low_price": 2650,
    #             "size": 1
    #         },
    #
    #     ]
    # },
    #
    # {
    #     "signalToken": "001002",
    #     "instrument": "BTC-USDT",
    #     "callAction": [
    #         {
    #             "enable": True,
    #             "InstId": "BTC-USD-250530-110000-C",
    #             # 定义有效价格区间：105000<=当前价格<=115000
    #             "top_price": 115000,  #
    #             "low_price": 105000,  #
    #             "size": 1
    #         },
    #     ],
    #     "putActions": [
    #         {
    #             "enable": True,
    #             "InstId": "BTC-USD-250530-110000-P",
    #             # 定义有效价格区间：115000<=当前价格<=105000
    #             "top_price": 115000,
    #             "low_price": 105000,
    #             "size": 1
    #         },
    #
    #     ]
    # }
]
