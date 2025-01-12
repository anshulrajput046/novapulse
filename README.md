# NovaPulse - Arbitrage Scanner

NovaPulse is a Django-based application designed to scan and analyze arbitrage opportunities across financial markets. The project includes backend logic for real-time data processing, a WebSocket service for live market feeds running on a Daphne server, and utilities to support efficient trading strategies.

## Project Structure

```
novapulse/
├── apps/
│   └── arbitrage_scanner/     # Core backend logic for arbitrage detection and data processing
├── configurations/            # Django settings and configurations
├── logs/                      # Application logs
├── novapulse/                 # Core Django project files
├── wrappers/                  # Utility functions or middleware
├── manage.py                  # Django project manager
├── requirements.txt           # Python dependencies
└── .idea/                     # IDE settings (PyCharm)
```

## Backend

- **Framework**: Django
- **Purpose**: Scans financial markets for arbitrage opportunities.
- **Core Logic**: Implemented in `apps/arbitrage_scanner`, handling real-time data processing and arbitrage detection algorithms.
- **Database Models**: Designed to store market data, detected opportunities.
- **APIs**: Django REST Framework (assumed) for exposing arbitrage data and actionable insights.
- **Logging**: Configured under the `logs/` directory for tracking system activity and errors.

## Frontend

- No specific frontend framework is detected, suggesting the project primarily focuses on serving APIs or WebSocket feeds. If a frontend is present, it is likely implemented through Django templates or managed as a separate UI service.
- The frontend includes a refresh feature that, when clicked, updates the data according to the live feed.
- The frontend could be enhanced by utilizing a Daphne server with WebSocket support, enabling automatic data pushes to the frontend instead of relying on manual refreshes.
- ![image](https://github.com/user-attachments/assets/a82ee5fe-3d1d-4fa6-a064-efbc2fc7001c)

## WebSocket Feed

- **Server**: Daphne (ASGI server)
- **Purpose**: Provides real-time market data feeds to support arbitrage scanning.
- **Usage**: Can be utilized to subscribe to live trading data and market updates for arbitrage detection.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone 
   cd novapulse
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
   
5. **Environment Variables Needed:**
   1. BINANCE_API_KEY
   2. BINANCE_SECRET
   3. BITQUERY_API_URL
   4. BITQUERY_AUTH_TOKEN

6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Scanner:**
   ```bash
    http://127.0.0.1:8000/novapulse/scanner/
   ```

8. **Run Daphne for WebSockets:**
   ```bash
    daphne -p 8001 novapulse.asgi:application
   ```

## Notes

- **WebSocket Integration**: 
  - The WebSocket runs on Daphne and can be integrated for live market data feeds to power arbitrage detection.
  - Websocket patload - {"pair": ["WBTC", "WSOL"]}
- **Logs**: Application logs are stored in the `logs/` directory for monitoring and debugging.

---

**Author:** Anshul Singh

