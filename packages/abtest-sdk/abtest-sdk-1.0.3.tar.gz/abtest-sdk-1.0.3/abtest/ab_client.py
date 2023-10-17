import copy
import threading
import requests
import json
from threading import Thread, Event

from abtest import proto, const


class ABClient:
    def __init__(self):
        self.ab_adapter = requests.Session()
        self.type_mask = 0
        self.info_map = {}
        self.interval = 60  # in seconds
        self.ticker = None
        self.ut = 0
        self.server_unavailable_ticks = 0
        self.ticks_to_skip = 0
        self.mutex = threading.Lock()
        self.close_event = Event()
        self.err_count = 0
        self.hostport = ""
        self.project_id = 0

    def open(self, hostport, interval, project_id):
        if self.is_running():
            return self
        self.close_event.clear()
        self.ab_adapter = requests.Session()
        self.project_id = project_id
        self.hostport = hostport
        self.interval = interval

        # print(f"Open hostport: {self.hostport}, interval: {self.interval}")

        if self.ticker:
            self.ticker.cancel()
        self.ticker = threading.Timer(self.interval, self.update)
        self.ticker.start()

        self.info_map = {}
        self.update()

        return self

    def is_running(self):
        return self.ticker and not self.close_event.is_set()

    def update(self):
        remote_info_map, err = self.remote_info_map()
        if err:
            return

        if not remote_info_map:
            return

        #print(f"{len(remote_info_map)} project experiment(s) to update")

        self.err_count = 0
        with self.mutex:
            local_info_map = self.info_map.get(self.project_id, {})

            for project_id, exp in local_info_map.items():
                if project_id not in remote_info_map:
                    remote_info_map[project_id] = exp
                else:
                    info_map = remote_info_map[project_id]
                    for exp_name, info in exp.items():
                        if exp_name not in info_map:
                            info_map[exp_name] = info

                    remote_info_map[project_id] = info_map

            self.info_map = remote_info_map

    def remote_info_map(self):
        project_info_map = {}

        param = {"time": self.ut}

        try:
            resp = self.get_config_list(param)
            if resp.get("ret") != 1 or not resp.get("data"):
                raise Exception(f"unexpected resp: {resp}")

            for project_id, exp_list in resp["data"]["config_list_map"].items():
                info_map = {}
                for info in exp_list:
                    info_map[info["name"]] = info
                project_info_map[project_id] = info_map

            self.ut = resp["data"]["time"]

        except Exception as e:
            return None, e

        return project_info_map, None

    def close(self):
        if not self.is_running():
            return

        self.close_event.set()
        self.ticker.cancel()
        self.ticker = None

    def get_config(self, user_id):
        result = {}
        if not self.is_running():
            return None

        info_map = self.info_map.get(self.project_id, {})
        for exp_name, info in info_map.items():
            if info.get("status") == proto.ExperimentStatus.Disabled:
                continue

            exp_config = self.get_experiment(user_id, exp_name)
            if exp_config:
                result.update(exp_config)

        return result

    def get_experiments(self, user_id):
        experiments = {}
        if not self.is_running():
            return None

        info_map = self.info_map.get(self.project_id, {})
        for exp_name, info in info_map.items():
            if info.get("status") == proto.ExperimentStatus.Disabled:
                continue

            exp_config = self.get_experiment(user_id, exp_name)
            if exp_config:
                experiments[exp_name] = exp_config

        return experiments

    def get_experiment(self, user_id, exp_name):
        result = {}
        if not self.is_running():
            return None
        info_map = self.info_map.get(str(self.project_id), {})
        info = info_map.get(exp_name)
        if not info:
            return None
        if info.get("status") == proto.ExperimentStatus.Disabled:
            return None

        experiment_info = proto.ExperimentInfo(info)
        return experiment_info.GetConfig(user_id)

    def get_key(self, user_id, exp_name, key_name, result):
        if not self.is_running():
            return

        try:
            config = self.get_experiment(user_id, exp_name)
            if not config:
                return

            if key_name not in config:
                raise ValueError("key not found")

            val = config.get(key_name, result)
            if type(val) == type(result):
                result = copy.deepcopy(val)
            else:
                raise ValueError("the val type does not match")


        except Exception as e:
            print(f"Error in GetKey: {e}")
        return result

    def api_request(self, url, http_body):
        try:
            headers = {"Content-Type": "application/json"}
            response = self.ab_adapter.post(url, data=http_body, headers=headers)
            response.raise_for_status()
            return response.content

        except Exception as e:
            print(f"apiRequest err: {e}")
            return None

    def get_config_list(self, param):
        url = f"{self.hostport}{const.DEFAULT_AB_API_PATH}"
        data = json.dumps(param)
        resp = self.api_request(url, data)
        if resp:
            return json.loads(resp.decode('utf-8'))
        return {}
