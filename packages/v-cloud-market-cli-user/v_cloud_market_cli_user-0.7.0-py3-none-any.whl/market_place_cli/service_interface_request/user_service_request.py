from rich.console import Console
from rich.prompt import IntPrompt, Prompt

from market_place_cli.utils.regex import is_image_name, is_valid_path, is_valid_env_name, is_valid_container_name
from market_place_cli.utils.string_utils import get_unit_num
class UserServiceRequest:

    def __init__(self, console: Console):
        self.console = console

    def get_user_service_id(self) -> str:
        msg = '[bright_green]Please enter the user service id: '
        return self.console.input(msg)

    def get_container_num(self, max_num) -> int:
        num = 0
        while True:
            msg = f'[bright_green]Please enter the number of container you want to create (max {max_num})'
            num = IntPrompt.ask(msg)
            if num > 0 and num <= max_num:
                break
        return num

    def get_container_name(self) -> str:
        while True:
            container_name = self.console.input('[bright_green]Please enter a valid name of the container: ').strip(" ")
            if is_valid_container_name(container_name):
                return container_name

    def get_container_unit_num(self, usable_unit_num) -> int:
        num = 0
        while True:
            msg = f'[bright_green]Please enter the number of unit you want to use for this container ({usable_unit_num} unit usable)'
            num = IntPrompt.ask(msg)
            if num > 0 and num <= usable_unit_num:
                break
        return num
    
    def get_container_host_num(self, usable_host_num) -> int:
        num = 0
        while True:
            msg = f'[bright_green]Please enter the number of port you want to use for this container ({usable_host_num} host usable)'
            num = IntPrompt.ask(msg)
            if num >= 0 and num <= usable_host_num:
                break
        return num

    def get_api_func(self, apis) -> (bool, str):
        api_types = ['normal', 'secret']
        while True:
            is_secret = False
            self.console.print('Please Choose API Type: ')
            msg = '[purple]1[/] -- Normal API Request\n' + \
                '[purple]2[/] -- Secret API Request\n'
            self.console.print(msg)
            choice = self._get_int_num('[bright_green]Please choose a number: ')
            if choice < 1 or choice > 2:
                continue
            is_secret = choice == 2
            while True:
                keys = list(apis[api_types[choice-1]].keys())
                api_func_msg = ''
                for index in range(len(keys)):
                    api_func_msg += f'[purple]{index+1}[/]' + ' -- ' + keys[index] + '\n'
                self.console.print(api_func_msg)
                api_func_choice = self._get_int_num('[bright_green]Please choose an API function: ')
                while api_func_choice < 1 or api_func_choice > len(keys):
                    self.console.print('[bright_red]!! Invalid Index Number !!\n')
                    api_func_choice = self._get_int_num('[bright_green]Please choose an API function: ')
                return is_secret, keys[api_func_choice-1]

    def _get_int_num(self, msg):
        try:
            choice = int(self.console.input(msg))
            return choice
        except ValueError:
            self.console.print('[bright_red]The input you entered in invalid.')
            return 0

    def get_image_info(self, check_image_func: callable, provider_host: str) -> str:
        image_name = None
        username = ''
        password = ''
        is_priv_image = self.console.input(f'[bright_green]Do you want to use private image? (default n) \[y/N]: ').strip().lower() == 'y'
        msg = '[bright_green]Please enter the image name on Docker Hub or Github Container Registry: '
        while image_name is None:
            value = self.console.input(msg).strip()
            colon_index = value.rfind(":")
            if colon_index < 0:
                value += ":latest"
            if not value or not is_image_name(value):
                msg = '[bright_red]Please enter a valid image name: '
                continue
            if is_priv_image:
                # get string before the last slash line
                value_list = value[:value.rfind(":")].split('/')
                if len(value_list) >= 2:
                    username = value_list[-2]
                else:
                    username = self.console.input('[bright_green]Please input the username of you repository for private image: ')
                password = Prompt.ask('[bright_green]Please input the access token(recommended) or password', password=True)
            if not check_image_func(value, provider_host, username, password):
                self.console.print('[bright_red]Check Image Failed! Please check your image name and try again.')
                msg = '[bright_green]Please enter the image name on Docker Hub or Github Container Registry: '
                continue
            image_name = value
        image_info = {
            'name': image_name,
            'username': username,
            'password': password            
        }
        return image_info

    # service_options: used to get region and portSpecification
    # container_configs: used to judge whether port is already used
    def get_ports(self, container_name: str, container_host_num: int, service_options: dict, container_configs: list, provider_host: str, check_port_func: callable) -> list:
        is_specified_port = service_options.get("portSpecification") == "User Specified Service Port"
        region = service_options.get("region")

        port_configs = []
        self.console.print(f'{container_host_num} port(s) will be set for {container_name}')
        for x in range(container_host_num):
            self.console.print(f'[bright_green]Container and host port {x + 1}:')
            container_port = self.get_container_port(port_configs, container_configs)
            port_config = {
                "containerPort": container_port
            }
            if is_specified_port:
                host_port = self.get_host_port(region, provider_host, port_configs, container_configs, check_port_func)
                port_config["hostPort"] = host_port
            protocol = self.get_port_protocol()
            if protocol:
                port_config["protocol"] = protocol
            port_configs.append(port_config)
        return port_configs

    def get_envs(self):
        env_list = []
        env_num = 0
        while True:
            result = self.console.input("Please input the number of env params you want to set (optional): ").strip()
            if result == '':
                break
            if not result.isdigit():
                self.console.print('[bright_red]Invalid input, please input number. ')
                continue
            env_num = int(result)
            break
        if env_num > 0:
            for i in range(env_num):
                name = ''
                value = ''
                while True:
                    try:
                        name = self.console.input(f"Please enter the name for env {i+1}(symbols only contain '-', '.', '_' and cannot start with a number): ").strip(" ")
                        if is_valid_env_name(name):
                            value = self.console.input(f"Please enter the value for {name}: ").strip(" ")
                            break
                    except Exception as e:
                        print('Env error')
                env = {
                    "name": name,
                    "value": value
                }
                env_list.append(env)
        return env_list

    def get_port_protocol(self) -> str:
        protocol_list = ['TCP', 'UDP']
        protocol = ''
        while protocol not in protocol_list:
            protocol = self.console.input('Please enter the host protocol(TCP or UDP, default TCP): ').strip().upper()
            if protocol in protocol_list or protocol == '':
                return protocol
            self.console.print('[bright_red]Invalid protocol.')

    def get_container_port(self, ports_configs: list, container_configs: list) -> int:
        value = 0
        while value <= 0 or value > 65535:
            try:
                value = int(self.console.input('[bright_green]Please enter the container port(1-65535): '))
                # check repetition
                for config in ports_configs:
                    if config["containerPort"] == value:
                        self.console.print('[bright_red]Container port cannot be repetitive! Please use another port.')
                        value = 0
                # check ports config in other containers
                for container_config in container_configs:
                    port_list = container_config["ports"]
                    for config in port_list:
                        if config["containerPort"] == value:
                            self.console.print('[bright_red]Container port cannot be repetitive! Please use another port.')
                            value = 0
            except ValueError:
                self.console.print('[bright_red]Invalid port number.')
                value = 0
        return value

    def get_host_port(self, region: str, provider_host: str, ports_configs: list, container_configs: list, check_port_func: callable) -> int:
        value = 0
        msg = '[bright_green]Please enter the host port(1-65535): '
        is_valid = False
        is_used = None
        while (not is_valid) or is_used:
            try:
                value = int(self.console.input(msg))
                # check port valid
                is_valid = value > 0 and value <= 65535
                if not is_valid:
                    msg = '[bright_red]Please use a valid port number within the range of 1 - 65535: '
                    continue
                # check if port is already used
                is_used = False
                for config in ports_configs:
                    if config["hostPort"] == value:
                        is_used = True
                # if not used, continue to check port config in other containers
                if not is_used:
                    for container_config in container_configs:
                        port_list = container_config["ports"]
                        for config in port_list:
                            if config["hostPort"] == value:
                                is_used = True
                if is_used:
                    self.console.print('[bright_red]Host port cannot be repetitive! Please use another port.')
                    continue
                resp = check_port_func([value], region, provider_host)
                status = resp.get("status", None)
                is_valid = status is None or status == "NotOccupied"
                if not is_valid:
                    msg = '[bright_red]The inputted port has been occupied. Please change the host port: '
            except ValueError as e:
                print(e)
                msg = '[bright_red]Please enter a valid integer: '
                value = 0
        return value

    def get_config_path(self) -> str:
        msg = "Please set config mounted path inside container (optional) (example: /config/config.yaml): "
        config_path = self.console.input(msg)
        while not is_valid_path(config_path) and config_path != "":
            config_path = self.console.input("[bright_red]Config path is invalid. Please input again: ")
        return config_path

    def get_mount_path(self) -> str:
        msg = "[bright_green]Please enter the directory to mount the data: "
        mount_path = self.console.input(msg)
        while not is_valid_path(mount_path) and mount_path != "":
            mount_path = self.console.input("[bright_red]Mount path is invalid: ")
        return mount_path
