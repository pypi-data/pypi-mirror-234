import sys
from rich.console import Console

from market_place_cli.v_cloud_market_cli_common.service_display.main_interface import MainInterface
from market_place_cli.v_cloud_market_cli_common.config.wallet_config import AGENT_VERSION
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState

class VersionServiceLogic:

    def __init__(self):
        self.title = "About Vcloud"
        self.state = GlobalState()
        self.console = self.state.console
        self.version_service = self.state.version_service

    @property
    def Name(self):
        return self.title

    def StartLogic(self):
        self.console.clear()
        self.show_version()

    def show_version(self):
        try:
            MainInterface.display_title(self.console, "About Version")
            data = self.version_service.get_version()
            version = data["version"]
            change_log = data["changeLog"]
            if self.need_update(version):
                self.console.print(f'[dark_sea_green4]Your current version:  {AGENT_VERSION}\n' \
                f'The latest version:    {version}\n' \
                f'Latest Change Log:\n{change_log}\n\n' \
                'Use the following command to upgrade:[/]\n' \
                '[red]pip install -U v-cloud-market-cli-user[/]\n')
                self.console.input(f'[dark_sea_green4]Press ENTER to continue...[/]')
                self.console.clear()
            else:
                self.console.print('[dark_sea_green4]No updates available\n' \
                f'Current version: {version}\n' \
                f'Change Log:\n{change_log}[/]\n')
                self.console.input(f'[dark_sea_green4]Press ENTER to continue...[/]')
        except Exception as e:
            self.console.input(f'Get version failed: {e}\nPress ENTER to continue...')

    def check_version(self):
        try:
            data = self.version_service.get_version()
            version = data["version"]
            min_version = data['minimalSupported']
            change_log = data["changeLog"]
            if self.not_support(min_version):
                MainInterface.display_title(self.console, "Not Supportted")
                self.console.print(f'[dark_sea_green4]Your current version:             {AGENT_VERSION}\n' \
                f'The latest version:               {version}\n' \
                f'The minimal supported version:    {min_version}\n\n' \
                'The current version is not supported.\n' \
                'Use the following command to upgrade:[/]\n' \
                '[red]pip install -U v-cloud-market-cli-user[/]\n')
                self.console.input(f'[dark_sea_green4]Press ENTER to exit[/]')
                sys.exit()
            if self.need_update(version):
                MainInterface.display_title(self.console, "Update Available")
                self.console.print(f'[dark_sea_green4]Your current version:  {AGENT_VERSION}\n' \
                f'The latest version:    {version}\n' \
                f'Latest Change Log:\n{change_log}\n\n' \
                'Use the following command to upgrade:[/]\n' \
                '[red]pip install -U v-cloud-market-cli-user[/]\n')
                self.console.input(f'[dark_sea_green4]Press ENTER to continue[/]')
                self.console.clear()
        except Exception as e:
            self.console.print(f'Version Check failed: {e}')

    def compare_version(self, version1, version2):
        # change version to string list
        v1 = [str(x) for x in str(version1).split('.')]
        v2 = [str(x) for x in str(version2).split('.')]
 
        # fill version list with 0
        if len(v1) > len(v2):
            v2 += [str(0) for x in range(len(v1) - len(v2))]
        if len(v1) < len(v2):
            v1 += [str(0) for x in range(len(v2) - len(v1))]
 
        # sort, small version list first
        list_sort = sorted([v1, v2])
        # judge which is bigger
        if list_sort[0] == list_sort[1]:
            # version1 same as version2
            return 0
        elif list_sort[0] == v1:
            # version1 smaller than version2
            return 1
        else:
            # version1 bigger than version2
            return -1
    def not_support(self, version):
        # AGENT_VERSION < min version, get 1, not support
        if self.compare_version(AGENT_VERSION, version) == 1:
            return True
        return False

    def need_update(self, version):
        # judge new version and current cli agent version
        # AGENT_VERSION < new version, get 1, need update
        if self.compare_version(AGENT_VERSION, version) == 1:
            return True
        return False