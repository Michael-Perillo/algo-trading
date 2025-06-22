import trading_bot_mvp.client.alpaca.api_field_mappings.model as alpaca_field_mappings
from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.client.alpaca.trading_models import (
    Account as AlpacaAccountResponseBody,
)
from trading_bot_mvp.client.alpaca.trading_models import (
    Position as AlpacaPositionResponseBody,
)
from trading_bot_mvp.service.brokerage.base_brokerage_service import (
    BaseBrokerageService,
)
from trading_bot_mvp.shared.model import Account, OrderRequest, OrderResponse, Position


class AlpacaBrokerageService(BaseBrokerageService):
    api_client: AlpacaAPIClient

    def __init__(self, api_client: AlpacaAPIClient | None = None):
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = AlpacaAPIClient()
        super().__init__(api_client)

    def get_account(self) -> Account:
        response = self.api_client.get_account()
        account_response_body = AlpacaAccountResponseBody(**response.json())
        return self.map_model(
            account_response_body, Account, alpaca_field_mappings.AccountFieldMap()
        )

    def get_open_positions(self, symbol: str | None = None) -> list[Position]:
        """
        Fetch open positions from Alpaca.
        :param symbol: Optional symbol to filter positions by.
        :return: List of open positions.
        """
        response = self.api_client.get_open_positions(symbol=symbol)
        if symbol:
            # If a symbol is provided, we expect a single position response
            position_response_body = AlpacaPositionResponseBody(**response.json())
            positions = [
                self.map_model(
                    position_response_body, Position, alpaca_field_mappings.PositionFieldMap()
                )
            ]
        else:
            positions = [
                self.map_model(
                    AlpacaPositionResponseBody(**position),
                    Position,
                    alpaca_field_mappings.PositionFieldMap(),
                )
                for position in response.json()
            ]
        return positions

    def place_order(self, order_request: OrderRequest) -> OrderResponse:
        # todo implement order response model
        """
        Place an order using the Alpaca API.
        :param order_request: The order request to be placed.
        :return: Generic order response.
        """
        # response = self.api_client.place_order(order_request)
        # order_response_body = AlpacaOrderResponseBody(**response.json())
        return OrderResponse(symbol=order_request.symbol)
