import os
import time
from rich.console import Console

from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState
from market_place_cli.v_cloud_market_cli_common.config.wallet_config import WALLET_FILENAME
from market_place_cli.v_cloud_market_cli_common.utils.wallet_storage import get_cache_file_path
from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface


class InitializationLogic(object):

    def __init__(self):
        # TODO use wallet storage
        self.title = 'Wallet Initialize'
        self.isTestnet = False
        self.main_functions = ['Recover Wallet From Seed', 'Generate New Wallet']
        self.state = GlobalState()
        self.console = self.state.console
        self.wr = self.state.wallet_request
        self.ws = self.state.wallet_service

    @property
    def Name(self):
        return self.title

    def StartLogic(self, isTestnet: bool):
        # This should be executed once if no wallet file detected
        self.isTestnet = isTestnet
        self.console.clear()
        wallet_path = get_cache_file_path(WALLET_FILENAME)
        if os.path.isfile(wallet_path):
            return
        MainInterface.display_title(self.console, self.title)
        self.console.print('[red]System does not detect wallet in your local environment.[/]')
        time.sleep(2)
        while True:
            choice = MainInterface.display_service_choice(self.console, self.title, self.main_functions)
            if choice not in ['1', '2']:
                self.console.print('[red] !!! Invalid Choice !!!')
                time.sleep(2)
                continue
            break
        if choice == '1':
            self._recover_from_seed()
        elif choice == '2':
            self._generate_new_wallet()

    def _recover_from_seed(self):
        numAddr = self.wr.get_num_address()
        net = 'T' if self.isTestnet else 'M'
        password = self.wr.get_password()
        self.state.update_wallet(password)
        seed = self.wr.get_seed()
        self.ws.recover_wallet(seed, numAddr)

    def _generate_new_wallet(self):
        numAddr = self.wr.get_num_address()
        net = 'T' if self.isTestnet else 'M'
        password = self.wr.get_password()
        self.state.update_wallet(password)
        self.ws.seed_generate(self.wr.display_detail_balance(), numAddr)
