import time

from orchestrator.base_orchestrator import BaseOrchestrator
from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.base_dao import BaseDAO
from thesis.base_thesis import BaseThesis


class DefaultOrchestrator(BaseOrchestrator):
    theses: list[BaseThesis]
    brokerage_service: BaseBrokerageService
    data_dao: BaseDAO

    def run(self, interval_seconds: int = 60) -> None:
        """
        The main event loop of the trading bot.
        """
        while True:
            print('\n--- Orchestrator Cycle Start ---')
            try:
                # Iterate through each trading thesis
                for thesis in self.theses:
                    print(f'\n--- Evaluating Thesis: {thesis.thesis_name} ---')
                    orders_to_place = thesis.generate_order()
                    for order in orders_to_place:
                        print(f'Placing order for {order.symbol}: {order.dict()}')
                        self.brokerage_service.place_order(order)

            except Exception as e:
                print(f'An error occurred in the main loop: {e}')

            print(f'\n--- Orchestrator Cycle End. Waiting for {interval_seconds} seconds... ---')
            time.sleep(interval_seconds)
