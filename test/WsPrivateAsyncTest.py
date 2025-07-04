import asyncio

from okx.websocket.WsPrivateAsync import WsPrivateAsync


def privateCallback(message):
    print("privateCallback", message)


async def main():
    url = "wss://ws.okx.com:8443/ws/v5/private"
    ws = WsPrivateAsync(
        apiKey="a0e09b8d-defd-4162-86c1-d814f8ec8b53",
        secretKey="537374F30510C3F957D4A13AB229E2D5",
        passphrase="milkyllx7353454A!",

        url=url,
        useServerTime=False
    )
    await ws.start()
    args = []
    arg1 = {"channel": "account", "ccy": "USDT"}
    arg2 = {"channel": "orders", "instType": "ANY"}
    arg3 = {"channel": "balance_and_position"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    await ws.subscribe(args, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg2]
    await ws.unsubscribe(args2, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg3]
    await ws.unsubscribe(args3, callback=privateCallback)


if __name__ == '__main__':
    asyncio.run(main())
