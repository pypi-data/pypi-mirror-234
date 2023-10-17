from market_place_cli.v_cloud_market_cli_common.config.server_config import API_VERSION
from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState, ServiceCommon

class VersionService:

    def __init__(self):
        self.cli = GlobalState().server_wrapper

    def get_version(self):
        route = API_VERSION + '/cli/version/latest'
        resp = GlobalState().server_wrapper.get_request(route)
        ServiceCommon.validate_response(resp)
        return resp
