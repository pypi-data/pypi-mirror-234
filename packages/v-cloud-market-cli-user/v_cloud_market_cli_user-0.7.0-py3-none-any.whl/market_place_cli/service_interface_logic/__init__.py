from rich.console import Console

from .market_service_logic import MarketServiceLogic
from .order_service_logic import OrderServiceLogic
from .wallet_service_logic import WalletServiceLogic
from .user_service_logic import UserServiceLogic
from .initialization_logic import InitializationLogic
from .cart_service_logic import CartServiceLogic
from .version_service_logic import VersionServiceLogic


class ServiceLogicContainer:

    def __init__(self):
        self.container = {}
        self.logic_list = {
            'init_logic': InitializationLogic(),
            'market_logic': MarketServiceLogic(),
            'order_logic': OrderServiceLogic(),
            'wallet_logic': WalletServiceLogic(),
            'user_logic': UserServiceLogic(),
            'cart_logic': CartServiceLogic(),
            'version_logic': VersionServiceLogic(),
        }

    def register_logics(self):
        logicList = self.logic_list
        for key in logicList:
            # register each logic
            self.container[logicList[key].Name] = logicList[key]
            for name in logicList:
                if name != key:
                    # add other logics as attr on each logic object
                    exec(f"logicList['{key}'].{name} = logicList['{name}']")

