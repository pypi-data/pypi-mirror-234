import json

from v_cloud_market_cli_common.utils.wallet_storage import get_cache_file_path

class CartService:


    def load_cart_from_file(self):
        json_data = {}
        file_path = get_cache_file_path('cart_data.json')
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
        except Exception as e:
            print(f'Load cart cache file failed {e}')
        return json_data

    def save_cart_to_file(self, data: dict):
        file_path = get_cache_file_path('cart_data.json')
        with open(file_path, 'w+') as file:
            try:
                data_str = json.dumps(data)
                file.write(data_str)
            except Exception as e:
                print(f'save data failed {e}')
