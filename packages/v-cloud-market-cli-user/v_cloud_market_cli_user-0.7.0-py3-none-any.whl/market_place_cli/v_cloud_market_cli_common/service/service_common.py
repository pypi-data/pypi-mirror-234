from rich.console import Console
from market_place_cli.v_cloud_market_cli_common.utils.service_error import WalletStorageLoadingException
from market_place_cli.v_cloud_market_cli_common.utils.wallet_storage import WalletStorage, get_cache_file_path
from market_place_cli.v_cloud_market_cli_common.config.wallet_config import WALLET_FILENAME
from market_place_cli.v_cloud_market_cli_common.utils.wallet_cipher import WalletCipher
from market_place_cli.v_cloud_market_cli_common.config.server_config import PLATFORM_HOST

from market_place_cli.service_interface_request.wallet_service_request import WalletServiceRequest
from market_place_cli.service_interface_request.user_service_request import UserServiceRequest
from market_place_cli.service_interface_request.order_service_request import OrderServiceRequest
from market_place_cli.service_interface_request.market_service_request import MarketServiceRequest
from market_place_cli.v_cloud_market_cli_common.service_display.market_service_display import MarketServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.cart_service_display import CartServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.order_service_display import OrderServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.user_service_display import UserServiceDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.wallet_service_display import WalletServiceDisplay

from rich.prompt import Prompt

from v_cloud_market_cli_common.utils.service_error import (
    HttpNotFoundException,
    HttpBadRequestException
)

class ServiceCommon:

    def __init__(self):
        pass

    @staticmethod
    def validate_response(resp):
        if not isinstance(resp, dict) and not isinstance(resp, list):
            raise HttpNotFoundException
        elif 'error' in resp:
            if 'code' in resp['error'] and 'message' in resp['error']:
                raise Exception(f"Net Error: {resp['error']['message']}")
            else:
                raise Exception(f"Net Error: {resp}")

class GlobalState:

    console = None
    _password = None
    _nonce = None
    _net_type = 'M'
    wallet_service = None

    def __new__(cls):
        # Use Singleton pattern, return the same instance
        if not hasattr(cls,'instance'):
            cls.instance = super(GlobalState, cls).__new__(cls)
        return cls.instance

    def initState(self, console: Console, isTestnet: bool):
        from market_place_cli.v_cloud_market_cli_common.service.wallet_service import WalletService
        from market_place_cli.v_cloud_market_cli_common.service.market_service import MarketService
        from market_place_cli.v_cloud_market_cli_common.service.user_service import UserService
        from market_place_cli.v_cloud_market_cli_common.service.order_service import OrderService
        from market_place_cli.v_cloud_market_cli_common.service.cart_service import CartService
        from market_place_cli.v_cloud_market_cli_common.service.version_service import VersionService
        from market_place_cli.v_cloud_market_cli_common.utils.server_api_wrapper import ServerWrapper
        self.console = console
        # init service request
        self.wallet_request = WalletServiceRequest(console)
        self.user_request = UserServiceRequest(console)
        self.order_request = OrderServiceRequest(console)
        self.market_request = MarketServiceRequest(console)
        # init service display
        self.market_display = MarketServiceDisplay(console)
        self.cart_display = CartServiceDisplay(console)
        self.order_display = OrderServiceDisplay(console)
        self.user_display = UserServiceDisplay(console)
        self.wallet_display = WalletServiceDisplay(console)

        self._net_type = self.get_net(isTestnet)
        # init wallet data file
        self.wallet_path = get_cache_file_path(WALLET_FILENAME)
        self.wallet_storage = WalletStorage(self.wallet_path)
        # init wallet core service
        self.wallet_service = WalletService()
        self.server_wrapper = ServerWrapper(PLATFORM_HOST)
        # init services
        self.market_service = MarketService()
        self.user_service = UserService()
        self.order_service = OrderService()
        self.cart_service = CartService()
        self.version_service = VersionService()

    def get_net(self, is_testnet) -> str:
        return 'T' if is_testnet else 'M'

    def get_net_type(self):
        return self._net_type

    def request_nonce(self, max_nonce=10):
        num = 1
        while True:
            try:
                num = int(self.console.input(f'[green]Please enter the index of address that you want to use (1-{max_nonce}): '))
                if num < 1 or num > max_nonce:
                    raise ValueError
            except ValueError:
                self.console.print(f'[bold bright_red]!!! Index should be between 1-{max_nonce} !!!')
                continue
            break
        self.set_nonce(num - 1)
        self.console.input(f'Success. Address index is set to {num}. Press ENTER to continue...')

    def set_nonce(self, nonce):
        self._nonce = nonce

    def get_nonce(self):
        if self._nonce == None:
            max_nonce = len(self.wallet_service.accounts)
            self.request_nonce(max_nonce)
        return self._nonce

    def get_current_account(self):
        nonce = self.get_nonce()
        return self.wallet_service.accounts[nonce]

    # update global password and reload wallet data if password change
    def update_wallet(self, password):
        if self._password != password:
            self.wallet_service.set_wallet_cipher(password)
            self._password = password
            # try to update wallet data if password is updated
            self.wallet_service.update_wallet_data()

    def clear_provider_cache(self):
        provider_cache_file = get_cache_file_path('provider_cache.json')
        with open(provider_cache_file, 'w') as cache:
            cache.write('{}')

    def request_password(self):
        password = ''
        while True:
            try:
                if self.wallet_has_password():
                    password = Prompt.ask('[green]Please enter your password for decrypting the wallet', password=True)
                if self.is_password_correct(password):
                    if self.wallet_has_password():
                        self.console.print('Wallet decrypted successfully.')
                    break
                else:
                    self.console.print('[bold bright_red]Password is wrong. Please try again.')
                    continue
            except Exception as e:
                break
        return password

    def get_password(self):
        return self._password

    def is_password_correct(self, password) -> bool:
        cipher = None if not password else WalletCipher(password)
        wallet_data = self.wallet_storage.load(cipher)
        if wallet_data:
            return True
        self.console.print('[bold bright_red]Failed to load information from wallet file.')
        return False

    def wallet_has_password(self) -> bool:
        try:
            wallet_data = self.wallet_storage.load(None)
            return wallet_data is None
        except Exception as e:
            return True
 
