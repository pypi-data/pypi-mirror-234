import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt

from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState
from market_place_cli.service_interface_request.common_request import get_table_choice, get_table_index


class OrderServiceLogic:

    def __init__(self):
        self.title = 'Order Service'
        self.state = GlobalState()
        self.console = self.state.console
        self.wr = self.state.wallet_request
        self.ws = self.state.wallet_service
        self.order_request = self.state.order_request
        self.order_display = self.state.order_display
        self.order_service = self.state.order_service
        self.main_functions = ['Show Pending Order', 'Show Paid Order', 'Show Filed Order',
                               'Show Order Detail', 'Pay An Order']

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
                    self.show_pending_order_logic()
                elif choice == '2':
                    self.show_paid_order_logic()
                elif choice == '3':
                    self.show_filed_order_logic()
                elif choice == '4':
                    self.show_order_detail_logic()
                elif choice == '5':
                    self.pay_order()
                elif choice.lower() == 'b':
                    break
            except Exception as e:
                self.console.input(f'Order Service Error: {e}\nPress ENTER to retry...')

    def show_pending_order_logic(self):
        self.show_order_page(status='OrderPending')

    def show_paid_order_logic(self):
        self.show_order_page(status='OrderPaid')

    def show_filed_order_logic(self):
        self.show_order_page(status='OrderFiled')

    def show_order_detail_logic(self, order_id: str = ''):
        if not order_id:
            order_id = self.order_request.get_order_id()
        try:
            info = self.order_service.query_order_info(order_id)
            self.order_display.display_order_info(info)
        except Exception as e:
            self.console.print(e)
            self.console.input('Press ENTER to continue...')

    def show_order_page(self, status: str):
        cur = 1
        page_size = 10

        title = self._construct_page_title(status)
        extra = self._construct_page_button(status)
        while True:
            try:
                display_result = self._construct_order_page_data(cur, status)
            except Exception as e:
                self.console.print(e)
                self.console.input('Press ENTER to continue...')
                return
            w = self.order_display.display_order_page(title, display_result)
            order_list = display_result['list']
            has_next = len(order_list) >= page_size or len(order_list) >= page_size

            choice = get_table_choice(self.console, w, has_next, extra=extra)
            # consider that order status takes some time to update, add refresh option
            if choice == 'r':
                continue
            if choice == 'p' and cur > 1:
                cur -= 1
            elif choice == 'n' and has_next:
                cur += 1
            elif choice == 's':
                index = get_table_index(order_list, '[bright_green]Please enter the Order INDEX')
                target_order_id = order_list[index]['id']
                if target_order_id:
                    self.show_order_detail_logic(target_order_id)
            elif choice == 'm' and status == 'OrderPending' :
                index = get_table_index(order_list, '[bright_green]Please enter the Order INDEX')
                target_order_id = order_list[index]['id']
                if target_order_id:
                    self.pay_order(target_order_id)
            elif choice == 'e':
                break

    def pay_order(self, order_id: str = ''):
        try:
            if not order_id:
                order_id = self.order_request.get_order_id()
            pubKey = self.state.get_current_account().publicKey
            order_info = self.order_service.query_order_info(order_id)
            recipient = order_info['recipient']

            # get currency
            result = self.order_service.get_currency()
            payment_list = result['list']
            # display all payment methods and currency
            self.order_display.display_pay_method(payment_list, order_info['amount'])

            # select payment method
            index = get_table_index(payment_list, '[bright_green]Please choose a payment method and enter the INDEX')
            selected_payment = payment_list[index]
            # get amount
            amount = self.wr.get_amount(selected_payment['symbolName'])
            if amount <= 0:
                self.console.print('[bright_red]!!! Invalid Amount !!!')
                self.console.input('Press ENTER to exit...')
                return
            # get payment info
            contract_id = selected_payment['contractId']
            unity = selected_payment['unit']
            # do payment
            self.ws.account_pay(self.nonce, recipient, amount, order_id + ';' + pubKey, contract_id, unity)
        except Exception as e:
            self.console.print(e)
            self.console.input('[bright_red]Failed to pay for order !!!')
        # mock payment code for local testing
        # resp = order_service.mock_order_payment(order_id, recipient, pubKey, amt)
        # self.console.print(Panel.fit(resp["content"]))

    def _construct_order_page_data(self, cur_page: int, order_status: str):
        display_result = {
            'pagination': {}
        }
        display_result = self.order_service.get_order_info_page(current=cur_page, status=order_status)
        return display_result

    def _construct_page_title(self, order_status: str):
        title = 'Order Information Table'
        if order_status == 'OrderPending':
            title = 'Pending ' + title
        elif order_status == 'OrderPaid':
            title = 'Paid ' + title
        elif order_status == 'OrderFiled':
            title = 'Filed ' + title
        return title

    def _construct_page_button(self, order_status: str):
        if order_status == 'OrderPending':
            extra = {'r': '[R]Refresh', 's': '[S]Show Order Detail', 'm': '[M]Pay An Order'}
        else:
            extra = {'r': '[R]Refresh', 's': '[S]Show Order Detail'}
        return extra

