from trading_bot_mvp.client.base_client import BaseAPIClient, APIRequest
from typing import Optional, Dict, Any
from httpx import Response

from trading_bot_mvp.settings import get_settings


class AlpacaAPIClient(BaseAPIClient):
    """
    Concrete implementation of BaseAPIClient for Alpaca's Data and Trading APIs.
    This client parametrizes requests using APIRequest and can be used for both trading_spec and data_spec endpoints.
    """
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        # todo break settings out into separate configs for different apis
        if base_url is not None and headers is not None:
            super().__init__(base_url, headers)
            return
        settings = get_settings()
        headers = {
            "APCA-API-KEY-ID": settings.API_KEY,
            "APCA-API-SECRET-KEY": settings.SECRET_KEY,
            "Content-Type": "application/json",
        }
        super().__init__(headers=headers)


    def get_account(self) -> Response:
        """
        Fetch the account information from Alpaca.
        """
        req = APIRequest(
            method="GET",
            endpoint="/v2/account"
        )
        return self.request(req)

class AlpacaDataClient(BaseAPIClient):
    """
    Concrete implementation of BaseAPIClient for Alpaca's Data API.
    This client is used for fetching market data.
    """
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        if base_url is not None and headers is not None:
            super().__init__(base_url, headers)
            return
        settings = get_settings()
        headers = {
            "APCA-API-KEY-ID": settings.API_KEY,
            "APCA-API-SECRET-KEY": settings.SECRET_KEY,
            "Content-Type": "application/json",
        }
        super().__init__(settings.DATA_BASE_URL, headers)

    def get_bars(self, symbols: str, start: str = None, end: str = None, timeframe: str = None, limit: int = None, page_token: str = None, adjustment: str = None, feed: str = None):
        """
        Get Bar data for multiple stock symbols using the /v2/stocks/bars endpoint.
        Parameters:
            symbols (str): Comma-separated list of stock symbols (e.g., 'AAPL,TSLA')
            start (str): Filter data equal to or after this time (RFC-3339 format)
            end (str): Filter data equal to or before this time (RFC-3339 format)
            timeframe (str): Timeframe for the aggregation (e.g., '1Min', '1Hour', '1Day')
            limit (int): Number of data points to return
            page_token (str): Pagination token
            adjustment (str): Corporate action adjustment(s) for bars data
            feed (str): Which feed to pull market data from (iex, otc, sip)
        Returns:
            httpx.Response: The raw HTTP response from Alpaca
        """
        params = {"symbols": symbols}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if timeframe is not None:
            params["timeframe"] = timeframe
        if limit is not None:
            params["limit"] = limit
        if page_token is not None:
            params["page_token"] = page_token
        if adjustment is not None:
            params["adjustment"] = adjustment
        if feed is not None:
            params["feed"] = feed
        req = APIRequest(method="GET", endpoint="/v2/stocks/bars", params=params)
        return self.request(req)

