import time

import numpy as np
from waveforms import Waveform, wave_eval, WaveVStack
from waveforms.math.signal import getFTMatrix, shift

from .common import BaseDriver, Quantity


def get_coef(coef_info, sampleRate):
    start, stop = coef_info['start'], coef_info['stop']
    numberOfPoints = int(
        (stop - start) * sampleRate)
    if numberOfPoints % 1024 != 0:
        numberOfPoints = numberOfPoints + 1024 - numberOfPoints % 1024
    t = np.arange(numberOfPoints) / sampleRate + start

    fList = []
    wList = []
    phases = []

    for kw in coef_info['wList']:
        Delta, t0, weight, w, phase = kw['Delta'], kw['t0'], kw['weight'], kw['w'], kw['phase']
        fList.append(Delta)

        if w is not None:
            w = np.zeros(numberOfPoints, dtype=complex)
            w[:len(w)] = w
            w = shift(w, t0 - start)
            phases.append(np.mod(phase + 2 * np.pi * Delta * start, 2*np.pi))
        else:
            weight = weight
            if isinstance(weight, np.ndarray):
                pass
            else:
                if isinstance(weight, str):
                    fun = wave_eval(weight) >> t0
                elif isinstance(weight, Waveform):
                    fun = weight >> t0
                else:
                    raise TypeError(f'Unsupported type {weight}')
                weight = fun(t)
            phase += 2 * np.pi * Delta * start
            w = getFTMatrix([Delta],
                            numberOfPoints,
                            phaseList=[phase],
                            weight=weight,
                            sampleRate=sampleRate)[:, 0]
            phases.append(np.mod(phase, 2*np.pi))
        wList.append(w)
    return np.asarray(wList), fList, numberOfPoints, phases


# class Quantity(object):
#     def __init__(self, name: str, value=None, ch: int = None, unit: str = ''):
#         self.name = name
#         self.default = dict(value=value, ch=ch, unit=unit)


def tolist(wv: WaveVStack) -> list:
    """将波形序列wv转为list

    Args:
        wv (WaveVStack): 波形序列

    Returns:
        list: list描述的波形序列
    """
    ret = [wv.start, wv.stop, wv.sample_rate, len(wv.wlist)]
    for w in wv.wlist:
        ret.extend(w.tolist())
    return ret


def fromlist(wl: list) -> WaveVStack:
    """从list创建WaveVStack

    Args:
        wl (list): 见tolist返回值

    Returns:
        WaveVStack: 波形序列
    """
    wv, wpos = WaveVStack([]), 4
    wv.start, wv.stop, wv.sample_rate, n = wl[:wpos]
    for _ in range(n):
        wav, pos = Waveform.fromlist(wl[wpos:], True)
        wv.wlist.append(wav)
        wpos += pos
    return wv


