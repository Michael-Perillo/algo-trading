from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.client.alpaca.trading_models import Account as AlpacaAccountResponseBody
from trading_bot_mvp.service.brokerage.base_brokerage_service import BaseBrokerageService
from trading_bot_mvp.shared.model import Account
import trading_bot_mvp.client.alpaca.api_field_mappings.model as alpaca_field_mappings


class AlpacaBrokerageService(BaseBrokerageService):
    api_client: AlpacaAPIClient

    def __init__(self, api_client: AlpacaAPIClient = None):
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = AlpacaAPIClient()
        super().__init__(api_client)

    def get_account(self) -> Account:
        response = self.api_client.get_account()
        account_response_body = AlpacaAccountResponseBody(**response.json())
        return self.map_model(account_response_body, Account, alpaca_field_mappings.AccountFieldMap())
