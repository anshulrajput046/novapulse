import logging
from datetime import timedelta

from django.utils.timezone import now

from apps.arbitrage_scanner.models.arbitrage_opportunity import ArbitrageOpportunity
from wrappers.binance import Binance
from wrappers.solana import Solana

logger = logging.getLogger(__name__)


class ArbitrageScanner:
    BINANCE_FEE = 0.001
    SOLANA_SWAP_FEE = 0.003
    TRANSACTION_COST = 0.0001

    def __init__(self):
        logger.info("Initialized ArbitrageScanner instance.")
        self.opportunity = {
            'direction': None,
            'symbol': None,
            'binance_price': None,
            'solana_price': None,
            'profit': None
        }

    def fetch_binance_price(self, pair):
        pair = pair[1:] if pair.startswith('W') else pair
        binance = Binance()
        logger.info(f"Fetching Binance price for pair: {pair}")
        price = binance.get_price(f'{pair}USDC')
        logger.info(f"Fetched Binance price for {pair}: {price}")
        return price

    def fetch_solana_price(self, pair):
        time_str = (now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        logger.info(f"Fetching Solana price for pair: {pair} with time: {time_str}")
        price = Solana().fetch_dex_trade_data(time_ago=time_str, symbols=[pair])
        logger.info(f"Fetched Solana price for {pair}: {price}")
        return price

    def calculate_binance_fee(self, amount, pair):
        logger.info(f"calculate_binance_fee for {amount =}, {pair =}")
        fee = amount * self.BINANCE_FEE
        logger.info(f"Calculated Binance fee for amount {amount}: {fee}")
        return fee

    def calculate_solana_fee(self, amount):
        fee = amount * self.SOLANA_SWAP_FEE + self.TRANSACTION_COST
        logger.info(f"Calculated Solana fee for amount {amount}: {fee}")
        return fee

    def find_arbitrage_opportunities(self, pair):
        logger.info(f"Finding arbitrage opportunities for pair: {pair}")
        solana_price = None
        binance_price = self.fetch_binance_price(pair)
        opportunities = []
        if binance_price:
            logger.info(f"Binance price for {pair} is {binance_price}.")
            solana_price = self.fetch_solana_price(pair)
            if solana_price:
                logger.info(f"Solana price for {pair} is {solana_price}.")
                binance_fee = self.calculate_binance_fee(binance_price, pair)
                solana_fee = self.calculate_solana_fee(solana_price)

                profit_binance_to_solana = binance_price - solana_price - binance_fee - solana_fee
                logger.info(f"Profit for Binance to Solana: {profit_binance_to_solana}")
                if profit_binance_to_solana > 0:
                    opportunities.append({
                        'direction': 'Binance to Solana',
                        'symbol': pair,
                        'binance_price': binance_price,
                        'solana_price': solana_price,
                        'profit': profit_binance_to_solana
                    })
                profit_solana_to_binance = solana_price - binance_price - binance_fee - solana_fee
                logger.info(f"Profit for Solana to Binance: {profit_solana_to_binance}")
                if profit_solana_to_binance > 0:
                    opportunities.append({
                        'direction': 'Solana to Binance',
                        'symbol': pair,
                        'binance_price': binance_price,
                        'solana_price': solana_price,
                        'profit': profit_solana_to_binance
                    })
        if not opportunities:
            opportunities.append({
                'direction': None,
                'symbol': pair,
                'binance_price': binance_price,
                'solana_price': solana_price,
                'profit': None
            })
        for opp in opportunities:
            if opp.get('profit'):
                ArbitrageOpportunity.objects.create(
                    direction=opp['direction'],
                    symbol=opp['symbol'],
                    binance_price=opp['binance_price'],
                    solana_price=opp['solana_price'],
                    profit=opp['profit']
                )
        logger.info(f"Arbitrage opportunities found for {pair}: {opportunities}")
        return opportunities[0]
