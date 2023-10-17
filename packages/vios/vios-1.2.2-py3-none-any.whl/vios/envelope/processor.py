"""仪器操作的结果(read操作返回见各设备驱动, write操作返回None)传给process进行处理
"""


import numpy as np
from lib.arch import baqisArchitecture
from waveforms.qlisp import get_arch, register_arch

register_arch(baqisArchitecture)


def demodulate(raw_data, **kwds):
    pass


def process(raw_data, **kwds):
    """处理数据

    Args:
        raw_data (dict): 从设备获取的原始结果

    Returns:
        dict: 处理后的数据, 形式为{'key1':np.array,'key2':np.array, ...}
    """
    # print('ddddddddddoooooooooooooooooooooo', kwds)
    # print("=============================================",raw_data)

    dataMap = kwds.get('dataMap', {'arch': 'baqis'})
    result = {}

    try:

        if 'arch' in dataMap and dataMap['arch'] == 'general':
            return raw_data['READ']['AD']
        elif list(dataMap.keys()) == ['arch']:  # for NA
            if 'READ' in raw_data:
                print(raw_data)
                nadata = result['data'] = raw_data['READ']['NA']
                if 'CH1.Trace' in nadata:
                    result['data'] = raw_data['READ']['NA'].pop('CH1.Trace')
                elif 'CH1.S' in nadata:
                    result['data'] = raw_data['READ']['NA'].pop('CH1.S')
            result['extra'] = raw_data
        else:
            result = get_arch(dataMap['arch']).assembly_data(raw_data, dataMap)
    except Exception as e:
        print('>'*10, 'Failed to process the result', e, '<'*10)
        result['error'] = [
            f'Failed to process the result, raise Exception: {e.__class__.__name__}("{str(e)}")',
            raw_data,
            dataMap
        ]

    for k, v in result.items():
        result[k] = np.asarray(v)

    return result

