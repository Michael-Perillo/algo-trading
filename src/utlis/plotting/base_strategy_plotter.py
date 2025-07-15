import os  # Import the os module
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseStrategyPlotter(ABC, BaseModel):
    """
    An abstract base class for plotting trading strategies.
    This class is designed to be extended by specific strategy plotters.
    """

    strategy_name: str
    figures_dir: str = 'figures'  # Default directory for figures

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.figures_dir = (
            self.setup_figures_directory()
        )  # Call setup_figures_directory during initialization

    @abstractmethod
    def plot_strategy(self, *args: Any, **kwargs: Any) -> None:
        """
        Abstract method to plot the trading strategy.
        """
        pass

    def setup_figures_directory(self) -> str:
        """
        Sets up the directory for saving figures.
        This method can be overridden by subclasses to customize the directory structure.
        """
        figures_dir = f'{self.strategy_name}_figures'
        os.makedirs(figures_dir, exist_ok=True)
        return figures_dir
