#!/bin/bash
set -e
# Generate Alpaca trading client
openapi-python-client generate --path src/trading_bot_mvp/client/alpaca/resources/trading_spec.json --config src/trading_bot_mvp/client/alpaca/resources/.alpaca-trading-openapi-python-client-config.json --meta none --output-path src/trading_bot_mvp/client/alpaca/generated/alpaca_trading --overwrite
openapi-python-client generate --path src/trading_bot_mvp/client/alpaca/resources/data_spec.json --config src/trading_bot_mvp/client/alpaca/resources/.alpaca-data-openapi-python-client-config.json --meta none --output-path src/trading_bot_mvp/client/alpaca/generated/alpaca_data --overwrite
# Add more lines for additional clients/specs as needed
