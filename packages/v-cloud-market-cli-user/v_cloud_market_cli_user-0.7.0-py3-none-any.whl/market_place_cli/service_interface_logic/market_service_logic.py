import math
from rich.console import Console
from rich.prompt import IntPrompt

from market_place_cli.v_cloud_market_cli_common.service_display.qr_code_display import QRCodeDisplay
from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.service_interface_request.common_request import get_table_choice
from market_place_cli.service_interface_logic.common import calculate_amount
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState
from market_place_cli.v_cloud_market_cli_common.utils.service_error import (
    HttpNotFoundException,
    HttpBadRequestException
)


class MarketServiceLogic(object):

    def __init__(self):
        self.title = 'Market Service'
        self.state = GlobalState()
        self.console = self.state.console
        self.wr = self.state.wallet_request
        self.mr = self.state.market_request
        self.md = self.state.market_display
        self.ws = self.state.wallet_service
        self.ms = self.state.market_service
        self.main_functions = ['Get Service Provider Information', 'Make An Order']

    @property
    def Name(self):
        return self.title

    @property
    def nonce(self):
        return self.state.get_nonce()

    @property
    def password(self):
        return self.state.get_password()

    @property
    def net_type(self):
        return self.state.get_net_type()

    def StartLogic(self):
        self.console.clear()
        while True:
            try:
                choice = MainInterface.display_service_choice(self.console, self.title, self.main_functions, True)
                if choice == '1':
                    # request provider
                    is_back = self.provider_logic()
                    if is_back:
                        return True
                elif choice == '2':
                    self.make_order_logic()
                elif choice.lower() == 'b':
                    break
            except Exception as e:
                self.console.input(f'Market Service Error: {e}\nPress ENTER to retry...')

    def provider_logic(self):
        cur = 1
        page_size = 10
        while True:
            result = self.ms.get_provider_info_page(current=cur, opt={}, page_size=page_size)
            w = self.md.display_provider_page(result)
            has_next = len(result['list']) >= page_size
            choice = get_table_choice(self.console, w, has_next, {'c': '[C]Choose Provider with Index', 'b': '[B]Back to Top Menu'})
            if choice == 'p' and cur > 1:
                cur -= 1
            elif choice == 'n' and has_next:
                cur += 1
            elif choice == 'c':
                index = IntPrompt.ask("[bright_green]Please enter the provider INDEX")
                if index < 0 or index > len(result['list']) - 1:
                    self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                    continue
                provider = result['list'][index]['name']
                is_back = self.category_logic(provider)
                if is_back:
                    return True
            elif choice == 'e':
                break
            elif choice == 'b':
                return True

    def category_logic(self, provider: str):
        cur = 1
        page_size = 10
        while True:
            result = self.ms.get_category_info_page({'provider': provider}, cur, page_size)
            w = self.md.display_category_page(result)
            has_next = len(result['list']) >= page_size
            choice = get_table_choice(self.console, w, has_next, {'c': '[C]Choose Category with Index', 'b': '[B]Back to Top Menu'})
            if choice == 'p' and cur > 1:
                cur -= 1
            elif choice == 'n' and has_next:
                cur += 1
            elif choice == 'c':
                index = IntPrompt.ask('[bright_green]Please enter the Category INDEX')
                if index < 0 or index > len(result['list']) - 1:
                    self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                    continue
                category = result['list'][index]['name']
                is_back = self.service_type_logic(provider, category)
                if is_back:
                    return True
            elif choice == 'e':
                break
            elif choice == 'b':
                return True

    def service_type_logic(self, provider: str, category: str):
        cur = 1
        page_size = 10
        opt = {
            'provider': provider,
            'category': category
        }
        while True:
            try:
                result = self.ms.get_service_info_page(opt, cur, page_size)
                idIndex = []
                for item in result['list']:
                    idIndex.append(item['id'])
                w = self.md.display_service_page(result)
                has_next = len(result['list']) >= page_size
                choice = get_table_choice(self.console, w, has_next, {'o': '[O]Make An Order ', 'i': '[I]Make An Order by choosing index', 'c': '[C]Add Service to Cart', 's': '[S]Show Cart Table', 'b': '[B]Back to Top Menu'})
                if choice == 'p' and cur > 1:
                    cur -= 1
                elif choice == 'n' and has_next:
                    cur += 1
                elif choice == 'o':
                    self.make_order_logic()
                elif choice == 'i':
                    idx = IntPrompt.ask('[bright_green]Please enter the service INDEX')
                    if idx < 0 or idx > len(idIndex) - 1:
                        self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                        continue
                    self.make_order_logic(serviceID=idIndex[idx])
                elif choice == 'c':
                    idx = IntPrompt.ask('[bright_green]Please enter the service INDEX')
                    if idx < 0 or  idx > len(idIndex) - 1:
                        self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                        continue
                    self.add_to_cart(serviceID=idIndex[idx])
                elif choice == 's':
                    is_back = self.cart_logic.show_cart_list()
                    if is_back:
                        return True
                elif choice == 'e':
                    break
                elif choice == 'b':
                    return True
            except:
                self.console.input("[bright_red]Failed to get services info. Press ENTER to continue...")
                break

    def get_order_info(self, serviceID: str = ''):
        service_id = self.mr.get_service_id() if not serviceID else serviceID  # To handle choose service id by index
        try:
            service_info = self.ms.get_service_info(service_id)
        except HttpNotFoundException:
            self.console.input("[bright_red]Service doesn't exist. Press ENTER to continue...")
            return
        except:
            self.console.input("[bright_red]Failed to get service info. Press ENTER to continue...")
            return

        opts = self.mr.user_choose_options(service_info['serviceOptions'])
        price_set = self.ms.find_price_set(service_info['durationToPrice'], opts)
        time_period = self.mr.user_choose_duration(price_set)
        amt = calculate_amount(price_set, time_period['time'])
        expired_date = time_period['expiredDate'] if 'expiredDate' in time_period else ''

        return amt, opts, time_period['time'], expired_date, service_info

    def make_order_logic(self, serviceID=None):
        pub_key = self.state.get_current_account().publicKey
        qr_display = QRCodeDisplay()

        amt, opts, duration, expired_date, service_info = self.get_order_info(serviceID=serviceID)

        if not self.ms.enough_balance(amt):
            self.console.print(f'[bright_red]Your balance in address index {self.nonce + 1} is not enough.')
            self.console.input('[bright_red]Order Creation Aborted...')
            return
        payload = {
            'userServices': [
                {
                    'serviceID': service_info['id'],
                    'duration': duration,
                    'serviceOptions': opts,
                }
            ]
        }
        if expired_date:
            payload['userServices'][0]['expiredDate'] = expired_date
        order_brief = self.ms.make_orders(payload)

        display_qr = self.mr.get_display_qr_code()
        self.md.display_order_brief(order_brief)

        if display_qr:
            qr_display.show_account_of_wallet(
                address=order_brief['recipient'],
                amt=order_brief['amount'],
                invoice=order_brief['id'] + '-' + pub_key)
            self.console.input('Press ENTER to continue...')

        # quick payment
        confirm = self.console.input(f'[bright_green]Do you want to pay this order directly? (default n) \[y/N]:').strip().lower()
        if confirm != 'y':
            return
        self.order_logic.pay_order(order_brief['id'])

    def add_to_cart(self, serviceID: str = ''):
        amount, options, duration, expired_date, service_info = self.get_order_info(serviceID=serviceID)
        provider_name = service_info['provider']
        self.cart_logic.add_order(amount, options, duration, expired_date, service_info)

