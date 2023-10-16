import json
import requests
from typing import Union, List
from salure_helpers.salureconnect import SalureConnect


class Tempo(SalureConnect):
    def __init__(self, label: Union[str, List], debug=False):
        super().__init__()
        self.debug = debug
        credentials = self.get_system_credential(system='tempo-timesheets', label=label)
        self.headers = {
            "Authorization": f"Bearer {credentials['api_token']}",
            "Content-Type": "application/json"
        }
        if self.debug:
            print(self.headers)

    def get_tempo_hours(self, from_date: str = None, to_date: str = None, updated_from: str = None) -> json:
        """
        This function gets hours from Tempo for max 8 backs week
        :param from_date:
        :param to_date:
        :return: json response with results
        """
        total_response = []
        got_all_results = False
        no_of_loops = 0
        parameters = {}
        if from_date is not None:
            parameters.update({"from": from_date})
        if to_date is not None:
            parameters.update({"to": to_date})
        if updated_from is not None:
            parameters.update({"updatedFrom": updated_from})

        while not got_all_results:
            loop_parameters = parameters | {"limit": 1000, "offset": 1000 * no_of_loops}
            response = requests.get('https://api.tempo.io/4/worklogs', headers=self.headers, params=loop_parameters)
            if response.status_code == 200:
                response_json = response.json()
                no_of_loops += 1
                got_all_results = False if int(response_json['metadata']['count']) == 1000 else True
                total_response += response_json['results']
            else:
                raise ConnectionError(f"Error getting worklogs from Tempo: {response.status_code, response.text}")

        if self.debug:
            print(f"Received {len(total_response)} lines from Tempo")

        return total_response