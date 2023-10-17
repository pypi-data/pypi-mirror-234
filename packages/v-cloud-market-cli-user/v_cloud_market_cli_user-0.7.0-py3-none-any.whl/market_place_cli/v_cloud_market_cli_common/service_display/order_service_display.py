import math
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.measure import Measurement
from rich.panel import Panel
from rich import box
from .table import display_table
from decimal import Decimal

from v_cloud_market_cli_common.service_display.display_common import utc_to_local


class OrderServiceDisplay:

    def __init__(self, console: Console):
        self.console = console

    def display_order_page(self, title: str, page_result: dict) -> int:
        self.console.clear()
        table = Table(show_header=True, header_style='magenta')
        if len(page_result["list"]) > 0:
            table.title = '[bold magenta]' + title + f' --- Address: {page_result["list"][0]["address"]}'
        else:
            table.title = '[bold magenta]' + title + ' --- Address: there is no pending orders'
        table.box = box.SIMPLE_HEAD
        table.add_column('Index', justify='center')
        table.add_column('Provider', justify='center')
        table.add_column('Order ID', justify='center', no_wrap=True)
        table.add_column('Order Type', justify='center')
        table.add_column('Order Status', justify='center')
        table.add_column('Creation Time', justify='center')
        table.add_column('Recipient Address', justify='center')
        table.add_column('Amount (USD)', '[u]412,000,000', justify='right')
        table.add_column('Amount Paid (USD)', '[u]412,000,000', justify='right')
        for row in self.form_order_rows(page_result['list']):
            table.add_row(*row)
        self.console.print(table, justify='center')
        return Measurement.get(self.console, table).maximum

    def display_pay_method(self, payment_list, amount):
        table_list = []
        index = 0
        for payment in payment_list:
            amt = str(Decimal(math.ceil(amount * payment['exchangeRate'] * payment['unit'])) / Decimal(payment['unit']))
            item = {
                'index': index,
                'name': payment['symbolName'],
                'rate': payment['exchangeRate'],
                'amount': amt
            }
            table_list.append(item)
            index += 1

        headers = [
            {"text": "Index", "value": "index"},
            {"text": "Payment Method", "value": "name"},
            {"text": "Exchange Rate", "value": "rate"},
            {"text": "Total Amount", "value": "amount"},
        ]
        display_table(self.console, "[bold bright_magenta]Choose Payment Method", headers, table_list, show_lines = True, header_style="magenta")

    def display_order_info(self, order_info):
        timeStr = utc_to_local(datetime.utcfromtimestamp(int(order_info['createdAt']))).strftime('%Y-%m-%d %H:%M:%S')
        order_msg = '[bold magenta]Address:[/] ' + ' ' * 12 + order_info['address'] + '\n' + \
            '[bold magenta]Order ID:[/] ' + ' ' * 11 + order_info['id'] + '\n' + \
            '[bold magenta]Type:[/] ' + ' ' * 15 + str(order_info['type']) + '\n' + \
            '[bold magenta]Provider:[/] ' + ' ' * 11 + order_info['provider'] + '\n' + \
            '[bold magenta]Recipient:[/] ' + ' ' * 10 + order_info['recipient'] + '\n' + \
            '[bold magenta]Amount (USD):[/] ' + ' ' * 6 + str(order_info['amount']) + '\n' + \
            '[bold magenta]Amount Paid (USD):[/] ' + ' ' + str(order_info['amountPaid']) + '\n' + \
            '[bold magenta]Creation Time:[/] ' + ' ' * 6 + timeStr + '\n' + \
            '[bold magenta]Status:[/] ' + ' ' * 13 + str(order_info['status']) + '\n'

        self.console.print(Panel.fit(order_msg, title="Order Detail Info"))

        service_list = []
        for service in order_info['userServices']:
            item = {
                'id': service['id'],
                'service': service['service'],
                'serviceID': service['serviceID'],
                'duration': str(service['duration']),
                'amount': str(service['amount']),
                'activated': str(service['serviceActivated']),
                'options': service['serviceOptions'],
            }
            service_list.append(item)

        headers = [
            {"text": "User Service ID", "value": "id", "no_wrap": True},
            {"text": "Service Name", "value": "service"},
            {"text": "Service ID", "value": "serviceID"},
            {"text": "Duration (hour)", "value": "duration"},
            {"text": "Amount (USD)", "value": "amount"},
            {"text": "Service Enabled", "value": "activated"},
            {"text": "Service Options", "value": "options"},
        ]
        w = display_table(self.console, "Service Detail", headers, service_list, show_lines = True)
        self.console.input('Press ENTER to continue...')

    def form_order_rows(self, orderList: [dict]) -> [[str]]:
        rows = []
        index = 0
        for order in orderList:
            row = [str(index), order['provider'], order['id'], order['type'], order['status']]
            time_dt = datetime.utcfromtimestamp(int(order['createdAt']))
            timeStr = utc_to_local(time_dt).strftime('%Y-%m-%d %H:%M:%S')
            row.extend([
                timeStr,
                order['recipient'],
                str(order['amount']),
                str(order['amountPaid']),
            ])
            rows.append(row)
            index += 1
        return rows
