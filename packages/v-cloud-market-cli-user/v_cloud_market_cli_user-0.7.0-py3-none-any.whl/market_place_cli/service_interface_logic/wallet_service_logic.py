from rich.console import Console
from rich.prompt import Prompt

from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.v_cloud_market_cli_common.service_display.qr_code_display import QRCodeDisplay
from market_place_cli.v_cloud_market_cli_common.utils.service_error import WalletStorageLoadingException
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState

from market_place_cli.v_cloud_market_cli_common.config.wallet_config import PAYMENT_METHOD

class WalletServiceLogic(object):

    def __init__(self):
        self.title = 'Wallet Service'
        self.main_functions = ['Show Wallet Info', 'Make Payment to An Address', 'Generate New Address',
                               'Restore Wallet', 'Reset Password', 'Change Index of Address', 'Backup Wallet']
        self.state = GlobalState()
        self.console = self.state.console
        self.wr = self.state.wallet_request
        self.ws = self.state.wallet_service

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
                    self.show_address_logic()
                elif choice == '2':
                    self.make_payment_logic()
                elif choice == '3':
                    self.generate_new_address_logic()
                elif choice == '4':
                    self.reset_wallet_logic()
                elif choice == '5':
                    self.set_wallet_password_logic()
                elif choice == '6':
                    self.change_nonce_logic()
                elif choice == '7':
                    self.backup_wallet()
                elif choice.lower() == 'b':
                    break
            except Exception as e:
                self.console.input(f'Wallet Service Error: {e}\nPress ENTER to retry...')

    def change_nonce_logic(self):
        self.console.print(f'[bright_green]The index of address you are using is {self.nonce + 1}.')
        max_index = self.ws.wallet_data.nonce
        self.state.request_nonce(max_index)

    def backup_wallet(self):
        if self.wr.ask_save_to_csv():
            path = self.ws.save_to_csv()
            self.console.print(f'Success. File path is {path}.')
            if self.wr.confirm_display_qr_code():
                qr = QRCodeDisplay()
                qr.show_export_seed(self.ws.wallet_data.seed)
        else:
            self.console.print(f'Cancel.')
        self.console.input('Press ENTER to continue...')

    def show_address_logic(self):
        try:
            MainInterface.display_title(self.console, self.title)
            balanceFlag = self.wr.display_detail_balance()
            self.ws.show_address(balanceFlag)
        except Exception as e:
            print(e)
            self.console.input("enter to exist")

    def reset_wallet_logic(self):
        MainInterface.display_title(self.console, self.title)
        if not self.wr.confirm_restore():
            self.console.print(f'Cancel.')
            self.console.input('Press ENTER to continue...')
            return
        seed = self.wr.get_seed()
        password = self.wr.get_password()
        numAddr = self.wr.get_num_address()

        # to avoid nonce out of range, reset to 0 
        self.state.set_nonce(0)
        # set new password and then use it to recover wallet
        self.state.update_wallet(password)
        self.ws.recover_wallet(seed, numAddr)

    def generate_new_address_logic(self):
        numAddr = self.wr.get_new_address()
        self.ws.address_generate(numAddr, self.wr.get_to_append())

    def make_payment_logic(self):
        amt = self.wr.get_amount()
        if amt <= 0:
            return
        recipient = self.wr.get_recipient_address()
        attach = self.wr.get_attachment()
        self.ws.account_pay(self.nonce, recipient, amt, attach)

    def set_wallet_password_logic(self):
        if self.state.wallet_has_password():
            # has password encrypted
            while True:
                password = Prompt.ask('[bright_green]Please enter old password: ', password=True)
                if self.state.is_password_correct(password):
                    break
                self.console.print('[bright_red]Invalid password for the wallet !')

        new_password = Prompt.ask('[bright_green]Please enter new password: ', password=True)
        password_again = Prompt.ask('[bright_green]Please enter new password AGAIN: ', password=True)
        if not new_password == password_again:
            self.console.input('[red]The two new password does not match!')
            return
        # set new password and then use it to save wallet
        self.state.update_wallet(new_password)
        self.ws.save_wallet_file()
        self.console.input('[bold green]Successfully Updated. Press ENTER to continue...')

