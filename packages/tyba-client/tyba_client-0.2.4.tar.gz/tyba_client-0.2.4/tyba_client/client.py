import pandas as pd
from requests import Response

from tyba_client.models import GenerationModel, PVStorageModel, StandaloneStorageModel
from generation_models import JobModel
import json
import requests
import time
from structlog import get_logger
from typing import Callable

logger = get_logger()


class Ancillary(object):
    """

    """
    def __init__(self, prices):
        self.prices = prices

    def get(self, route, params=None):
        return self.prices.get(f"ancillary/{route}", params=params)

    def get_pricing_regions(self, *, iso, service, market):
        return self.get("regions", {"iso": iso,
                                    "service": service,
                                    "market": market})

    def get_prices(self, *, iso, service, market, region, start_year, end_year):
        return self.get("prices", {"iso": iso,
                                   "service": service,
                                   "market": market,
                                   "region": region,
                                   "start_year": start_year,
                                   "end_year": end_year})


class LMP(object):
    """

    """
    def __init__(self, prices):
        self.prices = prices

    def get(self, route, params=None):
        return self.prices.get(f"lmp/{route}", params=params)

    def get_all_nodes(self, *, iso):
        return self.get("nodes", {"iso": iso})

    def get_prices(self, *, node_ids, market, start_year, end_year):
        return self.get("prices", {"node_ids": json.dumps(node_ids),
                                   "market": market,
                                   "start_year": start_year,
                                   "end_year": end_year})


class Services(object):
    """

    """
    def __init__(self, client):
        self.client = client
        self.ancillary = Ancillary(self)
        self.lmp = LMP(self)

    def get(self, route, params=None):
        return self.client.get(f"services/{route}", params=params)

    def get_all_isos(self):
        return self.get("isos")


class Client(object):
    """Tyba valuation client class"""

    DEFAULT_OPTIONS = {
        'version': '0.1'
    }

    def __init__(self, personal_access_token, host="https://dev.tybaenergy.com", request_args=None):
        """A :class:`Client` object for interacting with Tyba's API.
        """
        self.personal_access_token = personal_access_token
        self.host = host
        self.services = Services(self)
        self.request_args = {} if request_args is None else request_args

    def _auth_header(self):
        return self.personal_access_token

    def _base_url(self):
        return self.host + "/public/" + self.DEFAULT_OPTIONS["version"] + "/"

    def get(self, route, params=None):
        return requests.get(self._base_url() + route,
                            params=params,
                            headers={"Authorization": self._auth_header()},
                            **self.request_args)

    def post(self, route, json):
        return requests.post(self._base_url() + route,
                             json=json,
                             headers={"Authorization": self._auth_header()},
                             **self.request_args
                             )

    def schedule_pv(self, pv_model: GenerationModel):
        model_json_dict = pv_model.to_dict()
        return self.post("schedule-pv", json=model_json_dict)

    def schedule_storage(self, storage_model: StandaloneStorageModel):
        model_json_dict = storage_model.to_dict()
        return self.post("schedule-storage", json=model_json_dict)

    def schedule_pv_storage(self, pv_storage_model: PVStorageModel):
        model_json_dict = pv_storage_model.to_dict()
        return self.post("schedule-pv-storage", json=model_json_dict)

    def schedule(self, model: JobModel):
        return self.post("schedule-job", json=model.dict())

    def get_status(self, run_id: str):
        url = "get-status/" + run_id
        return self.get(url)

    def get_status_v1(self, run_id: str):
        return self.get(f"get-status/{run_id}", params={"fmt": "v1"})

    @staticmethod
    def _wait_on_result(run_id: str, wait_time: int, log_progress: bool, getter: Callable[[str], Response]):
        while True:
            resp = getter(run_id)
            resp.raise_for_status()
            res = resp.json()
            if res["status"] == "complete":
                return res["result"]
            elif res["status"] == "unknown":
                raise UnknownRunId(f"No known model run with run_id '{run_id}'")
            message = {
                "status": res["status"]
            }
            if res.get("progress") is not None:
                message["progress"] = f"{float(res['progress']) * 100:3.1f}%"
            if log_progress:
                logger.info("waiting on result", **message)
            time.sleep(wait_time)

    def wait_on_result(self, run_id: str, wait_time: int = 5, log_progress: bool = False):
        return self._wait_on_result(run_id, wait_time, log_progress, getter=self.get_status)

    def wait_on_result_v1(self, run_id: str, wait_time: int = 5, log_progress: bool = False):
        res = self._wait_on_result(run_id, wait_time, log_progress, getter=self.get_status_v1)
        return parse_v1_result(res)


def parse_v1_result(res: dict):
    return {
        "hourly": pd.concat({k: pd.DataFrame(v) for k, v in res["hourly"].items()}, axis=1),
        "waterfall": res["waterfall"]
    }


class UnknownRunId(ValueError):
    pass
