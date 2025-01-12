from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
from novapulse.constants import COMMON_TOKEN
from wrappers.arbitrage_scanner import ArbitrageScanner


def fetch_opportunity(pair):
    scanner = ArbitrageScanner()
    return scanner.find_arbitrage_opportunities(pair)


def index(request):
    final_opportunities = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_opportunity, pair) for pair in COMMON_TOKEN]
        for future in futures:
            opportunities = future.result()
            final_opportunities.append(opportunities)
    return render(request, 'arbitrage_scanner/index.html', {'opportunities': final_opportunities})
