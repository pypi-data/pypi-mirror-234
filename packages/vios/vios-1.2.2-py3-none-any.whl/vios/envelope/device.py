"""设备驱动独立于测控系统, 本模块接口是设备与系统的交接处(此外还有open/close). 
系统发给设备的所有指令均会经过以下两个函数, 即read和write. 
设备执行结果交由processor模块处理. 
"""

from typing import Any

from ..driver.common import BaseDriver


def read(device: BaseDriver, quantity: str, channel: int = 1, **kwds):
    """从设备读取

    Args:
        device (_type_): 设备
        quantity (str): 设备属性, 如Waveform/Power/Offset
        channel (int, optional): 设备通道. Defaults to 1.

    Returns:
        _type_: 读取结果
    """
    return device.getValue(quantity, ch=channel, **kwds)


def write(device: BaseDriver, quantity: str, value: Any, channel: int = 1, **kwds):
    """向设备写入

    Args:
        device (_type_): 设备
        quantity (str): 设备属性
        value (Any): 待写入的数据
        channel (int, optional): 设备通道. Defaults to 1.
    """
    return device.setValue(quantity, value, ch=channel, **kwds)
