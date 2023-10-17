from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.health_pb2 import *
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys
from rich import print

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def check_health(self: GRPCClient):
        result = {}

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: NodeHealthResponse = self.health.Check(
            request=NodeHealthRequest()
        )

        return grpc_return_value
