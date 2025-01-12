import requests
import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class Solana:
    def __init__(self):
        self.api_url = settings.BITQUERY_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.BITQUERY_AUTH_TOKEN}'
        }
        logger.info("Solana class initialized with API URL and Authorization Token")

    def fetch_dex_trade_data(self, time_ago, symbols):
        payload = json.dumps({
            "query": """
                query ($time_ago: DateTime, $symbols: [String!]) {
                  Solana {
                    DEXTradeByTokens(
                      where: {
                        Transaction: {Result: {Success: true}},
                        Block: {Time: {after: $time_ago}},
                        Trade: {Currency: {Symbol: {in: $symbols}}}
                      }
                      orderBy: {descendingByField: "usd"}
                    ) {
                      Trade {
                        price_last: PriceInUSD(maximum: Block_Slot)
                      }
                      dexes: uniq(of: Trade_Dex_ProgramAddress)
                      amount: sum(of: Trade_Side_Amount)
                      usd: sum(of: Trade_Side_AmountInUSD)
                      traders: uniq(of: Trade_Account_Owner)
                    }
                  }
                }
            """,
            "variables": {
                "time_ago": time_ago,
                "symbols": symbols
            }
        })

        try:
            logger.info(f"Sending request to {self.api_url} for symbols: {symbols} and time_ago: {time_ago}")
            response = requests.post(self.api_url, headers=self.headers, data=payload)
            response.raise_for_status()
            data = response.json()
            if 'data' in data and data['data']['Solana']['DEXTradeByTokens']:
                price = data['data']['Solana']['DEXTradeByTokens'][0]['Trade']['price_last']
                logger.info(f"Received price: {price}")
                return price
            else:
                logger.warning(f"No data found for symbols: {symbols} and time_ago: {time_ago}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during API request: {e}")
            return None
        except KeyError as e:
            logger.error(f"Error in response structure: Missing key {e}")
            return None
