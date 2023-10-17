import os, sys
sys.path.append(os.getcwd())

import click
from enum import Enum
from rich.console import Console

from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.service_interface_logic import ServiceLogicContainer

from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState

class ServiceState(Enum):
    MainService = 0
    MarketService = 1
    OrderService = 2
    WalletService = 3
    UserService = 4
    CartService = 5
    VersionService = 6
    UpperLevelService = 7


@click.command()
@click.option('-t', '--testnet', is_flag=True, help='Specify net type')
def start(testnet):
    console = Console()
    # init global state instance and init wallet services
    GlobalState().initState(console, testnet)
    GlobalState().clear_provider_cache()
    curState = ServiceState.MainService
    # init service logics
    Logics = ServiceLogicContainer()
    # register service logics
    Logics.register_logics()
    Logics.container['Wallet Initialize'].StartLogic(testnet)
    Logics.container.pop('Wallet Initialize', None)
    Logics.logic_list['version_logic'].check_version()
    init_wallet(console, Logics)
    while True:
        try:
            state = int(service_execution(console, curState, Logics))
            if state == ServiceState.UpperLevelService.value:
                curState = ServiceState.MainService
            elif state == ServiceState.MarketService.value:
                curState = ServiceState.MarketService
            elif state == ServiceState.OrderService.value:
                curState = ServiceState.OrderService
            elif state == ServiceState.WalletService.value:
                curState = ServiceState.WalletService
            elif state == ServiceState.UserService.value:
                curState = ServiceState.UserService
            elif state == ServiceState.CartService.value:
                curState = ServiceState.CartService
            elif state == ServiceState.VersionService.value:
                curState = ServiceState.VersionService
            else:
                print('You should not be here...')
        except Exception as e:
            print(f'Main Logic Start Error {e}')


def init_wallet(console: Console, Logics):
        # if empty password, init wallet data with password '' and init nonce
        global_state = GlobalState()
        if not global_state.wallet_has_password():
            global_state.update_wallet('')
            global_state.get_nonce()
        else:
            while True:
                try:
                    choice = MainInterface.display_service_choice(console, "Unlock Wallet", ["Input Password", "Restore Wallet with Seed"])
                    if choice == '1':
                        # request password from user and init wallet data
                        password = global_state.request_password()
                        global_state.update_wallet(password)
                        global_state.get_nonce()
                        return
                    elif choice == '2':
                        Logics.logic_list['wallet_logic'].reset_wallet_logic()
                    else:
                        continue
                except Exception as e:
                    console.input('Error. Press enter to continue.')


def service_execution(console: Console, state: ServiceState, Logics) -> str:
    if state == ServiceState.MainService:
        newState = MainInterface.display_service_choice(console, "Main Services", Logics.container.keys())
        if newState == '' or int(newState) > ServiceState.UpperLevelService.value or int(newState) < ServiceState.MainService.value:
            return service_execution(console, state, Logics)
        return newState
    elif state == ServiceState.MarketService:
        Logics.logic_list['market_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    elif state == ServiceState.OrderService:
        Logics.logic_list['order_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    elif state == ServiceState.WalletService:
        Logics.logic_list['wallet_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    elif state == ServiceState.UserService:
        Logics.logic_list['user_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    elif state == ServiceState.CartService:
        Logics.logic_list['cart_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    elif state == ServiceState.VersionService:
        Logics.logic_list['version_logic'].StartLogic()
        return str(ServiceState.UpperLevelService.value)
    else:
        console.input('You should not be here...')
