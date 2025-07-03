import time
import pymysql
from datetime import datetime
from okx.MarketData import MarketAPI

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "crypto_follow",
    "charset": "utf8"
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def save_kline_data(instId, interval, kline_data):
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

                sql_check = "SELECT COUNT(1) FROM okx_kline WHERE instId=%s AND interval=%s AND timestamp=%s"
                cursor.execute(sql_check, (instId, interval, timestamp))
                exists = cursor.fetchone()[0]
                if exists:
                    continue

                sql_insert = """
                INSERT INTO okx_kline (instId, interval, timestamp, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (instId, interval, timestamp, open_price, high_price, low_price, close_price, volume))
            conn.commit()
    finally:
        conn.close()


def calculate_and_save_sma200(instId):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_select = """
            SELECT timestamp, close FROM okx_kline
            WHERE instId=%s AND interval='1W'
            ORDER BY timestamp ASC
            """
            cursor.execute(sql_select, (instId,))
            rows = cursor.fetchall()

            if len(rows) < 200:
                print("周线数据不足200条，无法计算SMA200")
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
                sql_check = "SELECT COUNT(1) FROM okx_sma200 WHERE instId=%s AND timestamp=%s"
                cursor.execute(sql_check, (instId, timestamps[i]))
                exists = cursor.fetchone()[0]
                if exists:
                    sql_update = "UPDATE okx_sma200 SET sma200=%s WHERE instId=%s AND timestamp=%s"
                    cursor.execute(sql_update, (sma200_values[i], instId, timestamps[i]))
                else:
                    sql_insert = "INSERT INTO okx_sma200 (instId, timestamp, sma200) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (instId, timestamps[i], sma200_values[i]))
            conn.commit()
    finally:
        conn.close()


def fetch_all_klines(market_api, instId, interval):
    all_klines = []
    after = ''
    limit = 100
    while True:
        data = market_api.get_history_candlesticks(instId=instId, after=after, bar=interval, limit=str(limit))
        if not data or 'data' not in data or len(data['data']) == 0:
            break
        klines = data['data']
        all_klines.extend(klines)
        last_ts = klines[-1][0]
        after = str(int(last_ts) + 1)
        if len(klines) < limit:
            break
    return all_klines


def scheduled_update(market_api, instId):
    daily_klines = fetch_all_klines(market_api, instId, '1D')
    save_kline_data(instId, '1D', daily_klines)

    weekly_klines = fetch_all_klines(market_api, instId, '1W')
    save_kline_data(instId, '1W', weekly_klines)

    calculate_and_save_sma200(instId)


if __name__ == '__main__':
    api = MarketAPI()
    symbol_instId = 'BTC-USD-SWAP'

    while True:
        try:
            scheduled_update(api, symbol_instId)
            print(f"{datetime.now()} - 数据更新完成")
        except Exception as e:
            print(f"更新出错: {e}")
        time.sleep(3600)