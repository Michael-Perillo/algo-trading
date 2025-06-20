#!/bin/bash
datamodel-codegen --input src/trading_bot_mvp/client/alpaca/trading_spec.json --input-file-type openapi --output src/trading_bot_mvp/client/alpaca/trading_models.py --output-model-type pydantic_v2.BaseModel
datamodel-codegen --input src/trading_bot_mvp/client/alpaca/data_spec.json --input-file-type openapi --output src/trading_bot_mvp/client/alpaca/data_models.py --output-model-type pydantic_v2.BaseModel
datamodel-codegen --input specs/common_models.yaml --input-file-type openapi --output src/trading_bot_mvp/shared/model.py --output-model-type pydantic_v2.BaseModel
