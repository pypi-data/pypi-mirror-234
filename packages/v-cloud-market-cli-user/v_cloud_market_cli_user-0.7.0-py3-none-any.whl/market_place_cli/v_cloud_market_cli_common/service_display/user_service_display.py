from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.measure import Measurement

from .display_common import utc_to_local
from .table import display_table


class UserServiceDisplay:

    def __init__(self, console: Console):
        self.console = console

    def display_service_table(self, status: str, infoList: [dict], serviceInfo: dict):
        data_list = self._form_service_table_data(status, infoList, serviceInfo)
        headers = self._form_service_table_header(status)
        title = self._form_service_table_title(status)
        return self.display_service_status(title, headers, data_list, justify='center', header_style="magenta")

    def display_notice_table(self, status: str, infoList: [dict]):
        notice_list = []
        for info in infoList:
            timestamp = info['timestamp']
            local_time = self.to_local_time_str(timestamp)
            item = {
                "time": local_time,
                "serviceID": info['serviceID'],
                "noticeType": info['noticeType'],
            }
            notice_list.append(item)
        headers = [
            { "text": "Time", "value": "time"},
            { "text": "Service ID", "value": "serviceID"},
            { "text": "Notice Type", "value": "noticeType"},
        ]
        title = self._form_service_table_title(status)
        return self.display_service_status(title, headers, notice_list, 'center')

    def _form_service_table_data(self, status: str, infoList: [dict], serviceInfo: dict):
        data_list = []
        index = 0
        for info in infoList:
            cTime = self.to_local_time_str(info['serviceActivateTS'])
            sTime = self.to_local_time_str(info['serviceRunningTS'])
            if int(info['endAt']) == 0:
                eTime = 'xxxxxx'
            else:
                eTime = self.to_local_time_str(info['endAt'])
            refundable = str(serviceInfo[info['serviceID']]['refundable'])
            item = {
                "index": str(index),
                "id": info['id'],
                "type": info['service'],
            }
            if status != 'ServiceRunning':
                item.update({ "cTime": cTime})
            if status != 'ServicePending':
                item.update({ "sTime": sTime})
            item.update({
                "duration": str(info['duration']),
                "eTime": eTime,
                "refundable": refundable,
            })
            data_list.append(item)
            index += 1
        return data_list
 
    def _form_service_table_header(self, status: str):
        headers = [
            { "text": "Index", "value": "index"},
            { "text": "User Service ID", "value": "id", "no_wrap": True},
            { "text": "Service Type", "value": "type"},
        ]
        if status != 'ServiceRunning':
            headers.append({ "text": "Creation Time", "value": "cTime"})
        if status != 'ServicePending':
            headers.append({ "text": "Start Time", "value": "sTime"})
        headers.extend([
            { "text": "Duration (HOUR)", "value": "duration"},
            { "text": "Expiration Time", "value": "eTime"},
            { "text": "Refundable", "value": "refundable"},
        ])
        return headers

    def _form_service_table_title(self, status: str):
        title = 'User Service Information Table'
        if status == 'ServiceRunning':
            title = 'Running ' + title
        elif status == 'ServicePending':
            title = 'Usable ' + title
        elif status == 'ServiceDone':
            title = 'Past ' + title
        elif status == 'ServiceAbort':
            title = 'Abort ' + title
        elif status == 'ServiceNotice':
            title = 'User Service Notice Information Table'
        title = '[bold bright_magenta]' + title
        return title

    def show_user_service_detail(self, info):
        table = Table(show_header=True)
        table.box = box.ROUNDED
        table.title = '[bold bright_magenta]' + info['id'] + '\nUser Service Details'
        table.add_column('Service Type', justify='center')
        table.add_column('Service Options', justify='left')
        for col in table.columns:
            col.header_style = 'magenta'

        row = [info['service'], self._form_service_options(info['serviceOptions'])]
        table.add_row(*row)
        self.console.print(table, justify='center')
        self.console.input('Press ENTER to continue...')

    def display_user_service(self, info, secret: str = ''):
        msg = '[bold magenta]ID:[/] ' + info['userServiceID'] + '\n' + \
              '[bold magenta]Service:[/] ' + info['service'] + '\n' + \
              '[bold magenta]Service ID:[/] ' + info['serviceID'] + '\n' + \
              '[bold magenta]Address:[/] ' + info['address'] + '\n' + \
              '[bold magenta]Status:[/] ' + info['status'] + '\n' + \
              '[bold magenta]Service Active Timestamp:[/] ' + self.to_local_time_str(info['serviceActiveTS']) + '\n'

        if info['status'] in ['ServiceRunning', 'ServiceDone', 'ServiceAbort']:
            time_str = self.to_local_time_str(info['serviceRunningTS'])
            msg += '[bold magenta]Service Running Timestamp:[/] ' + time_str + '\n'
        if info['status'] == 'ServiceDone':
            time_str = self.to_local_time_str(info['serviceDoneTS'])
            msg += '[bold magenta]Service Done Timestamp:[/] ' + time_str + '\n'
        if info['status'] == 'ServiceAbort':
            time_str = self.to_local_time_str(info['serviceAbortTS'])
            msg += '[bold magenta]Service Abort Timestamp:[/] ' + time_str + '\n'

        msg += '[bold magenta]Service Options:[/] \n' + self._form_service_options(info['serviceOptions'])

        if secret:
            msg += '[bold magenta]Secret Info:[/] \n' + secret + '\n'
        self.console.print(Panel.fit(msg))
        self.console.input('Press ENTER to continue...')

    def display_renew_amount(self, headers: list, data: list, justify: str = 'left', header_style: str = ''):
        title = '[bold bright_magenta] Renewal Amount'
        try:
            w = display_table(self.console, title, headers, data, justify=justify, header_style=header_style)
            return w
        except Exception as err:
            self.console.print(err)

    def display_domain_table(self, title: str, headers: list, data: list):
        self.console.clear()
        try:
            w = display_table(self.console, title, headers, data, justify='center')
            return w
        except Exception as err:
            self.console.print(err)

    def display_service_status(self, title: str, headers: list, data: list, justify: str = 'left', header_style: str = ''):
        self.console.clear()
        try:
            w = display_table(self.console, title, headers, data, justify=justify, header_style=header_style)
            return w
        except Exception as err:
            self.console.print(err)

    def display_container_of_pod(self, container_list):
        table_list = []
        index = 0
        for container in container_list:
            item = {
                'index': index,
                'name': container['name'],
                'image': container['image'],
            }
            table_list.append(item)
            index += 1

        headers = [
            {"text": "Index", "value": "index"},
            {"text": "Container Name", "value": "name"},
            {"text": "Image Name", "value": "image"},
        ]
        display_table(self.console, "[bold bright_magenta]Choose Container", headers, table_list, show_lines = True, header_style="magenta")

    def _form_service_options(self, serviceOptions) -> str:
        service_opts = ''
        if not serviceOptions or len(serviceOptions) == 0:
            return service_opts
        for opt_key in serviceOptions:
            service_opts += '[bright_green]' + opt_key + ':[/]\n'
            service_opts += ' ' * 4 + serviceOptions[opt_key] + '\n'
        return service_opts

    def to_local_time_str(self, ts: str):
        return utc_to_local(datetime.utcfromtimestamp(int(ts))).strftime('%Y-%m-%d %H:%M:%S')

