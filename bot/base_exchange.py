class BaseExchange:
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    # def place_order(self, message):
    #     """下单接口，需要在子类中实现"""
    #     raise NotImplementedError("Subclasses must implement this method")

    # 是否为合约
    def check_perpetual_contract(self, tv_instrument):
        if tv_instrument.endswith(".P"):
            return True
        return False

    def process_trade_message(self, message):
        raise NotImplementedError("Subclasses must implement this method")