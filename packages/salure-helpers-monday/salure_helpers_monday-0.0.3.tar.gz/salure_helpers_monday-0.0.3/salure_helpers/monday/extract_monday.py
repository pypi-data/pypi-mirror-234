import os
import sys
import pandas as pd

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


class ExtractMonday(SalureConnect):

    def __init__(self, label: Union[str, List], debug: bool = False):
        """
        For the full documentation, see: https://developer.monday.com/api-reference/docs/basics
        """

        super().__init__()
        self.headers = self.__get_headers(label=label)
        self.endpoint = "https://api.monday.com/v2/"

    def __get_headers(self, label):
        credentials = self.get_system_credential(system='monday', label=label)
        api_key = credentials['api_key']
        headers = {
            'Authorization': f"Bearer {api_key}",
            'Content-Type': 'application/json'
        }

        return headers

    def get_users(self):
        continue_loop = True
        page = 0
        df = pd.DataFrame()
        while continue_loop:
            page += 1
            payload = json.dumps({
                "query": f"query {{users (limit:50 page:{page}) {{id name created_at email is_admin is_guest is_view_only is_pending enabled join_date title last_activity account {{id}} }} }}"
            })
            response = requests.request("POST", self.monday_url, headers=self.headers, data=payload)
            response_length = len(response.json()['data']['users'])
            if response_length > 0:
                df_temp = pd.json_normalize(response.json()['data']['users'])
                df = pd.concat([df, df_temp], axis=0)
            if response_length < 50:
                continue_loop = False
        return df
