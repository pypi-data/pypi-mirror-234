from rich.console import Console
from rich.prompt import Prompt


class WalletServiceRequest:

    def __init__(self, console: Console):
        self.console = console

    def get_num_address(self) -> int:
        msg = '[green]Please enter the number of addresses in the wallet (1-10): '
        num = self._get_num(msg)
        return num

    def get_new_address(self) -> int:
        msg = '[green]Please enter the number of wallet addresses to be added: '
        num = self._get_num(msg)
        return num

    def get_payment_address(self) -> int:
        msg = 'Please enter the index of address that you want to use: '
        return self._get_num(msg) - 1

    def get_password(self) -> str:
        msg = '[green]Please enter a password to encrypt your wallet (press ENTER for no encryption)'
        return Prompt.ask(msg, password=True)

    def get_dec_password(self) -> str:
        msg = '[green]Please enter your password for decrypting the wallet'
        return Prompt.ask(msg, password=True)

    def confirm_display_qr_code(self) -> bool:
        msg = '[bright_green]Display payment QR code (default n) [Y/n]: '
        choice = self._get_input(msg)
        return self.get_yes_no(choice)

    def confirm_restore(self) -> str:
        msg = '[green]This operation will overwrite the existing wallet data (default n) [Y/n]:'
        choice = self._get_input(msg)
        return self.get_yes_no(choice)

    def get_seed(self) -> str:
        msg = '[green]Please enter your wallet seed: '
        return self._get_input(msg)

    def ask_save_to_csv(self) -> bool:
        msg = '[green]Backup WALLET INFO and SEED to a csv file in user directory (default n) [Y/n]: '
        choice = self._get_input(msg)
        return self.get_yes_no(choice)

    def display_detail_balance(self) -> bool:
        msg = '[green]Display detailed balance info (default n) [Y/n]: '
        choice = self._get_input(msg)
        return self.get_yes_no(choice)

    def get_to_append(self) -> bool:
        msg = '[green]Append new generated addresses to wallet (default n) [Y/n]: '
        choice = self._get_input(msg)
        return self.get_yes_no(choice)

    def get_recipient_address(self) -> str:
        msg = '[green]Please enter the recipient\'s address: '
        return self._get_input(msg)

    def get_amount(self, name='') -> int:
        try:
            msg = '[green]Please enter the amount' + (f'({name}): ' if name else ':')
            amt = self._get_input(msg)
            return float(amt)
        except Exception as e:
            print(f'[bright_red]Invalid input amount: {e}')
            return -1

    def get_attachment(self) -> str:
        msg = '[green]Please enter an attachment for this payment[/] [optional]: '
        return self._get_input(msg)

    def get_yes_no(self, choice: str) -> bool:
        if choice.lower() not in ['y', 'n', '']:
            choice = 'n'
        if choice == '':
            choice = 'n'
        return choice.lower() == 'y'

    def _get_num(self, msg) -> int:
        num = 1
        while True:
            try:
                num = int(self.console.input(msg))
                if num < 1 or num > 10:
                    raise ValueError
            except ValueError:
                self.console.print('[bold bright_red]!!! Invalid Input Number !!!')
                continue
            break
        return num

    def _get_input(self, msg: str) -> str:
        return self.console.input(msg)

