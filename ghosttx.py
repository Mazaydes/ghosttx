import requests
from .utils import is_suspicious_tx

ETHERSCAN_API_URL = "https://api.etherscan.io/api"

class GhostTxScanner:
    def __init__(self, api_key, address=None):
        self.api_key = api_key
        self.address = address

    def fetch_transactions(self):
        params = {
            "module": "account",
            "action": "txlist",
            "apikey": self.api_key,
            "sort": "desc",
        }

        if self.address:
            params["address"] = self.address
        else:
            raise ValueError("Address must be specified")

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data["status"] != "1":
            raise Exception("Failed to fetch transactions.")

        return data["result"]

    def scan(self):
        txs = self.fetch_transactions()
        ghost_txs = [tx for tx in txs if is_suspicious_tx(tx)]
        return ghost_txs
