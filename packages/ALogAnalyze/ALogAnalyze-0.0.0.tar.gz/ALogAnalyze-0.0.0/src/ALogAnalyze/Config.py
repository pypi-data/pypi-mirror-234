#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#

import json
import os
from datetime import datetime, date

class Config():

    def __new__(self):
        configFile = open(os.path.dirname(__file__) + '/template/config.json')
        config = json.load(configFile)
        # print(json.dumps(config, indent=4))

        return config

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
