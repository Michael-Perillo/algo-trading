import client.alpaca.adapters as alpaca_adapters
from client.alpaca.generated.alpaca_trading.api.accounts.get_account import (
    sync as get_account,
)
from client.alpaca.generated.alpaca_trading.api.positions.get_all_open_positions import (  # noqa: E501
    sync as get_all_open_positions,
)
from client.alpaca.generated.alpaca_trading.api.positions.get_open_position import (
    sync as get_open_position,
)
from client.alpaca.generated.alpaca_trading.client import (
    Client as AlpacaAPIClient,
)
from client.client_factory import get_alpaca_trading_client
from service.brokerage.base_brokerage_service import BaseBrokerageService
from shared.model import Account, OrderRequest, OrderResponse, Position


class AlpacaBrokerageService(BaseBrokerageService):
    def __init__(self, api_client: AlpacaAPIClient | None = None):
        self.api_client: AlpacaAPIClient
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = get_alpaca_trading_client()
        super().__init__(api_client)

    def get_account(self) -> Account:
        account_response_body = get_account(client=self.api_client)
        if account_response_body is None:
            raise ValueError('Failed to fetch account information from Alpaca.')
        return alpaca_adapters.account_from_alpaca(account_response_body)

    def get_open_positions(self, symbol: str | None = None) -> list[Position]:
        """
        Fetch open positions from Alpaca.
        :param symbol: Optional symbol to filter positions by.
        :return: List of open positions.
        """
        positions: list[Position] = []
        if symbol is not None:
            return [self.get_open_position(symbol)]
        all_open_positions = get_all_open_positions(client=self.api_client)
        if all_open_positions is None:
            raise ValueError('Failed to fetch open positions from Alpaca.')
        for position in all_open_positions:
            position_response_body = alpaca_adapters.position_from_alpaca(position)
            positions.append(position_response_body)
        return positions

    def get_open_position(self, symbol: str) -> Position:
        open_position_response = get_open_position(
            client=self.api_client, symbol_or_asset_id=symbol
        )
        if open_position_response is None:
            raise ValueError(f'Failed to fetch open position for symbol: {symbol}')
        return alpaca_adapters.position_from_alpaca(open_position_response)

    def place_order(self, order_request: OrderRequest) -> OrderResponse:
        # todo implement order response model
        """
        Place an order using the Alpaca API.
        :param order_request: The order request to be placed.
        :return: Generic order response.
        """
        # response = self.api_client.place_order(order_request)
        # order_response_body = AlpacaOrderResponseBody(**response.json())
        return OrderResponse(id=order_request.symbol)
