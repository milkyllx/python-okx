import pymysql
from okx.MarketData import MarketAPI
import time
from config import SPOT_SYMBOLS

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "juxue654321A!",
    "database": "crypto_follow",
    "charset": "utf8"
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def save_kline_data(instId, timeframe, kline_data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for k in kline_data:
                timestamp = int(k[0])
                open_price = float(k[1])
                high_price = float(k[2])
                low_price = float(k[3])
                close_price = float(k[4])
                volume = float(k[5])
                sql_check = "SELECT COUNT(1) FROM spot_kline WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
                cursor.execute(sql_check, (instId, timeframe, timestamp))
                exists = cursor.fetchone()[0]
                if exists:
                    continue

                sql_insert = """
                INSERT INTO spot_kline (inst_id, timeframe, timestamp, open, high, low, close, volume, update_time,data_src)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP,%s)
                """
                cursor.execute(sql_insert, (instId, timeframe, timestamp, open_price, high_price, low_price, close_price, volume,'OKX'))
            conn.commit()
    finally:
        conn.close()


def fetch_all_klines(market_api, instId, timeframe):
    all_klines = []
    after = ''
    limit = 100
    while True:
        data = market_api.get_history_candlesticks(instId=instId, after=after, bar=timeframe, limit=str(limit))
        if not data or 'data' not in data or len(data['data']) == 0:
            break
        klines = data['data']
        all_klines.extend(klines)
        last_ts = klines[-1][0]
        after = str(int(last_ts) + 1)
        if len(klines) < limit:
            break
    return all_klines


def calculate_and_save_sma200(instId, timeframe='1D'):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_select = """
            SELECT timestamp, close FROM spot_kline
            WHERE inst_id=%s AND timeframe=%s
            ORDER BY timestamp ASC
            """
            cursor.execute(sql_select, (instId, timeframe))
            rows = cursor.fetchall()

            if len(rows) < 200:
                print(f"{instId} {timeframe} 数据不足200条，无法计算SMA200")
                return

            closes = [row[1] for row in rows]
            timestamps = [row[0] for row in rows]

            sma200_values = []
            for i in range(len(closes)):
                if i < 199:
                    sma200_values.append(None)
                else:
                    sma200 = sum(closes[i-199:i+1]) / 200
                    sma200_values.append(sma200)

            for i in range(len(timestamps)):
                if sma200_values[i] is None:
                    continue
                sql_check = "SELECT COUNT(1) FROM spot_kline WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
                cursor.execute(sql_check, (instId, timeframe, timestamps[i]))
                exists = cursor.fetchone()[0]
                if exists:
                    sql_update = "UPDATE spot_kline SET sma200=%s WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
                    cursor.execute(sql_update, (sma200_values[i], instId, timeframe, timestamps[i]))
                else:
                    sql_insert = "INSERT INTO spot_kline (inst_id, timeframe, timestamp, sma200) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql_insert, (instId, timeframe, timestamps[i], sma200_values[i]))
            conn.commit()
    finally:
        conn.close()

def full_data_fetch():
    api = MarketAPI()
    for symbol in SPOT_SYMBOLS:
        #查询日K
        klines = fetch_all_klines(api, symbol, '1D')
        save_kline_data(symbol, '1D', klines)
        calculate_and_save_sma200(symbol, '1D')
        #查询周K
        weekly_klines = fetch_all_klines(api, symbol, '1W')
        save_kline_data(symbol, '1W', weekly_klines)
        calculate_and_save_sma200(symbol, '1W')

if __name__ == '__main__':
    full_data_fetch()