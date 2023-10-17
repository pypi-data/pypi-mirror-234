import datetime
import json
import threading
import re

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import IntPrompt
from base58 import b58encode


from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.service_interface_request.common_request import get_table_choice, get_table_index
from market_place_cli.service_interface_logic.common import calculate_amount
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState
from market_place_cli.v_cloud_market_cli_common.utils.message_decipher import decrypt_message
from market_place_cli.v_cloud_market_cli_common.utils.server_stream import ServerStream
from market_place_cli.utils.regex import is_image_name
from market_place_cli.utils.string_utils import get_container_memory


class UserServiceLogic:

    def __init__(self):
        self.title = 'User Service'
        self.service_info_cache = {}
        self.main_functions = ['Show Running User Service', 'Show Usable User Service', 'Show Past User Service', 'Show Abort User Service', 'Show Notice Message']
        self.interface_index = 0 
        self.stream = ServerStream()
        self.state = GlobalState()
        self.console = self.state.console
        self.wr = self.state.wallet_request
        self.ur = self.state.user_request
        self.md = self.state.market_display
        self.ud = self.state.user_display
        self.ws = self.state.wallet_service
        self.ms = self.state.market_service
        self.us = self.state.user_service
        self.order_service = self.state.order_service

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
                    self.interface_index = 1
                    self.show_current_user_service_logic()
                elif choice == '2':
                    self.interface_index = 2
                    self.show_usable_user_service_logic()
                elif choice == '3':
                    self.interface_index = 3
                    self.show_past_user_service_logic()
                elif choice == '4':
                    self.interface_index = 4
                    self.show_abort_user_service_logic()
                elif choice == '5':
                    self.interface_index = 5
                    self.show_notice_message()
                elif choice.lower() == 'b':
                    break
                self.interface_index = 0
            except Exception as e:
                self.console.input(f'User Service Error: {e}\nPress ENTER to retry...')

    def show_current_user_service_logic(self):
        self.show_user_service_page("ServiceRunning")

    def show_usable_user_service_logic(self):
        self.show_user_service_page("ServicePending")

    def show_past_user_service_logic(self):
        self.show_user_service_page("ServiceDone")

    def show_abort_user_service_logic(self):
        self.show_user_service_page("ServiceAbort")

    def show_notice_message(self):
        self.show_user_notice_page("ServiceNotice")

    def access_provider_api_logic(self, service_info: dict, index: int):
        try:
            # get decryption private key
            private_key = self.state.get_current_account().privateKey

            provider_host = self.ms.get_provider_host(service_info["provider"])
            service_host = self._get_service_host(provider_host, service_info.get('serviceOptions', {}).get('region'))

            info = self.us.get_user_service_info(provider_host, service_info["id"])
            magic = info["magic"]
            magic_txt = decrypt_message(private_key, magic)
            magic_dict = json.loads(magic_txt)
            content = {
                'Secret': b58encode(f"{service_host}:{magic_dict['Secret']}").decode("utf-8")
            }
            p = Panel.fit(str(content))
            p.title = "Service Login Information"
            p.title_align = "center"
            self.console.print(p)
            self.console.input("Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("[bright_red]Failed to get userservice info. Press ENTER to continue...")

    def start_user_service_api_logic(self, service_info: dict, index: int):

        if service_info["serviceStatus"] != "ServicePending":
            self.console.print(f"User service status is { service_info['status'] }, and cannot start service.")
            self.console.input("Press ENTER to continue...")
            return
        # get provider host
        user_service = self._get_us_info_with_secret(service_info, index)
        if user_service is None or "Secret" not in user_service:
            self.console.print(f"[bright_green]Fail to get secret for Service {service_info['id']}!")
            self.console.input("Press ENTER to continue...")
            return

        service_config = { "containers": [] }
        container_configs = []
        user_configs = []
        # get container and host post persistStorage
        service_options = user_service["serviceOptions"]
        # get unit num
        match_result = re.match(r'^(\d+)-Unit-Resource', service_options["resourceUnit"])
        if not match_result:
            return
        unit_num = int(match_result.group(1))

        # if only 1 unit available, skip prompt and set container_num 1
        if unit_num > 1:
            container_num = self.ur.get_container_num(unit_num)
        else:
            container_num = unit_num

        # set usable_unit_num and usable_host_num
        usable_unit_num = unit_num
        usable_host_num = unit_num

        for i in range(container_num):
            # if no usable unit, stop loop
            if usable_unit_num == 0:
                break
            # if no usable host port, stop loop
            if usable_host_num == 0:
                break
            self.console.print(f'Please set config for Container {i+1}:')
            # get container name and image_name
            name = self.ur.get_container_name()
            image_info = self.ur.get_image_info(self.us.check_image, user_service["service_host"])
            # ask unit num for this container, if only 1 unit available, skip prompt and set container_unit_num 1
            if unit_num > 1:
                container_unit_num = self.ur.get_container_unit_num(usable_unit_num)
            else:
                container_unit_num = unit_num
            # caculate rest usable unit num
            usable_unit_num = usable_unit_num - container_unit_num
            # ask host num for this container
            container_host_num = self.ur.get_container_host_num(usable_host_num)
            # caculate rest usable host num
            usable_host_num = usable_host_num - container_host_num
            # init config
            container_config = {
                "name": name,
                "imageName": image_info['name'],
                "resourceUnit": container_unit_num,
                "ports": [],
                "envs": [],
                "mountPath": "",
                "command": "",
                "args": "",
                "configMountPath": "",
                "config": ""
            }
            user_config = {
                "username": image_info['username'],
                "password": image_info['password']
            }
            # set container port and host port
            container_config["ports"] = self.ur.get_ports(name, container_host_num, service_options, container_configs, user_service["service_host"], self.us.check_ports)
            # get env list
            env_list = self.ur.get_envs()
            container_config["envs"] = env_list
            # get mount path
            if service_options.get("persistStorage") == "Yes":
                container_config["mountPath"] = self.ur.get_mount_path()
            # get command
            cmd = self.console.input("Please input command (optional): ")
            if len(cmd.replace(" ", "")) > 0:
                container_config["command"] = cmd
            # get args
            args = self.console.input("Please input arguments (optional): ")
            if len(args) != 0:
                container_config["args"] = args
            # get config map
            config_path = self.ur.get_config_path()
            if len(config_path) > 0:
                config_content = ''
                while True:
                    path = self.console.input("Please input the path of your local config file: ")
                    config_content = self.us.load_config_from_file(path)
                    if config_content:
                        break
                    self.console.input("[bright_red]Empty config content. Press enter to retry.")
                container_config["configMountPath"] = config_path
                container_config["config"] = config_content
            # add to containers list
            container_configs.append(container_config)
            user_configs.append(user_config)
        # According to the requirements of backend developer, for multi containers in one pod with persistent storage
        # at least one `mountPath` param should be set
        if service_options.get("persistStorage") == "Yes":
            # if all `mountPath` param is empty, stop and retry
            if not any(config.get('mountPath') for config in container_configs):
                self.console.print("At least one `mountPath` should be set for `persistStorage` pod")
                self.console.input("Press ENTER to continue...")
                return
        # add container_configs to service_config
        service_config["containers"] = container_configs
        # add private image login info
        service_config["pvtLogin"] = user_configs

        try:
            # deployment with v-kube-service host
            if not self.us.start_usr_service(service_config, user_service["service_host"], user_service["Secret"]):
                self.console.print(f"[bright_red]Failed to start service { service_info['id'] }")
            else:
                self.console.print(f"[bright_green]User Service { service_info['id'] } has been deployed successfully!")
        except Exception as e:
            print(e)
            self.console.print(f"[bright_red]Failed to start service { service_info['id'] }")
        self.console.input("Press ENTER to continue...")

    def tail_service_log_logic(self, service_info: dict, index: int):
        user_service = self._get_us_info_with_secret(service_info, index)
        if user_service is None or "Secret" not in user_service:
            self.console.print(f"[bright_green]Service {service_info['id']} has invalid magic!")
            self.console.input("Press ENTER to continue...")
            return
        status_data = self.us.service_status(user_service["service_host"], user_service["Secret"])
        container_list = status_data.get("podStatus", {}).get("containerStatuses", [])
        if len(container_list) == 0:
            self.console.print(f"[bright_green]No container data!")
            self.console.input("Press ENTER to continue...")
            return
        # if more than one container, show containers list to select
        elif len(container_list) > 1:
            self.ud.display_container_of_pod(container_list)
            index = get_table_index(container_list, '[bright_green]Please choose a container and enter the INDEX')
            container_name = container_list[index]["name"]
        else:
            container_name = container_list[0]["name"]
        url = user_service["service_host"] + f"/api/v1/k8s/pod/logs?container={container_name}"
        headers = {
            "Connection": "close",
            "secret": user_service["Secret"]
        }
        self.console.clear()
        self.console.print("[bright_green]Press ENTER to stop log...")
        log_thread = threading.Thread(target=self.stream.open, args=(url, headers, None, self.read_stream))
        log_thread.daemon = True
        log_thread.start()
        self.console.input("")
        # close stream
        self.stream.close()

    def show_config_map(self, service_info: dict, index: int):
        try:
            user_service = self._get_us_info_with_secret(service_info, index)
            configmap_data = self.us.config_map(user_service["service_host"], user_service["Secret"])
            for container in configmap_data:
                self.console.print(f'[bright_green]Config for Container {container}:[/]\n{configmap_data[container]}\n')
            self.console.input("Press ENTER to continue...")
        except Exception as e:
            self.console.print('No container config for this pod')
            self.console.input("Press ENTER to continue...")
            return

    def restart_user_service_logic(self, service_info: dict, index: int):
        try:
            confirm = self.console.input(f'[bright_green]Are you sure you want to restart the user services? (default n) \[y/N]: ').strip().lower()
            if confirm != 'y':
                self.console.input("Canceled. Press ENTER to continue...")
                return
            user_service = self._get_us_info_with_secret(service_info, index)
            result = self.us.restart_usr_service(user_service["service_host"], user_service["Secret"])
            self.console.print('Success. Service is restarting. Please wait.')
            self.console.input("Press ENTER to continue...")
        except Exception as e:
            self.console.print(e)
            self.console.input("Press ENTER to continue...")
            return

    def update_service_config(self, service_info: dict, index: int):
        try:
            user_service = self._get_us_info_with_secret(service_info, index)
            new_config = {
                "config": {},
                "environment": {}
            }
            status_data = self.us.service_status(user_service["service_host"], user_service["Secret"])
            try:
                configmap_data = self.us.config_map(user_service["service_host"], user_service["Secret"])
            except Exception as e:
                configmap_data = {}
            containers = status_data['podSpec']['containers']
            for container in containers:
                container_name = container['name']
                # not set config if no config map mouthPath for this container
                if container_name in configmap_data:
                    confirm1 = self.console.input(f'[bright_green]Do you want to update container config for container {container_name}? (default n) \[y/N]: ').strip().lower()
                    if confirm1 == 'y':
                        config_content = ''
                        while True:
                            path = self.console.input("Please input the path of your local config file: ")
                            config_content = self.us.load_config_from_file(path)
                            if config_content:
                                break
                            self.console.input("[bright_red]Empty config. Press enter to retry.")
                        new_config['config'][container['name']] = config_content
                confirm2 = self.console.input(f'[bright_green]Do you want to update env for container {container_name}? (default n) \[y/N]: ').strip().lower()
                if confirm2 == 'y':
                    while True:
                        env_list = self.ur.get_envs()
                        if len(env_list) > 0:
                            break
                        self.console.input("[bright_red]Empty env list. Press enter to retry.")
                    # convert env_list to env_dict
                    # env_list [{"name": key,"value": value}]
                    # env_dict {key: value}
                    env_dict = {}
                    for env in env_list:
                        env_dict[env['name']] = env['value']
                    new_config['environment'][container['name']] = env_dict
            # judge if new_config['config'] and new_config['environment'] is empty
            if len(new_config['config']) == 0 and len(new_config['environment']) == 0:
                self.console.input("Canceled. Press ENTER to continue...")
                return
            confirm = self.console.input(f'[bright_green]Are you sure you want to restart and update the config for service {user_service["id"]}? (default n) \[y/N]: ').strip().lower()
            if confirm != 'y':
                self.console.input("Canceled. Press ENTER to continue...")
                return
            result = self.us.update_config(user_service["service_host"], user_service["Secret"], new_config)
            self.console.print('Success. Service is restarting. Please wait.')
            self.console.input("Press ENTER to continue...")
        except Exception as e:
            self.console.print(e)
            self.console.input("Press ENTER to continue...")
            return

    def domain_logic(self, service_info: dict, nonce: int):
        try:
            user_service = self._get_us_info_with_secret(service_info, nonce)
            if user_service is None:
                return
            while True:
                status_data = self.us.service_status(user_service["service_host"], user_service["Secret"])
                # if no domain, init as empty list
                domain_data_list = status_data.get("domains") or []
                domain_table_list = []
                for index, domain_data in enumerate(domain_data_list):
                    item = {
                        'index': index,
                        "domain": domain_data["domain"],
                        "port": domain_data["containerPort"],
                        "isHttps": domain_data["isHttps"]
                    }
                    domain_table_list.append(item)
                headers = [
                    { "text": "Index", "value": "index"},
                    { "text": "Domain Name", "value": "domain"},
                    { "text": "Container Port", "value": "port"},
                    { "text": "Is Https", "value": "isHttps"}
                ]
                title = '[bold bright_magenta] Domain Name'
                w = self.ud.display_domain_table(title, headers, domain_table_list)
                # if domain is empty, only show bind choice
                if len(domain_data_list) > 0:
                    choices = {'b': '[B]Bind Domain Name', 'c': '[C]Clean Up Domain Name', 'u': '[U]Unbind Domain Name'}
                else:
                    choices = {'b': '[B]Bind Domain Name'}
                choice = get_table_choice(self.console, w, has_next=False, extra=choices)
                if choice == 'b':
                    self.bind_domain_logic(user_service, domain_data_list)
                    continue
                elif choice == 'c':
                    self.unbind_domain_logic(user_service)
                    continue
                elif choice == 'u':
                    self.delete_domain_logic(user_service, domain_data_list)
                    continue
                elif choice == 'e':
                    break
        except Exception as e:
            print(e)
            self.console.input("Failed. Press ENTER to continue...")

    def bind_domain_logic(self, user_service: dict, domain_data_list: list):
        reg = "^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$"
        base_reg = "[a-zA-Z0-9][-a-zA-Z0-9]{0,62}\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62}$"
        try:
            while True:
                domain_name = self.console.input('[bright_green]Please input the domain name: ')
                if re.match(reg, domain_name):
                    break
                self.console.print('[bright_red]Invalid domain name. Please try again.')
            container_port = IntPrompt.ask('[bright_green]Please enter the container port')
            # reg search base donmain
            reg_result = re.search(base_reg, domain_name)
            if reg_result:
                base_domain = reg_result.group()
            is_https = None
            is_set_https = True
            # if domain is already set, not set again
            for domain_data in domain_data_list:
                if base_domain in domain_data['domain']:
                    is_set_https = False
                    break
            while is_set_https:
                # Give prompt for initial set domain name.
                self.console.print('[bright_green]Https can only be set when the domain name is bound for the first time.')
                use_https = self.console.input('[bright_green]Do you want to use https (default Y)[Y/n]: ').strip().lower()
                if use_https in ['y', 'n', '']:
                    is_https = False if use_https =='n' else True
                    break
                self.console.print('[bright_red]Invalid input. Please try again.')
            result = self.us.bind_domain_name(user_service["service_host"], user_service["Secret"], domain_name, is_https, container_port)
            if self.check_response(result):
                # check_response, if old version response error 501
                # proxy unbind and bind for user
                self.us.unbind_domain_name(user_service["service_host"], user_service["Secret"])
                for domain_data in domain_data_list:
                    self.us.bind_domain_name(user_service["service_host"], user_service["Secret"], domain_data['domain'], domain_data['isHttps'], domain_data['containerPort'])
            else:
                self.console.input("Success. Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("Failed. Press ENTER to continue...")

    def unbind_domain_logic(self, user_service: dict):
        try:
            confirm = self.console.input(f'[bright_green]Are you sure you want to clean up all domain names for user service {user_service["id"]}? (default n) \[y/N]: ').strip().lower()
            if confirm != 'y':
                self.console.input("Canceled. Press ENTER to continue...")
                return
            result = self.us.unbind_domain_name(user_service["service_host"], user_service["Secret"])
            self.console.input("Success. Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("Failed. Press ENTER to continue...")

    def delete_domain_logic(self, user_service: dict, domain_data_list: list):
        try:
            action = 'Del'
            index_str = self.console.input(f"[bright_green]Please input index numbers of the domain name you want to unbind (separated by space or comma): ").strip().lower()
            str_list = index_str.replace(' ',',').split(',')
            # filter and remove duplicate index
            index_list = list(set([int(item) for item in str_list if item.isdigit()]))
            delete_list = []
            for i in index_list:
                delete_list.append(domain_data_list[i]['domain'])
            confirm = self.console.input(f'[bright_green]Are you sure you want to unbind the domain {", ".join(delete_list)}? (default n) \[y/N]: ').strip().lower()
            if confirm != 'y':
                self.console.input("Canceled. Press ENTER to continue...")
                return
            result = self.us.update_domain_name(user_service["service_host"], user_service["Secret"], action, delete_list)
            # check_response, if old version response error 501
            if self.check_response(result):
                # proxy unbind for user if 501
                self.us.unbind_domain_name(user_service["service_host"], user_service["Secret"])
            else:
                self.console.input("Success. Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("Failed. Press ENTER to continue...")

    def check_response(self, resp):
        if 'error' in resp and 'code' in resp['error']:
            if resp['error']['code'] == 501:
                return True
            elif 'message' in resp['error']:
                raise Exception(f"Error: {resp['error']['message']}")
        return False

    def update_image_logic(self, service_info: dict, index: int):
        try:
            user_service = self._get_us_info_with_secret(service_info, index)
            image_info = self.ur.get_image_info(self.us.check_image, user_service["service_host"])
            confirm = self.console.input(f'[bright_green]Are you sure you want to update the image to {image_info["name"]}? (default n) \[y/N]: ').strip().lower()
            if confirm != 'y':
                self.console.input("Canceled. Press ENTER to continue...")
                return
            result = self.us.update_image(user_service["service_host"], user_service["Secret"], image_info)
            self.console.input("Success. Press ENTER to continue...")
        except Exception as e:
            print(e)
            self.console.input("Failed. Press ENTER to continue...")

    def renew_user_service_logic(self, serviceList: list):
        try:
            renew_list = []
            renew_data = {}
            total_amount = 0
            renew_num = 0
            while True:
                result = self.console.input('[bright_green]Please input the service index or press enter to stop:').strip()
                if result == '':
                    break
                if not result.isdigit():
                    self.console.input('[bright_red]Please input a correct index number. Press ENTER to continue...')
                    continue
                index = int(result)
                if index < 0 or index > len(serviceList) - 1:
                    self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                    continue
                # Ask renewal duration
                duration = IntPrompt.ask('[bright_green]Please enter the renewal duration number: ')

                user_service_id = serviceList[index]['id']
                provider = serviceList[index]['provider']
                # calculate amount
                service_id = serviceList[index]['serviceID']
                service_info = self.service_info_cache[service_id]
                options = serviceList[index]['serviceOptions']
                price_set = self.ms.find_price_set(service_info['durationToPrice'], options)
                amount = calculate_amount(price_set, duration)

                # add renew service data for different provider
                if provider not in renew_data:
                    renew_data[provider] = {}
                renew_data[provider][user_service_id] = {
                    'userServiceID': user_service_id,
                    'duration': duration,
                    # use float amount for renew service api
                    'amount': float(amount)
                }
                total_amount += amount
                renew_num += 1

            if renew_num == 0:
                self.console.input('[bright_red]No input. Press ENTER to continue...')
                return

            # add to list to display amount in table
            for item in renew_data.values():
                renew_list.extend(list(item.values()))
            renew_list.append({'userServiceID':'Total', 'amount': total_amount})
            headers = [
                {"text": "User Service ID", "value": 'userServiceID'},
                {"text": "Duration", "value": "duration"},
                {"text": "Amount", "value": "amount"},
            ]
            w = self.ud.display_renew_amount(headers, renew_list)
            confirm = self.console.input(f'[bright_green]Are you sure you want to create the renewal order? (default n) \[y/N]:').strip().lower()
            if confirm != 'y':
                return
            # create renew order for different providers
            for item in renew_data.values():
                order_brief = self.us.renew_usr_service(list(item.values()))
                self.md.display_order_brief(order_brief)
                confirm = self.console.input(f'[bright_green]Do you want to pay this renewal order directly? (default n) \[y/N]:').strip().lower()
                if confirm != 'y':
                    continue
                self.order_logic.pay_order(order_brief['id'])
        except Exception as e:
            self.console.input("Renew error. Press enter and try again.")

    def refund_user_service_logic(self, serviceList: list):
        refund_num = 0
        refund_data = {}
        while True:
            result = self.console.input('[bright_green]Please input the service index or press enter to stop:').strip()
            if result == '':
                break
            if not result.isdigit():
                self.console.input('[bright_red]Please input a correct index number. Press ENTER to continue...')
                continue
            index = int(result)
            if index < 0 or index > len(serviceList) - 1:
                self.console.input('[bright_red]Index out of range. Press ENTER to continue...')
                continue

            service_id = serviceList[index]['serviceID']
            user_service_id = serviceList[index]['id']
            provider = serviceList[index]['provider']
            if not self.service_info_cache[service_id]['refundable']:
                self.console.input('[bright_red]This service is not refundable.Press ENTER to continue...')
                continue
            # save user services for different providers
            if provider not in refund_data:
                refund_data[provider] = []
            if user_service_id not in refund_data[provider]:
                refund_data[provider].append(user_service_id)
                refund_num += 1
        if refund_num == 0:
            self.console.input('[bright_red]No input. Press ENTER to continue...')
            return
        confirm = self.console.input(f'[bright_green]Are you sure you want to stop and refund the user services? (default n) \[y/N]: ').strip().lower()
        if confirm != 'y':
            return
        # refund for different providers
        for refund_list in refund_data.values():
            self.us.refund_usr_service(refund_list)
        self.console.print('Success. Service is refunding. Please wait.')
        self.console.input("Press ENTER to continue...")
        

    def monitor_services(self, serviceList: list, nonce: int):
        status_list = []
        with Progress() as progress:
            task = progress.add_task("[green]Querying data...", total=len(serviceList) * 2, start=False)
            progress.start_task(task)
            try:
                for service_info in serviceList:
                    if service_info["serviceStatus"] != "ServiceRunning":
                        continue
                    user_service = self._get_us_info_with_secret(service_info, nonce)
                    progress.update(task, advance=1)
                    if user_service is None:
                        continue
                    status_data = self.us.service_status(user_service["service_host"], user_service["Secret"])
                    progress.update(task, advance=1)
                    if status_data is None:
                        continue
                    for container_status in status_data.get("podStatus", {}).get("containerStatuses", []):
                        container_name = container_status["name"]
                        item = {
                            "id": service_info["id"],
                            "name": container_name,
                            "region": service_info["serviceOptions"]["region"]
                        }
                        item["image"] = container_status["image"]
                        state = list(container_status["state"].keys())
                        item["state"] = state[0]
                        item["restartCount"] = container_status["restartCount"]
                        item["hostIP"] = status_data["podStatus"]["hostIP"]

                        if not status_data:
                            item["state"] = "shutdown"

                        if "podSpec" in status_data and "containers" in status_data["podSpec"]:
                            for container_spec in status_data["podSpec"]["containers"]:
                                if container_spec["name"] == container_name:
                                    # no "port" field if not used
                                    item["ports"] = container_spec.get("ports", "-")
                                    # deal with env dict list
                                    env_list = container_spec.get("env", [])
                                    if len(env_list) == 0:
                                        item["env"] = "-"
                                    else:
                                        item["env"] = []
                                        for env in env_list:
                                            env_item = {}
                                            env_item[env["name"]] = env.get("value", '')
                                            item["env"].append(env_item)
                                    item["memory"] = container_spec["resources"]["limits"]["memory"]
                                    break
                        status_list.append(item)
            except Exception as e:
                print(e)
                self.console.input("Press ENTER to continue...")
                return
        headers = [
            { "text": "User Service ID", "value": "id"},
            { "text": "Container Name", "value": "name"},
            { "text": "Region", "value": "region"},
            { "text": "Image", "value": "image"},
            { "text": "Memory", "value": "memory"},
            { "text": "Container Status", "value": "state"},
            { "text": "Env List", "value": "env", "justify": "left"},
            # { "text": "Restart Count", "value": "restartCount"},
            { "text": "Host IP", "value": "hostIP"},
            { "text": "Port Spec", "value": "ports", "justify": "left"},
        ]
        title = '[bold bright_magenta] User Service Status'
        if len(status_list) == 0:
            self.console.print(f"[bright_green]No container data!")
        else:
            self.ud.display_service_status(title, headers, status_list)
        self.console.input("Press ENTER to continue...")

    def show_user_notice_page(self, status: str):
        cur = 1
        page_size = 10
        service_id = ''
        extra = self._get_page_choices(status)
        service_id = self.console.input('[bright_green]Please enter user service id for search (default All): ')
        while True:
            try:
                # only use v-kube-service provider for now
                # TODO: get all providers for the user
                provider_name = 'v-kube-service'
                provider_host = self.ms.get_provider_host(provider_name)
                # use notice host
                notice_host = self._get_service_host(provider_host, 'notice')
                display_result = self._construct_notice_service_page(cur, page_size, status, service_id, notice_host)
            except Exception as e:
                self.console.print(e)
                self.console.input("[bright_red]Failed to get user notice info. Press ENTER to continue...")
                break
            w = self.ud.display_notice_table(status, display_result['list'])
            has_next = len(display_result['list']) >= page_size and display_result['pagination']['total']/page_size > cur
            choice = get_table_choice(self.console, w, has_next, extra=extra)
            if choice == 'p' and cur > 1:
                cur -= 1
            elif choice == 'n' and has_next:
                cur += 1
            elif choice == 'e':
                break

    def show_user_service_page(self, status: str):
        cur = 1
        page_size = 10
        service_id = ''
        extra = self._get_page_choices(status)
        while True:
            try:
                try:
                    display_result = self._get_user_service_data(cur, page_size, status)
                except Exception as e:
                    self.console.print(e)
                    self.console.input("[bright_red]Failed to get userservice info. Press ENTER to continue...")
                    break
                self.get_service_info_data(display_result['list'], self.nonce)
                w = self.ud.display_service_table(status, display_result['list'], self.service_info_cache)
                has_next = len(display_result['list']) >= page_size and display_result['pagination']['total']/page_size > cur
                service_list = display_result['list']
                choice = get_table_choice(self.console, w, has_next, extra=extra)
                if choice == 'p' and cur > 1:
                    cur -= 1
                elif choice == 'n' and has_next:
                    cur += 1
                elif choice == 'e':
                    break
                elif choice == 'd':
                    idx = self.get_target_index(service_list)
                    self.ud.show_user_service_detail(service_list[idx])
                elif status == 'ServiceRunning' and choice == 'b':
                    idx = self.get_target_index(service_list)
                    self.domain_logic(service_list[idx], self.nonce)
                elif (status == 'ServicePending' or status == 'ServiceRunning') and choice == 'a':
                    idx = self.get_target_index(service_list)
                    self.access_provider_api_logic(service_list[idx], self.nonce)
                elif status == 'ServicePending' and choice == 's':
                    idx = self.get_target_index(service_list)
                    self.start_user_service_api_logic(service_list[idx], self.nonce)
                elif self.interface_index == 1 and choice == 't':
                    idx = self.get_target_index(service_list)
                    self.tail_service_log_logic(service_list[idx], self.nonce)
                elif self.interface_index == 1 and choice == 'c':
                    idx = self.get_target_index(service_list)
                    us_info = service_list[idx]
                    self.show_config_map(us_info, self.nonce)
                elif self.interface_index == 1 and choice == 'r':
                    idx = self.get_target_index(service_list)
                    self.restart_user_service_logic(service_list[idx], self.nonce)
                elif self.interface_index == 1 and choice == 'u':
                    idx = self.get_target_index(service_list)
                    self.update_service_config(service_list[idx], self.nonce)
                elif self.interface_index == 1 and choice == 'm':
                    temp_list = []
                    idx = self.console.input('[bright_green]Please enter the user service index (default All): ').strip()
                    if idx != '':
                        temp_list.append(service_list[int(idx)])
                    else:
                        temp_list = service_list
                    if len(temp_list) == 0:
                        temp_list = display_result["list"]
                    self.monitor_services(temp_list, self.nonce)
                elif self.interface_index == 1 and choice == 'g':
                    self.renew_user_service_logic(display_result['list'])
                elif self.interface_index == 1 and choice == 'h':
                    idx = self.get_target_index(service_list)
                    self.update_image_logic(service_list[idx], self.nonce)
                elif (self.interface_index == 1 or self.interface_index == 2) and choice == 'f':
                    self.refund_user_service_logic(display_result['list'])
            except Exception as e:
                self.console.print(e)
                self.console.input("Press ENTER to continue...")

    def validate_user_service(self, result: dict, user_service_id: str) -> (dict, bool):
        found = False
        for u in result['list']:
            if u['id'] == user_service_id:
                found = True
                return u, found
        if not found:
            self.console.input("[bright_red]User Service ID Not Found.[/] Press ENTER to continue...")
            return None, found

    def get_target_index(self, data_list: dict):
        return get_table_index(data_list, '[bright_green]Please enter the User Service INDEX')

    def get_service_info_data(self, service_list: list, index: int = 0):
        for service in service_list:
            service_id = service['serviceID']
            if service_id not in self.service_info_cache:
                service_info = self.ms.get_service_info(service_id)
                self.service_info_cache[service_id] = service_info

    def _construct_notice_service_page(self, cur_page: int, page_size: int, status: str, service_id: str = '', provider_host: str = ''):
        display_result = self.us.get_user_notice_info(
            current=cur_page,
            page_size=page_size,
            service_id=service_id,
            provider_host=provider_host
        )
        return display_result

    def _get_user_service_data(self, cur_page: int, page_size: int, status: str):
        result = self.us.get_user_service_data(
            current=cur_page,
            page_size=page_size,
            statuses=[status]
        )
        return result

    def _get_page_choices(self, status: str):
        extra = {}
        if status == 'ServiceRunning':
            extra = {'d': '[D]User Service Detail', 'a': '[A]User Service API Access', 't': '[T]Tail Service Log', 'b': '[B]Domain Name', 'm': '[M]Service Status', 'r': '[R]Restart Service', 'f': '[F]Refund Service', 'g': '[G]Renew Service', 'h': '[H]Update Image', 'c': '[C]Container Config', 'u': '[U]Update Config'}
        elif status == 'ServicePending':
            extra = {'d': '[D]User Service Detail', 'a': '[A]User Service API Access', 's': '[S]Start a service', 'f': '[F]Refund Service'}
        return extra

    def _get_us_info_with_secret(self, service_info: dict, wallet_index: int) -> dict:
        # get decryption private key
        try:
            private_key = self.state.get_current_account().privateKey
            provider_host = self.ms.get_provider_host(service_info['provider'])
            info = self.us.get_user_service_info(provider_host, service_info["id"])
            info["provider_host"] = provider_host
            info["service_host"] = self._get_service_host(provider_host, service_info.get('serviceOptions', {}).get('region'))
            plain_txt_magic = decrypt_message(private_key, info["magic"])
            magic_dict = json.loads(plain_txt_magic)
            return { **magic_dict, **info }
        except Exception as err:
            print(err)
            return None

    def _get_service_host(self, provider_host: str, region: str):
        service_region = region.replace(' ', '-').lower()
        reg = r"^(https?://)(.+)$"
        match_result = re.match(reg, provider_host)
        if match_result:
            service_host = match_result.group(1) + service_region + '.' + match_result.group(2)
        else:
            raise Exception("Invalid service host")
        return service_host

    def read_stream(self, data):
        line = data.decode("utf-8")
        if line.startswith("data:"):
            line = line[5:]
        if line != "\"logger - Client disconnected.\"":
            self.console.print(line)
