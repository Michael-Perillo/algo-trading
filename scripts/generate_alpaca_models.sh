#!/bin/bash
datamodel-codegen --input src/trading_bot_mvp/client/alpaca/trading_spec.yaml --input-file-type openapi --output src/trading_bot_mvp/client/alpaca/trading_models.py
datamodel-codegen --input src/trading_bot_mvp/client/alpaca/data_spec.yaml --input-file-type openapi --output src/trading_bot_mvp/client/alpaca/data_models.py
datamodel-codegen --input specs/common_models.yaml --input-file-type openapi --output src/trading_bot_mvp/shared/model.py
