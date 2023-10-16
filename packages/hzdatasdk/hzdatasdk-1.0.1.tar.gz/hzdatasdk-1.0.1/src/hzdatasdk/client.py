# coding=utf-8

import threading
import grpc
import json
import msgpack
import numpy as np
import pandas as pd
# import hzdata_pb2
# import hzdata_pb2_grpc
from . import hzdata_pb2
from . import hzdata_pb2_grpc
import six
import zlib

from pandas.compat.pickle_compat import pkl, Unpickler, load as _load

MAX_MESSAGE_LENGTH = 20 * 1024 * 1024


class HZDataClient(object):
    _threading_local = threading.local()
    _default_addr = "10.28.2.133:10001"

    @classmethod
    def instance(cls):
        _instance = getattr(cls._threading_local, '_instance', None)
        if _instance is None:
            _instance = HZDataClient()
            cls._threading_local._instance = _instance
        return _instance

    def __init__(self):
        print("create HZDataClient object.")

    @classmethod
    def convert_message(cls, msg):
        if isinstance(msg, dict):
            data_type = msg.get("type", None)
            data_value = msg.get("value", None)
            if data_type is not None and data_value is not None:
                params = data_value
                if data_type.startswith("pandas"):
                    data_index_type = params.pop("index_type", None)
                    if data_index_type == "Index":
                        params["index"] = pd.Index(params["index"])
                    elif data_index_type == "MultiIndex":
                        params["index"] = (
                            pd.MultiIndex.from_tuples(params["index"])
                            if len(params["index"]) > 0 else None
                        )
                    if data_type == "pandas_dataframe":
                        dtypes = params.pop("dtypes", None)
                        msg = pd.DataFrame(**params)
                        if dtypes:
                            msg = msg.astype(dtypes, copy=False)
                    elif data_type == "pandas.core.series.Series":
                        msg = pd.Series(**params)
            else:
                msg = {
                    key: cls.convert_message(val)
                    for key, val in msg.items()
                }
        return msg

    def __call__(self, method, **kwargs):
        # 参数打包
        request = hzdata_pb2.HZDataRequest()
        request.methodName = method
        request.params = msgpack.packb(kwargs)

        # rpc请求
        channel = grpc.insecure_channel(self._default_addr, options=[
            ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH)
        ])
        stub = hzdata_pb2_grpc.HZDataStub(channel)
        response = stub.HZDataQuery(request)

        # 是否触发异常
        if len(response.errMsg) > 0:
            raise Exception(response.errMsg)

        # 参数解包
        buffer = zlib.decompress(response.datas)
        file = six.BytesIO()
        file.write(buffer)
        msg = _load(file, encoding="latin1")

        return self.convert_message(msg)

    def __getattr__(self, method):
        return lambda **kwargs: self(method, **kwargs)
