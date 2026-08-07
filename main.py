import os

from veri import get_data
from strateji import analiz_et
from telegram_bot import send_message


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def main():
    print("XAU AI SIGNAL BOT")
    print("Bot baslatildi...")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN bulunamadi.")

    if not CHAT_ID:
        raise ValueError("CHAT_ID bulunamadi.")

    try:
        data = get_data()

        if data is None or data.empty:
            print("Veri alinamadi.")
            return

        prices = data["close"].tolist()

        result = analiz_et(prices)

        print("Signal:", result["signal"])
        print("Score:", result["score"])
        print("Reason:", result["reason"])

        if result["signal"] in ["BUY", "SELL"]:
            message = (
                "XAUUSD SIGNAL\n\n"
                f"Signal: {result['signal']}\n"
                f"Score: {result['score']}\n"
                f"Reason: {result['reason']}"
            )

            send_message(
                BOT_TOKEN,
                CHAT_ID,
                message
            )

            print("Telegram message sent.")

        else:
            print("No strong signal.")

    except Exception as e:
        print("ERROR:", str(e))
        raise


if __name__ == "__main__":
    main()
