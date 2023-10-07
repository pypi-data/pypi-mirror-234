from typing import List
from .types import ProcessInfo, SystemData, GPUInfo


class SystemInfo:
    """
    #   https://chromedevtools.github.io/devtools-protocol/tot/SystemInfo/
    """
    __slots__ = ("_connection",)

    def __init__(self, conn) -> None:
        from ...connection import Connection

        self._connection: Connection = conn

    async def getSystemInfo(self) -> SystemData:
        """
        Возвращает информацию о системе.
        https://chromedevtools.github.io/devtools-protocol/tot/SystemInfo/#method-getInfo
        :return:
        """
        result = await self._connection.call("SystemInfo.getInfo")
        return SystemData(
            gpu=GPUInfo(**result["gpu"]), modelName=result["modelName"],
            modelVersion=result["modelVersion"], commandLine=result["commandLine"]
        )

    async def getProcessInfo (self) -> List[ProcessInfo]:
        """
        Возвращает информацию обо всех запущенных в системе процессах.
        https://chromedevtools.github.io/devtools-protocol/tot/SystemInfo/#method-getProcessInfo
        :return:
        """
        result = await self._connection.call("SystemInfo.getProcessInfo")
        return [ProcessInfo(**i) for i in result]
