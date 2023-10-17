from .contract import Contract, DataEntry, Type
from .crypto import bytes2str, sign
import struct
import base58


supersede_function_index = 0
issue_function_index = 1
destroy_function_index = 2
send_function_index = 3
transfer_function_index = 4
deposit_function_index = 5
withdraw_function_index = 6
totalSupply_function_index = 7
maxSupply_function_index = 8
balanceOf_function_index = 9
get_issuer_function_index = 10

def register_data_stack_generator(max, unity, description):
    max_data_entry = DataEntry(max, Type.amount)
    unity_data_entry = DataEntry(unity, Type.amount)
    description_data_entry = DataEntry(description, Type.short_text)
    return [max_data_entry, unity_data_entry, description_data_entry]

def supersede_data_stack_generator(new_issuer):
    new_issuer_data_entry = DataEntry(new_issuer, Type.address)
    return [new_issuer_data_entry]

def issue_data_stack_generator(amount):
    amount_data_entry = DataEntry(amount, Type.amount)
    return [amount_data_entry]

def destroy_data_stack_generator(amount):
    amount_data_entry = DataEntry(amount, Type.amount)
    return [amount_data_entry]

def send_data_stack_generator(recipient, amount):
    try:
        recipient_data_entry = DataEntry(recipient, Type.address)
        amount_data_entry = DataEntry(amount, Type.amount)
        return [recipient_data_entry, amount_data_entry]
    except Exception as e:
        print(e)
        return None

def transfer_data_stack_generator(sender, recipient, amount):
    sender_data_entry = DataEntry(sender, Type.address)
    recipient_data_entry = DataEntry(recipient, Type.address)
    amount_data_entry = DataEntry(amount, Type.amount)
    return [sender_data_entry, recipient_data_entry, amount_data_entry]

def deposit_data_stack_generator(sender, contract, amount):
    sender_data_entry = DataEntry(sender, Type.address)
    contract_data_entry = DataEntry(contract, Type.contract_account)
    amount_data_entry = DataEntry(amount, Type.amount)
    return [sender_data_entry, contract_data_entry, amount_data_entry]

def withdraw_data_stack_generator(contract, recipient, amount):
    contract_data_entry = DataEntry(contract, Type.contract_account)
    recipient_data_entry = DataEntry(recipient, Type.address)
    amount_data_entry = DataEntry(amount, Type.amount)
    return [contract_data_entry, recipient_data_entry, amount_data_entry]

def totalSupply_data_stack_generator():
    return []

def maxSupply_data_stack_generator():
    return []

def balanceOf_data_stack_generator(address):
    address_data_entry = DataEntry(address, Type.address)
    return [address_data_entry]

def get_issuer_data_stack_generator():
    return []

def issuer_db_key_generator():
    issuer_key_bytes = struct.pack(">B", 0)
    return base58.b58encode(issuer_key_bytes).decode()

def maker_db_key_generator():
    maker_key_bytes = struct.pack(">B", 1)
    return base58.b58encode(maker_key_bytes).decode()
