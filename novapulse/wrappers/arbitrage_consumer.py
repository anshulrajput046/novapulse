import logging
import json
import time
import threading
from channels.generic.websocket import WebsocketConsumer
from wrappers.arbitrage_scanner import ArbitrageScanner

logger = logging.getLogger(__name__)


class ArbitrageConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pair = None
        self.pair_thread = None
        self.connected = False

    def connect(self):
        logger.info("Accepted connection")
        self.connected = True
        self.accept()

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            self.pair = text_data_json.get("pair", None)
            logger.info(f"Received trading pairs: {self.pair}")

            if not self.pair or len(self.pair) != 2:
                self.send(text_data=json.dumps({
                    'error': 'Invalid pair provided. Please send an array with two trading pairs.'
                }))
                return

            self.pair_thread = threading.Thread(target=self.send_arbitrage_data)
            self.pair_thread.start()

        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            self.send(text_data=json.dumps({
                'error': 'Invalid JSON format.'
            }))
        except Exception as e:
            logger.error(f'Error processing the request: {e}')
            self.send(text_data=json.dumps({
                'error': 'An error occurred while processing your request.'
            }))

    def send_arbitrage_data(self):
        scanner = ArbitrageScanner()
        while self.connected:
            for pair in self.pair:
                opportunities = scanner.find_arbitrage_opportunities(pair)
                if opportunities:
                    self.send(text_data=json.dumps({
                        'opportunity': opportunities
                    }))
                else:
                    self.send(text_data=json.dumps({
                        'error': 'No arbitrage opportunities found.'
                    }))
                time.sleep(1)

    def disconnect(self, close_code):
        logger.info("Closed connection")
        self.connected = False
        if hasattr(self, 'pair_thread'):
            self.pair_thread.join()
