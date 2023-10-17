import hashlib
import json
import re
import time

from abtest import const

class ExperimentType:
    RecExperiment = 1
    AllExperiment = 2

class ExperimentStatus:
    Enabled = 1
    Disabled = -1


class ExperimentInfo:
    def __init__(self, data):
        self.ExpID = data.get("exp_id")
        self.Name = data.get("name")
        self.ExpType = data.get("exp_type")
        self.Ut = data.get("ut")
        self.PartitionCount = data.get("partition_count")
        self.Status = data.get("status")
        self.Expire = data.get("expire")
        self.Version = data.get("version")

        self.WhiteMap = data.get("white_map")
        self.ConfigMap = data.get("config_map")
        self.ConfigRawMap = data.get("config_raw_map")
        self.PartitionsMap = data.get("partitions_map")
        self.StrategyNameTable = [''] * self.PartitionCount
        if self.PartitionCount > 0:
            pars = IntervalList()
            for strategyName, v in self.PartitionsMap.items():
                partitions = v
                self.PartitionsMap[strategyName] = partitions
                pars.Init(partitions, self.PartitionCount)
                for index in pars.Array():
                    self.StrategyNameTable[index] = strategyName

    def GetStrategy(self, id):
        if self.WhiteMap is None:
            raise ValueError("whiteMap is None")

        strategyName = self.WhiteMap.get(id)
        if strategyName:
            return strategyName
        if self.PartitionCount > 0 and len(self.StrategyNameTable) == self.PartitionCount:
            index = self.HashIndex(self.ExpID, id, self.PartitionCount)
            strategyName = self.StrategyNameTable[index]

        if not strategyName:
            strategyName = "default"

        return strategyName

    def GetConfig(self, id):
        result = {}
        strategyName = self.GetStrategy(id)
        if self.ConfigMap is None:
            raise ValueError("configMap is None")
        if strategyName in self.ConfigMap:
            result = self.ConfigMap[strategyName]

        return result

    def GetDefaultConfig(self):
        result = {}
        if self.ConfigMap is None:
            raise ValueError("configMap is None")

        if const.DEFAULT_STRATEGY_NAME in self.ConfigMap:
            result = self.ConfigMap[const.DEFAULT_STRATEGY_NAME]

        return result

    def GetRawConfigs(self):
        data = {}
        if self.ConfigRawMap is None:
            raise ValueError("configRawMap is None")

        for k, v in self.ConfigRawMap.items():
            data[k] = v.encode()

        return data

    def GetRawConfig(self, id):
        if self.ConfigRawMap is None:
            raise ValueError("configRawMap is None")

        strategyName = self.GetStrategy(id)
        data = self.ConfigRawMap.get(strategyName, "")

        return data.encode()

    def HashIndex(self, expID, id, total_count):
        combined_str = expID + id
        hash_object = hashlib.md5(combined_str.encode())
        hash_hex = hash_object.hexdigest()
        last_bytes = hash_hex[24:]
        index = int(last_bytes, 16) % total_count
        return index

class IntervalList:
    def __init__(self):
        self.str = ""
        self.max = 0
        self.intervals = []

    def Init(self, s, max_value):
        self.str = ""
        self.max = 0
        self.intervals = []

        if max_value <= 0:
            return

        self.max = max_value
        if not s:
            return

        segments = s.split(",")
        re_range = re.compile("^[0-9]+-[0-9]+$")
        re_number = re.compile("^(0|[1-9][0-9]*)$")

        min_value = -1

        for segment in segments:
            i1, i2 = 0, 0

            if re_range.match(segment):
                # range format: %d-%d
                i1, i2 = map(int, segment.split("-"))

                if i1 <= min_value or i1 > i2:
                    raise ValueError("err near %s, partitions should be monotonic increasing" % segment)

                if i2 >= max_value:
                    raise ValueError("partition: %d should be less than partitionCount: %d" % (i2, max_value))

                min_value = i2

                self.intervals = self.append_interval(self.intervals, i1, i2 + 1)
            elif re_number.match(segment):
                # number format: %d
                i1 = int(segment)

                if i1 <= min_value:
                    raise ValueError("err near %s, partitions should be monotonic increasing" % segment)

                if i1 >= max_value:
                    raise ValueError("partition: %d should be less than partitionCount: %d" % (i1, max_value))

                min_value = i1

                self.intervals = self.append_interval(self.intervals, i1, i1 + 1)
            else:
                raise ValueError("syntax err near %s" % segment)

        self.format_str()

    def append_interval(self, intervals, l, r):
        result = intervals
        length = len(intervals)

        if length > 0 and result[length - 1].Right >= l:
            result[length - 1].Right = r
            return result

        result.append(Interval(Left=l, Right=r))
        return result

    def Array(self):
        array = []
        for interval in self.intervals:
            l, r = interval.Left, interval.Right
            while l < r:
                array.append(l)
                l += 1
        return array

    def format_str(self):
        ss = []
        for interval in self.intervals:
            ss.append(interval.String())
        self.str = ",".join(ss)

class Interval:
    def __init__(self, Left=0, Right=0):
        self.Left = Left
        self.Right = Right

    def String(self):
        if self.Left == self.Right - 1:
            return str(self.Left)
        return "{}-{}".format(self.Left, self.Right - 1)

class ByVersionDesc:
    def __init__(self):
        pass

    @staticmethod
    def Len(s):
        return len(s)

    @staticmethod
    def Swap(s, i, j):
        s[i], s[j] = s[j], s[i]

    @staticmethod
    def Less(s, i, j):
        return s[i].Version > s[j].Version

class DataResp:
    def __init__(self):
        self.Ret = 0
        self.Errcode = 0
        self.Msg = ""
        self.Data = GetConfigListData()

class GetConfigListData:
    def __init__(self):
        self.Time = 0
        self.ConfigListMap = {}
