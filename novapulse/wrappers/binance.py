import binance
from binance import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Binance:

    BASE_CURRENCY = "USDC"

    def __init__(self):
        self.api_key = settings.BINANCE_API_KEY
        self.api_secret = settings.BINANCE_SECRET
        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.exchange_info = None
        self.currency_pairs = None
        self.currencies = None
        self.prices = dict()
        logger.info("Binance client initialized")

    def get_exchange_info(self):
        try:
            logger.info("Fetching exchange info from Binance API")
            self.exchange_info = self.client.get_exchange_info()
            self.currency_pairs = [symbol['symbol'] for symbol in self.exchange_info['symbols'] if self.BASE_CURRENCY in symbol['symbol']]
            self.currencies = [pair.replace(self.BASE_CURRENCY, '') for pair in self.currency_pairs if self.BASE_CURRENCY in pair]
            logger.info(f"Currency pairs found: {self.currency_pairs}")
            return self.currency_pairs
        except Exception as e:
            logger.error(f"Error fetching exchange info: {str(e)}")
            return []

    def get_prices(self):
        logger.info("Fetching prices for currency pairs")
        for pair in self.currency_pairs:
            try:
                ticker = self.client.get_ticker(symbol=pair)
                self.prices[pair] = float(ticker['lastPrice'])
                logger.info(f"Price for {pair}: {self.prices[pair]}")
            except binance.exceptions.BinanceAPIException as exc:
                logger.error(f"Error fetching price for {pair}: {exc}")
        return self.prices

    def get_price(self, currency_pair):
        try:
            logger.info(f"Fetching price for {currency_pair}")
            ticker = self.client.get_ticker(symbol=currency_pair)
            price = float(ticker['lastPrice'])
            logger.info(f"Price for {currency_pair}: {price}")
            return price
        except binance.exceptions.BinanceAPIException as exc:
            logger.error(f"Error fetching price for {currency_pair}: {exc}")
            return None

    def get_trade_fee(self, currency_pair):
        trade_fee = self.client.get_trade_fee(symbol=currency_pair)
        if trade_fee and trade_fee[0]:
            trade_fee = trade_fee[0]
            maker_fee = float(trade_fee['makerCommission'])
            taker_fee = float(trade_fee['takerCommission'])
            return maker_fee + taker_fee
        return None
