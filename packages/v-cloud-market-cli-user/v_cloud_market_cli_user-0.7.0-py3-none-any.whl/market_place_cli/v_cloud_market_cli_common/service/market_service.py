import json

from v_cloud_market_cli_common.config.server_config import API_VERSION
from v_cloud_market_cli_common.utils.wallet_storage import get_cache_file_path
from .service_common import ServiceCommon

from market_place_cli.v_cloud_market_cli_common.service.service_common import GlobalState

class ServiceTypeQueryParam:
    provider = ''
    category = ''
    name = ''
    current = 1
    page_size = 10

    def as_dict(self) -> dict:
        return {
            'provider': self.provider,
            'category': self.category,
            'name': self.name,
            'current': self.current,
            'pageSize': self.page_size
        }

class MarketService:

    def __init__(self):
        self.state = GlobalState()
        self.cli = self.state.server_wrapper
        self.baseRoute = API_VERSION + '/service'

    def get_service_info_page(self, opt, current=1, page_size=10):
        route = self.baseRoute + '/type'
        opts = {
            'current': current,
            'pageSize': page_size,
            'category': opt['category']
        }
        opts.update(opt)
        opts = {k: v for k, v in opts.items() if v}
        resp = self.cli.get_request(route, url_param=opts, needAuth=False)
        ServiceCommon.validate_response(resp)
        return resp

    def get_category_info_page(self, opt, current=1, page_size=10):
        route = self.baseRoute + '/category'
        opts = {
            'current': current,
            'pageSize': page_size
        }
        opts.update(opt)
        opts = {k: v for k, v in opts.items() if v is not None}
        resp = self.cli.get_request(route, url_param=opts, needAuth=False)
        ServiceCommon.validate_response(resp)
        return resp

    def get_provider_info_page(self, opt, current=1, page_size=10):
        route = self.baseRoute + '/provider'
        opts = {
            'current': current,
            'pageSize': page_size
        }
        opts.update(opt)
        opts = {k: v for k, v in opts.items() if v is not None}
        resp = self.cli.get_request(route, url_param=opts, needAuth=False)
        ServiceCommon.validate_response(resp)
        return resp

    def get_provider_service_type(self, opt, current=1, page_size=10):
        route = self.baseRoute + "/type"
        opts = {
            'current': current,
            'pageSize': page_size
        }
        opts.update(opt)
        opts = {k: v for k, v in opts.items() if v is not None}
        resp = self.cli.get_request(route, url_param=opts, needAuth=False)
        ServiceCommon.validate_response(resp)
        return resp

    def get_service_info(self, service_id):
        route = self.baseRoute + f'/type/{service_id}'
        resp = self.cli.get_request(route)
        ServiceCommon.validate_response(resp)
        return resp

    def get_service_category(self, category_id):
        route = self.baseRoute + f'/category/{category_id}'
        resp = self.cli.get_request(route)
        ServiceCommon.validate_response(resp)
        return resp

    def get_service_provider(self, provider):
        route = self.baseRoute + f'/provider/{provider}'
        resp = self.cli.get_request(route)
        ServiceCommon.validate_response(resp)
        return resp

    def query_service_info(self, params: ServiceTypeQueryParam):
        route = self.baseRoute + f'/type'
        resp = self.cli.get_request(route, params.as_dict())
        ServiceCommon.validate_response(resp)
        return resp

    def make_orders(self, payload: dict):
        '''
        return
        id - order id
        recipient - Vsys address of merchant to be paid
        amount: Amount of current order
        '''
        orderRoute = API_VERSION + '/order/add'
        resp = self.cli.post_request(orderRoute, body_data=payload, needAuth=True)
        ServiceCommon.validate_response(resp)
        return resp

    def get_provider_host(self, provider: str) -> str:
        route = self.baseRoute + '/provider/' + provider

        # get provider host
        provider_cache_file = get_cache_file_path('provider_cache.json')
        # create cache file if not exist
        with open(provider_cache_file, 'a+') as cache:
            try:
                # set file position at 0 and read file
                cache.seek(0)
                hold = json.load(cache)
            except json.JSONDecodeError:
                hold = {}
            if provider in hold and hold[provider]:
                return hold[provider]
            else:
                resp = self.cli.get_request(route)
                ServiceCommon.validate_response(resp)
                hold[provider] = resp['apiHost']
                if hold[provider]:
                    # clean cache file and write data
                    cache.truncate(0)
                    json.dump(hold, cache)
                return hold[provider]

    def enough_balance(self, payAmount):
        account = self.state.get_current_account()
        info = account.balance_detail()
        if info is None or info['available'] < payAmount:
            return False
        return True

    def find_price_set(self, durations, options):
        for duration in durations:
            found = True
            for opt in duration['chargingOptions'].values():
                found = opt in options.values() and found
            if found:
                return duration
