import math
from decimal import Decimal
from base58 import b58encode

from v_cloud_market_cli_common.utils.wallet_cipher import WalletCipher

from v_cloud_market_cli_common.utils.wallet_storage import WalletData, get_cache_file_path
from v_cloud_market_cli_common.utils.vsyschain.account import *
from v_cloud_market_cli_common.utils.vsyschain import testnet_chain
from v_cloud_market_cli_common.utils.vsyschain.contract_helper import (
    send_data_stack_generator,
    send_function_index
)
from v_cloud_market_cli_common.config.wallet_config import (
    WALLET_FILENAME,
    AGENT_STRING,
    ADDRESS_CSV_FILENAME,
    PAYMENT_METHOD,
    PAYMENT_UNITY
)
from v_cloud_market_cli_common.utils.vsyschain.contract import (
    token_id_from_contract_id
)
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState


class WalletService:

    def __init__(self):
        self.accounts = []
        self.cipher = None
        self.wallet_data = None
        self.state = GlobalState()
        self.wallet_storage = self.state.wallet_storage
        self.display = self.state.wallet_display

    @property
    def net(self):
        return self.state.get_net_type()

    # update wallet data
    def update_wallet_data(self, data=None):
        # data and self.wallet_data is None at init, load from wallet file first
        if not self.wallet_data and data == None:
            try:
                data = self.wallet_storage.load(self.cipher)
            except Exception as e:
                return
        if data == None:
            return
        self.wallet_data = data
        self._load_accounts(seed=data.seed, nonce=data.nonce)

    def save_wallet_file(self):
        if not self.wallet_data:
            return
        self.wallet_storage.save(self.wallet_data, self.cipher)

    def set_wallet_cipher(self, new_password: str):
        self.cipher = None if not new_password else WalletCipher(new_password)

    def construct_account_info(self, account, balanceFlag):
        accInfo = {}
        accInfo['addr'] = account.address
        accInfo['accSeed'] = account.accountSeed
        accInfo['priv'] = account.privateKey
        accInfo['pub'] = account.publicKey
        accInfo['nonce'] = account.nonce
        if not balanceFlag:
            if PAYMENT_METHOD == "vsys":
                accInfo['balance'] = account.balance()
            else:
                token_id = token_id_from_contract_id(PAYMENT_METHOD, 0)
                accInfo['balance'] = account.token_balance(token_id)
        if balanceFlag:
            accInfo['balanceDetail'] = account.balance_detail()
        return accInfo

    def show_address(self, balanceFlag):
        seed = self.wallet_data.seed
        accInfoList = []
        for i in range(0, len(self.accounts)):
            account = self.accounts[i]
            accInfo = self.construct_account_info(account, balanceFlag)
            accInfoList.append(accInfo)
        self.display.display_address(accInfoList)

    def recover_wallet(self, seed, count, balanceFlag=True):
        self._load_accounts(seed, count)
        accInfoList = []
        for i in range(0, count):
            account = self.accounts[i]
            accInfo = self.construct_account_info(account, balanceFlag)
            accInfoList.append(accInfo)
        data = WalletData(seed, count, AGENT_STRING)
        # update wallet data and save to wallet file
        self.update_wallet_data(data)
        self.save_wallet_file()
        self.display.display_address(accInfoList)

    def seed_generate(self, balanceFlag, count=1):
        seed = WalletCipher.generate_phrase()
        self._protect_local_wallet()
        self.display.show_seed(seed)
        self.recover_wallet(seed=seed, count=count, balanceFlag=balanceFlag)

    def address_generate(self, count, toAppend, balanceFlag=True):
        n = self.wallet_data.nonce
        seed = self.wallet_data.seed
        accInfoList = []
        for i in range(n, n + count):
            # generate new account
            account = self._load_account(seed, i)
            accInfo = self.construct_account_info(account, balanceFlag)
            accInfoList.append(accInfo)
        if toAppend:
            data = WalletData(seed, count + n, AGENT_STRING)
            self.update_wallet_data(data)
            self.save_wallet_file()
        self.display.display_address(accInfoList)

    def account_pay(self, accountNonce, recipient, amount, attachment='', contract_id='', unity=None):
        try:
            if not unity:
                unity = PAYMENT_UNITY
            account = self.accounts[accountNonce]
            # round up to 1
            amount = math.ceil(amount * unity)
            if contract_id == 'vsys' or contract_id == '':
                resp = account.send_payment(recipient, amount, attachment=attachment)
            else:
                # check if enough token balance to pay
                token_id = token_id_from_contract_id(contract_id, 0)
                balance = account.token_balance(token_id)
                if balance < amount:
                    raise Exception('Insufficient Token balance')
                data_stack = send_data_stack_generator(recipient, amount)
                if data_stack is None:
                    self.display.console.input('[bright_red]Failed to generate data entries for payment! Press ENTER to continue...')
                    return
                resp = account.execute_contract(contract_id=contract_id, func_id=send_function_index, data_stack=data_stack, attachment=attachment)
            # need import numpy if not use scientific notation
            # self.display.show_account_pay(recipient, numpy.format_float_positional(amount/unity, trim='-'))
            self.display.show_account_pay(recipient, str(Decimal(amount)/Decimal(unity)))
        except Exception as e:
            raise e

    def _protect_local_wallet(self):
        wallet_path = get_cache_file_path(WALLET_FILENAME)
        if os.path.exists(wallet_path):
            input('> press ENTER to continue.')

    def save_to_csv(self):
        wallet_path = get_cache_file_path(ADDRESS_CSV_FILENAME)
        with open(wallet_path, 'w+') as file:
            file_str = 'Nonce, Address, Public Key, Private Key, Account Key, Seed \n'
            for account in self.accounts:
                file_str += str(account.nonce) + ',' + \
                account.address + ',' + \
                account.publicKey + ',' + \
                account.privateKey + ',' + \
                account.accountSeed + ',' + \
                account.seed + '\n'
            file.write(file_str)
        return wallet_path

    def _clean_csv_file(self):
        file_path = get_cache_file_path(ADDRESS_CSV_FILENAME)
        with open(file_path, 'w+') as file:
            file.write('')

    def _load_accounts(self, seed, nonce):
        self.accounts = []
        for i in range(0, nonce):
            self.accounts.append(self._load_account(seed, i))

    def _load_account(self, seed, nonce):
        if self.net == 'M':
            return Account(chain=mainnet_chain(), seed=seed, nonce=nonce)
        else:
            return Account(chain=testnet_chain(), seed=seed, nonce=nonce)
