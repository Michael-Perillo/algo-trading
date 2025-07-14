#!/bin/bash
datamodel-codegen --input specs/common_models.yaml --input-file-type openapi --output src/shared/model.py --output-model-type pydantic_v2.BaseModel
