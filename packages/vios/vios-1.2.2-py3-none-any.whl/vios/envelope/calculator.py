"""所有指令都会由此模块进行预处理, 如采样、失真、串扰等, 
并送入设备执行(见device模块)
"""

import numpy as np
from qlisp.kernel_utils import sample_waveform
from waveforms import Waveform, wave_eval


def calculate(step: str, target: str, cmd: list, targets: dict = {}):
    """指令的预处理

    Args:
        step (str): 步骤名, 如main/step1/...
        target (str): 设备通道, 如AWG.CH1.Offset
        cmd (list): 操作指令, 格式为(操作类型, 值, 单位, kwds). 其中
            操作类型包括WRITE/READ/WAIT, kwds见assembler.preprocess说明. 

    Returns:
        tuple: 预处理结果
    
    >>> calculate('main', 'AWG.CH1.Waveform',('WRITE',square(100e-6),'au',{'calibration':{}}))
    """
    ctype, value, unit, kwds = cmd

    line = {}

    if ctype != 'WRITE':
        return (step, target, cmd), line

    if isinstance(value, str):
        try:
            func = wave_eval(value)
        except SyntaxError as e:
            func = value
    else:
        func = value

    delay = 0

    if isinstance(func, Waveform):
        if target.startswith(tuple(kwds.get('filter', ['zzzzz']))):
            support_waveform_object = True
        else:
            support_waveform_object = False
        
        try:
            ch = kwds['target'].split('.')[-1]
            delay = kwds['calibration'][ch].get('delay', 0)
            cmd[1] = sample_waveform(func, kwds['calibration'][ch],
                                    sample_rate=kwds['srate'],
                                    start=0, stop=kwds['LEN'],
                                    support_waveform_object=support_waveform_object)
        except KeyError as e:
            # KeyError: 'calibration'
            func.start = 0
            func.stop = 100e-6
            func.sample_rate = kwds['srate']
            
            if support_waveform_object:
                cmd[1] = func
            else:
                # import time
                # t0 = time.time()
                cmd[1] = func.sample()
                # print(time.time()-t0,33333333333333333333333333333333333333333333333333333333333333333333333333333333)
    else:
        cmd[1] = func

    cmd[-1] = {'sid': kwds['sid'], 'tracking': kwds['tracking'],
               'target': kwds['target'], 'srate': kwds['srate']}
    
    try:
        line = preview(target, cmd, targets, delay)
    except Exception as e:
        print('>'*30, '  failed to calculate waveform', e, type(e).__name__)

    return (step, target, cmd), line


def preview(target:str, cmd: dict, targets: dict = {}, delay: float = 0.0):
    """收集需要实时显示的波形

    Args:
        target (str): 设备.通道.属性, 波形目标地址.
        cmd (dict): 见calculator返回值.
        targets (dict, optional): 即etc.preview(为避免与preview函数同名). Defaults to {}.
        delay (float, optional): 通道延时, 扣除后即为从设备输出的波形. Defaults to 0.0.

    Returns:
        _type_: _description_
    """
    if not targets.get('filter', []):
        return {}

    if cmd[-1]['target'].split('.')[0] not in targets['filter'] or cmd[-1]['sid'] < 0:
        return {}

    if target.endswith('Waveform'):

        srate = cmd[-1]['srate']
        t1, t2 = targets['range']
        xr = slice(int(t1*srate), int(t2*srate))

        val = cmd[1]
        if isinstance(val, Waveform):
            val = val.sample()

        xt = (np.arange(len(val))/srate)[xr] - delay
        yt = val[xr]

        try:
            nz = (np.abs(np.diff(yt))>1e-6).nonzero()[0]
            if targets.get('align', 'right') == 'left':
                xx = np.hstack((xt[:nz[-1]+100], xt[-10:]))
                yy = np.hstack((yt[:nz[-1]+100], yt[-10:]))
            else:
                xx = np.hstack((xt[:100], xt[nz[0]-100:]))
                yy = np.hstack((yt[:100], yt[nz[0]-100:]))
        except Exception as e:
            xx = np.hstack((xt[:100], xt[-100:]))
            yy = np.hstack((yt[:100], yt[-100:]))

        line = {'xdata': xx, 'ydata': yy, 'suptitle': cmd[-1]["sid"]}
        color = targets.get('color', None)
        if color and isinstance(color, (list, tuple)):
            line['color'] = tuple(color)

        return {cmd[-1]['target']: line}
    return {}
                


if __name__ == "__main__":
    import doctest
    doctest.testmod()