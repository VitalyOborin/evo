from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv
import json

load_dotenv()

session = HTTP(
    testnet=False,
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
)


balance = session.get_wallet_balance(accountType="UNIFIED")
print(json.dumps(balance, ensure_ascii=False, indent=4))