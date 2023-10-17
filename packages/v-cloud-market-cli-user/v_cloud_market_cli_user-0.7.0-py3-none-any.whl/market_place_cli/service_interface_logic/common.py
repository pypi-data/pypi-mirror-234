from decimal import Decimal

def get_net(is_testnet) -> str:
    return 'T' if is_testnet else 'M'

def calculate_amount(price_set: dict, duration: int) -> Decimal:
    discount = 1
    time_units = sorted(price_set['duration'].keys(), key=int)
    for dur in time_units:
        if duration >= int(dur):
            discount = price_set['duration'][dur]
    amt = Decimal(str(price_set['price'])) * Decimal(str(discount)) * Decimal(duration)
    return amt

