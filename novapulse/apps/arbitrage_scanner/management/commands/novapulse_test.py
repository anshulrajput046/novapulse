import logging

from django.core.management.base import BaseCommand
from wrappers.binance import Binance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to test the Binance wrapper.
    """

    help = "Test the Binance wrapper integration."

    def handle(self, *args, **options):
        binance = Binance()
        print(binance.get_exchange_info())
        # prices = binance.get_prices()
        # time_str = (timezone.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        # solana_price = Solana().fetch_dex_trade_data(time_ago=time_str,
        #                                              symbols=['WSOL', 'RAY'])
        # scanner = ArbitrageScanner()
        # final_opportunities = []
        # for pair in ['RAY', 'WSOL', 'PENGU']:
        #     opportunities = scanner.find_arbitrage_opportunities(pair)
        #     print(opportunities)
        #     final_opportunities.append(opportunities)
        # print(final_opportunities)



