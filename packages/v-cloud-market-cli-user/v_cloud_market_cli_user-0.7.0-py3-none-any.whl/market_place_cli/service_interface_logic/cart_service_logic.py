from rich.console import Console
from rich.prompt import IntPrompt
from decimal import Decimal

from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.service_interface_request.common_request import get_table_choice
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState
from market_place_cli.v_cloud_market_cli_common.utils.service_error import HttpNotFoundException

class CartServiceLogic:

    def __init__(self):
        self.title = "Cart Service"
        self.cart_display = None
        self.main_functions = ['Show cart list']
        self.state = GlobalState()
        self.console = self.state.console
        self.market_display = self.state.market_display
        self.cart_display = self.state.cart_display
        self.cart_service = self.state.cart_service
        # load cart data from cache file
        self.cart_data = self.cart_service.load_cart_from_file()
        self.ms = self.state.market_service

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
                    is_back = self.show_cart_list()
                    if is_back:
                        return True
                elif choice.lower() == 'b':
                    break
            except Exception as e:
                self.console.input(f'Cart Service Error: {e}\nPress ENTER to retry...')
    
    def add_order(self, amount: Decimal, options: dict, duration: int, expired_date: str, service_info: dict):
        provider_name = service_info['provider']
        if provider_name not in self.cart_data:
            self.cart_data[provider_name] = []
        # Due to error when convert Decimal type to json
        # change amount from Decimal to str and then add to cart data
        order = {
            'amount': str(amount),
            'options': options,
            'duration': duration,
            'expired_date': expired_date,
            'service_info': service_info
        }
        self.cart_data[provider_name].append(order)
        self.cart_service.save_cart_to_file(self.cart_data)
        self.console.input('Success. Press ENTER to continue...')

    def remove_order(self, target : int = 0):
        index = 0
        for provider_name, orders in self.cart_data.items():
            for order in orders:
                if target == index:
                    orders.remove(order)
                    self.cart_service.save_cart_to_file(self.cart_data)
                    self.console.print('Success')
                    return
                index += 1
        self.console.input('[bright_red]Index out of range. Press ENTER to continue...')

    def show_cart_list(self):
        while True:
            index = 0
            total_amount = 0
            cart_list = []
            for provider_name, orders in self.cart_data.items():
                for order in orders:
                    service_info =  order['service_info']
                    item = {
                        'index': index,
                        'id': service_info['id'],
                        'provider': service_info['provider'],
                        'name': service_info['name'],
                        'options': order['options'],
                        'duration': order['duration'] or '-',
                        'expired_date': order['expired_date'] or '-',
                        'amount': order['amount']
                    }
                    total_amount += Decimal(order['amount'])
                    cart_list.append(item)
                    index += 1
            if len(cart_list) != 0:
                total = {
                    'index': 'total',
                    'amount': str(total_amount)
                }
                cart_list.append(total)

            headers = [
                {"text": "Index", "value": 'index'},
                {"text": "Service ID", "value": 'id'},
                {"text": "Service Provider", "value": 'provider'},
                {"text": "Service Name", "value": "name"},
                {"text": "Service Options", "value": "options"},
                {"text": "Duration", "value": "duration"},
                {"text": "Expired Date", "value": "expired_date"},
                {"text": "Amount", "value": "amount"},
            ]
            w = self.cart_display.display_cart_table(headers, cart_list)
            choice = get_table_choice(self.console, w, False, {'o': '[O]Make Order from Cart', 'r': '[R]Remove Order by Choosing Index', 'b': '[B]Back to Top Menu'})
            if choice == 'o':
                self.make_order()
            elif choice == 'r':
                target_index = IntPrompt.ask("[bright_green]Please enter the order INDEX: ")
                self.remove_order(target_index)
            elif choice == 'e':
                break
            elif choice == 'b':
                return True

    def make_order(self):
        try:
            payload_dict = {}
            amount = 0
            for provider_name, orders in self.cart_data.items():
                payload = {
                    'userServices': []
                }
                for order in orders:
                    item = {
                        'serviceID': order['service_info']['id'],
                        'duration': order['duration'],
                        'serviceOptions': order['options'],
                    }
                    if order['expired_date']:
                        item['expiredDate'] = order['expired_date']
                    payload['userServices'].append(item)
                    amount += Decimal(order['amount'])
                payload_dict[provider_name] = payload

            if not self.ms.enough_balance(amount):
                self.console.print(f'[bright_red]Your balance in address index {self.nonce + 1} is not enough.')
                self.console.input('[bright_red]Order Creation Aborted...')
                return

            for provider_name, payload in payload_dict.items():
                order_brief = self.ms.make_orders(payload)
                # delete cart order if make order success
                self.cart_data.pop(provider_name, None)
                self.cart_service.save_cart_to_file(self.cart_data)
                self.market_display.display_order_brief(order_brief)
                # quick payment
                confirm = self.console.input(f'[bright_green]Do you want to pay this order directly? (default n) \[y/N]:').strip().lower()
                if confirm != 'y':
                    continue
                self.order_logic.pay_order(order_brief['id'])
        except Exception as e:
            print(e)
