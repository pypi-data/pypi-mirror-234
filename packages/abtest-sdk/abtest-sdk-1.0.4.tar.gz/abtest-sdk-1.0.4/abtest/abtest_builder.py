import json

import logging

from abtest import const
from typing import List, Union, Dict, Any

from abtest.ab_client import ABClient

client = ABClient()

def init_client(project_id, kwargs):
    opt = {
        "Hostport": const.DEFAULT_AB_CONFIG_HOST,
        "Interval": const.DEFAULT_INTERVAL_IN_SECOND,
    }
    for key, value in kwargs.items():
        opt[key] = value

    client.open(opt["Hostport"], opt["Interval"], project_id)
    return


def get_config(id):
    config = client.get_config(id)
    return config


def get_experiments(id):
    experiments = client.get_experiments(id)
    return experiments


def get_experiment(id, exp_name):
    exp = client.get_experiment(id, exp_name)
    return exp


def get_key(id, exp_name, key_name, default_val):
    key = client.get_key(id, exp_name, key_name, default_val)
    return key
