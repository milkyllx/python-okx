from datetime import datetime  # 引入 datetime 模块
import email
import imaplib
import json
import time

from bot.config import EMAIL, PASSWORD, IMAP_SERVER
from exchange_router import ExchangeRouter
from exchange_config import config

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

        email_ids = messages[0].split()[:10]
        result = []

        for num in email_ids:
            status, msg_data = mail.fetch(num, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_address = msg.get("From")
                    date_header = msg.get("Date")
                    print(f"Email from: {from_address}, received at: {date_header}")

                    if "@tradingview.com" not in from_address:
                        continue

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                payload = part.get_payload(decode=True).decode()
                                try:
                                    email_data = json.loads(payload)
                                    if validate_email_content(email_data):
                                        result.append(email_data)
                                except json.JSONDecodeError:
                                    print("Invalid JSON format in email.")
                    else:
                        if msg.get_content_type() == "text/plain":
                            payload = msg.get_payload(decode=True).decode()
                            try:
                                email_data = json.loads(payload)
                                if validate_email_content(email_data):
                                    result.append(email_data)
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

def main():
    router = ExchangeRouter(config)

    while True:
        messages = poll_email()
        if not messages:
            # 获取当前时间并格式化为 yyyy-MM-dd hh:mm:ss 格式
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"时间：{current_time} >> 没有新的报警消息，暂停5秒...... ")
            time.sleep(5)  # 暂停 5 秒
            continue
        # 打印当前时间和新的消息数
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"时间：{current_time} >> 收到新的报警消息数量：{len(messages)}")
        for message in messages:
            router.route_message(message)

if __name__ == "__main__":
    main()