class Driver(BaseDriver):
    """设备驱动，类名统一为Driver，文件名为设备名称，如VirtualDevice

    Args:
        BaseDriver (class): 所有的驱动均继承自基类，要求实现
        open/close/read/write四个接口
    """
    segment = ('na', '101|102|103')
    # 设备可用通道数量
    CHs = list(range(36))

    # 设备常见读写属性，可自行增加，对应在read/write中实现不同的方法即可
    # 属性名中的单词均以大写开头，缩写全为大写，用于说明有哪些可读写设置
    # 应给每个属性加上注释，方便了解设置的作用
    quants = [
        # 微波源(MW)
        Quantity('Frequency', value=0, ch=1, unit='Hz'), # 频率，float
        Quantity('Power', value=0, ch=1, unit='dBm'),  # 功率，float
        Quantity('Output', value='OFF', ch=1),  # 输出开关，str

        # 任意波形发生器(AWG)
        Quantity('Amplitude', value=0, ch=1, unit='Vpp'), # 振幅，float
        Quantity('Offset', value=0, ch=1, unit='V'), # 偏置，float
        Quantity('Waveform', value=np.array([]), ch=1), # 波形，np.array
        Quantity('Marker1', value=[], ch=1), # Marker1，np.array
        Quantity('Marker2', value=[], ch=1), # Marker2，np.array

        # 数据采集(ADC)
        Quantity('PointNumber', value=1024, ch=1, unit='point'),  # 采样点数，int
        Quantity('TriggerDelay', value=0, ch=1, unit='s'),  # 采样延迟，float
        Quantity('Shot', value=512, ch=1),  # 采样次数，int
        Quantity('TraceIQ', value=np.array([]), ch=1),  # 时域采样，np.array
        Quantity('Trace', value=np.array([]), ch=1),  # 时域采样，np.array
        Quantity('IQ', value=np.array([]), ch=1),  # 解调后数据，np.array
        Quantity('Coefficient', value=np.array([]), ch=1),  # 解调所需系数，np.array
        Quantity('StartCapture', value=1, ch=1,),  # 开始采集，value随机，通知采集卡准备就绪
        Quantity('CaptureMode', value='raw', ch=1),  # 采集模式，str，raw->TraceIQ, alg-> IQ

        # test
        Quantity('Classify', value=0, ch=1), #
        Quantity('Counts', value=[], ch=1),

        # 触发(TRIG)
        Quantity('TRIG'),
        Quantity('TriggerMode'), # burst or continuous
        Quantity('Wait', value=0, ch=1),  # wait
    ]

    def __init__(self, addr: str = '', timeout: float = 3.0, **kw):
        super().__init__(addr=addr, timeout=timeout, **kw)
        """根据设备地址、超时时间实例化设备驱动
        """
        self.model = 'VirtualDevice' # 默认为设备名字
        self.timeout = 1.0
        self.srate = 1e9 # 设备采样率

    def open(self, **kw):
        """打开并初始化仪器设置，获取仪器操作句柄，必须实现，可以为空(pass)但不能没有
        """
        self.handle = 'DeviceHandler'
        # test = 1/0

    def close(self, **kw):
        """关闭仪器，必须实现，可以为空(pass)但不能没有
        """
        self.handle.close()

    def write(self, name: str, value, **kw):
        """设置仪器，额外的参数(如通道指定)可通过kw传入。必须实现，如

        if name == '属性名':
            执行操作
        elif name == '属性名':
            执行操作
        """
        if name == 'Wait':
            time.sleep(value)
        elif name == 'Waveform':
            # print(np.asarray(value).shape)
            # t = np.random.randint(100,200,1)/1000
            # time.sleep(t[0])
            # print(value)
            if isinstance(value, list):
                t0 = time.time()
                wf = fromlist(value)
                t1 = time.time()
                wf.sample()
                print('sssssssssssssssssssssssssssssssssssssssssssssss',time.time()-t1,t1-t0)
            if isinstance(value, Waveform):
                t0 = time.time()
                value.sample()
                print('sssssssssssssssssssssssssssssssssssssssssssssss',time.time()-t0)
            # 如，self.set_offset(value, ch=1)
        elif name == 'Shot':
            pass
        elif name == 'Coefficient':
            data, f_list, numberOfPoints, phase = get_coef(value, self.srate)
            # coef_data = np.moveaxis([data.real,data.imag],0,-2)
            self.setValue('PointNumber', numberOfPoints, **kw)
            # self.update('Coefficient', data, channel=ch)
            return data
            # 如，self.set_shot(value, ch=2)
        return value

    def read(self, name: str, **kw):
        """读取仪器，额外的参数(如通道指定)可通过kw传入。必须实现，如

        if name == '属性名':
            return 执行操作
        elif name == '属性名':
            return 执行操作
        """
        if name == 'TraceIQ':
            shot = self.getValue('Shot', **kw)
            point = self.getValue('PointNumber', **kw)
            # test = 1/0
            return np.ones((shot, point)), np.ones((shot, point))
        elif name == 'IQ':
            shot = self.getValue('Shot', **kw)
            fnum = self.getValue('Coefficient', **kw).shape[0]
            # time.sleep(0.1)
            return np.random.random((shot, fnum)), np.random.random((shot, fnum))

    # *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# user defined #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
    def get_iq(self):
        pass

    def get_trace(self):
        pass
