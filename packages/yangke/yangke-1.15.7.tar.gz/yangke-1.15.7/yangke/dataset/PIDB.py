import os.path
import traceback

import pandas as pd

from yangke.common.config import logger
from yangke.core import runCMD


class PIDB:
    def __init__(self, ip=None):
        self.ip = ip
        self.PI_API = os.path.abspath(os.path.join(os.path.dirname(__file__), "PIAPI", "net6", "PIAPI.exe"))

    def get_snapshot(self, tags, description=None):
        """
        从PI数据库中读取快照值

        :param tags:
        :param description: 点的描述，如果传入描述，则返回的测点标题是描述，否则测点标题是标签名
        :return:
        """
        try:
            cmd = f"{self.PI_API} getsnapshot \"{tags}\""
            output, err = runCMD(cmd, wait_for_result=True)
            res = output
            res_dict = {}
            for line in res.split("\r"):
                line: str = line.strip()
                if line.startswith("#") or line == "":
                    continue
                tag, value = line.split("=")
                if tag in tags:
                    res_dict.update({tag.strip(): float(value)})
            df = pd.DataFrame(data=res_dict.values(), index=list(res_dict.keys())).T
            df.rename(columns=dict(zip(tags, description)), inplace=True)
            return df
        except:
            traceback.print_exc()

    def write_snapshot(self, tags, values):
        try:
            data_ = dict(zip(tags, values))
            cmd = f"{self.PI_API} writesnapshot \"{data_}\""
            runCMD(cmd)
        except:
            traceback.print_exc()
