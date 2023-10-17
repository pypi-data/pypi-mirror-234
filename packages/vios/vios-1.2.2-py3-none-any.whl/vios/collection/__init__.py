"""本模块主要由工具函数构成, 且依赖server
>>> tasks: 实验描述
>>> task: 任务描述例子
>>> uapi: 与前端进行交互, 如matplotlib画图、数据库查询、实时画图等, 详见各函数说明. 
"""
import asyncio
import inspect
import json
import os
import random
import time
from functools import cached_property
from pathlib import Path

import dill
import h5py
import matplotlib.pyplot as plt
import numpy as np
from kernel.sched.task import App
from quark import connect, loads
from tqdm import tqdm
from waveforms import Waveform, wave_eval
from waveforms.dicttree import flattenDictIter
from waveforms.scan_iter import StepStatus

from .. import Progress, startup

try:
    with open(Path(startup.get('site', '')) / 'etc/bootstrap.json', 'r') as f:
        cfg = json.loads(f.read())['executor']
except Exception as e:
    print(e)
    cfg = {"host": "127.0.0.1", "port": 2088}

print(cfg)
_s = connect('QuarkServer', host=cfg.get('host', '0.0.0.0'), port=cfg.get('port',2088))
_cs = connect('QuarkCanvas', port=2089)
_vs = connect('QuarkViewer', port=2086)


class Task(object):
    """适用于大量任务连续提交(如量子云), 获取任务状态、结果、进度等. 
    Args:
        task (dict): 任务描述
        timeout (float | None, optional):任务最大时长, 默认为None, 即任务执行完毕结束.

    任务样例见本模块下experiment. 使用方法: 
    >>> task = Task(s21) # s21 为task.py中字典描述
    >>> task.run()
    >>> task.bar() # 适用于notebook
    """

    handles = {}

    def __init__(self, task: dict, timeout: float | None = None) -> None:
        """_summary_

        Args:
            task (dict): 任务描述，详见submit函数
            timeout (float | None, optional): 阻塞任务最大时间. Defaults to None.
        """
        self.task = task
        self.timeout = timeout

        self.data: dict[str, np.ndarray] = {} # 从server取回的数据
        self.meta = {} # 坐标轴等描述类信息
        self.index = 0 # 当前已取回的数据数量
        self.last = 0 # 上一次获取的数据量

    @cached_property
    def name(self):
        return self.task['metainfo'].get('name', 'Unknown')

    def run(self):
        self.stime = time.time()  # start time
        try:
            circuit = self.task['taskinfo']['CIRQ']
            if isinstance(circuit, list) and callable(circuit[0]):
                circuit[0] = inspect.getsource(circuit[0])
        except Exception as e:
            print(e)
        self.tid = _s.submit(self.task)

    def cancel(self):
        _s.cancel(self.tid)
        # self.clear()

    def save(self):
        _s.save(self.tid)

    def result(self):
        meta = True if not self.meta else False
        res = _s.fetch(self.tid, start=self.index, meta=meta)

        if isinstance(res, str):
            return self.data
        elif isinstance(res, tuple):
            if isinstance(res[0], str):
                return self.data
            data, self.meta = res
        else:
            data = res
        self.last = self.index
        self.index += len(data)
        # data.clear()
        self.process(data)

        self.plot(not meta)

        return self.data

    def status(self, key: str = 'runtime'):
        if key == 'runtime':
            return _s.track(self.tid)
        elif key == 'compile':
            return _s.apply('status', user='task')
        else:
            return 'supported arguments are: {rumtime, compile}'

    def report(self):
        return _s.report(self.tid)

    def step(self, index: int, stage: str = 'raw'):
        """获取任务中某一步的详细信息

        Args:
            index (int): 步数.
            stage (str, optional): 任务执行所经历的阶段. Defaults to 'raw'.包括:
                > ini: 编译生成的指令.
                > raw: 映射为硬件通道后的指令及收集好的相关参数.
                > ctx: 编译所用的上下文环境(ctx).
                > debug: 由设备返回的原始数据.
                > trace: 每个指令执行所用时间.

        Returns:
            _type_: _description_
        """
        if stage in ['ini', 'raw', 'ctx']:
            return _s.review(self.tid, index)[stage]
        elif stage in ['debug', 'trace']:
            return _s.track(self.tid, index)[stage]

    def process(self, data: list[dict]):
        """处理从server取回的数据

        Args:
            data (list[dict]): 一维数组, 其中每个元素均为dict, 即envelope.process函数返回值.
        """
        for dat in data:
            for k, v in dat.items():
                if k in self.data:
                    self.data[k].append(v)
                else:
                    self.data[k] = [v]

    def update(self):
        try:
            self.result()
        except Exception as e:
            print(e)

        status = self.status()['status']

        if status in ['Failed', 'Canceled']:
            self.stop(self.tid, False)
            return True
        elif status in ['Running']:
            self.progress.goto(self.index)
            return False
        elif status in ['Finished', 'Archived']:
            self.progress.goto(self.progress.max)
            if hasattr(self, 'app'):
                self.app.save()
            self.stop(self.tid)
            self.result()
            return True

    def clear(self):
        for tid, handle in self.handles.items():
            self.stop(tid)

    def stop(self, tid: int, success: bool = True):
        try:
            self.progress.finish(success)
            self.handles[tid].cancel()
        except Exception as e:
            pass

    def bar(self, interval: float = 2.0):
        """任务进度信息. 如果timeout非零, 则同步阻塞执行, 否则异步.
        NOTE: 如果结果获取不到或者不全, 可能是save清空导致,可 减小interval增加取数频率.

        Args:
            interval (float, optional): 进度刷新时间间隔, 不宜也不必过快. Defaults to 2.0.

        Raises:
            TimeoutError: 如果任务超过了认定的最大时间还未完则停止.
            实际还在执行, 只是Task不再获取数据及进度.
        """
        while True:
            try:
                status = self.status()['status']
                if status in ['Pending']:
                    time.sleep(interval)
                    continue
                else:
                    self.progress = Progress(self.name, self.report()['size'])
                    break
            except Exception as e:
                print(e, status, self.report())

        if isinstance(self.timeout, float):
            while True:
                if self.timeout > 0 and (time.time() - self.stime > self.timeout):
                    msg = f'Timeout: {self.timeout}'
                    print(msg)
                    raise TimeoutError(msg)
                time.sleep(interval)
                if self.update():
                    break
        else:
            self.progress.clear()
            self.refresh(interval)
        self.progress.close()

    def refresh(self, interval: float = 2.0):
        """异步获取数据并刷新进度, 不会阻塞notebook。

        Args:
            interval (float, optional): 刷新时间间隔. Defaults to 2.0.
        """
        self.progress.display()
        if self.update():
            self.progress.display()
            return
        self.handles[self.tid] = asyncio.get_running_loop(
        ).call_later(interval, self.refresh, *(interval,))

    def plot(self, append: bool = False):
        """实时画图

        Args:
            append (bool, optional): 绘图方法, 首次画图(True)或增量数据画图(False).

        NOTE: 子图数量不宜太多(建议最大6*6), 单条曲线数据点亦不宜过多(建议不超过5000)

        >>> 如
        row = 4
        col = 4
        for i in range(100): # 步数
            time.sleep(0.1) # 防止刷新过快导致卡顿
            try:
                data = []
                for r in range(row):
                    rd = []
                    for c in range(col):
                        cell = {}
                        for j in range(2):
                            line = {}
                            line['xdata'] = np.arange(i, i+1)
                            line['ydata'] = np.random.random(1)
                            line['title'] = f'{r}_{c}'
                            line['xlabel'] = f'xx'
                            line['ylabel'] = f'yy'
                            line['titlecolor'] = 'red'
                            line['linecolor']=random.choice(['r', 'g', 'b', 'k', 'c', 'm', 'y', (31, 119, 180)])
                            cell[f'test{j}'] = line
                        rd.append(cell)
                    data.append(rd)
                if i == 0:
                    _vs.plot(data)
                else:
                    _vs.append(data)
            except Exception as e:
                print(e)
        """
        if self.last == 0:
            _vs.clear()

        if 'population' in str(self.meta['other']['signal']):
            signal = 'population'
        else:
            signal = str(self.meta['other']['signal']).split('.')[-1]
        raw = np.abs(np.asarray(self.data[signal][self.last:self.index]))

        if hasattr(self, 'app'):
            try:
                title = self.app.consts['couplers']
            except Exception as e:
                title = self.app.consts['qubits']
        axis = self.meta['axis']
        label = tuple(axis)

        if len(label) == 1:
            xlabel = label[0]
            ylabel = 'Any'
            xdata = axis[xlabel][xlabel][self.last:self.index]
            ydata = raw
        elif len(label) == 2:
            xlabel, ylabel = label
            xdata = axis[xlabel][xlabel]
            ydata = axis[ylabel][ylabel]
            zdata = raw

        if len(label) > 3:
            return
        row, col = raw.shape[-1]//4+1, 4

        time.sleep(0.1) # 防止刷新过快导致卡顿
        try:
            data = []
            for r in range(row):
                rd = []
                for c in range(col):
                    cell = {}
                    for j in range(1):
                        idx = r*col+c
                        line = {}
                        if len(label) == 1:
                            try:
                                line['xdata'] = xdata
                                line['ydata'] = ydata[..., idx].squeeze()
                            except Exception as e:
                                # line['ydata'] = ydata[..., 0]*0
                                continue

                        if len(label) == 2:
                            try:
                                if self.last == 0:
                                    line['xdata'] = xdata
                                    line['ydata'] = ydata
                                line['zdata'] = zdata[..., idx]
                                line['colormap'] = 'jet'#magma
                            except Exception as e:
                                # line['zdata'] = np.array([0])
                                continue
                        
                        try:
                            line['title'] = f'{self.name}_{self.app.record_id}_{title[idx]}'
                        except Exception as e:
                            line['title'] = f'{r}_{c}'
                        line['xlabel'] = xlabel
                        line['ylabel'] = ylabel
                        line['linecolor']='r'
                        cell[f'test{j}'] = line
                    rd.append(cell)
                data.append(rd)
            if not append:
                _vs.plot(data)
            else:
                _vs.append(data)
        except Exception as e:
            print(e)


def submit(app: App, block: bool = False, path: str | Path = Path.cwd(), encoding: bool = True,
           reset: list = [], suffix: str = '0', dry_run: bool = False, preview: list = []):
    """转换继承自App的任务为server可执行任务

    Args:
        app (App): 任务基类.
        block (bool, optional): 是否阻塞任务, 用于多个任务顺序执行.
        path (str | Path, optional): 线路文件读写路径. Defaults to Path.cwd().
        encoding (bool, optional): 是否序列化线路. Defaults to True.
        reset (bool, optional): 任务开始前执行，重置设备指令列表, 如[('WRITE','Q0.waveform.Z','zero()','au')].
        suffix (str, optional): 线路文件后缀, 用于多个任务循环时避免文件覆盖.
        dry_run (bool, optional): 是否跳过设备执行, 但波形正常计算可以显示, 用于debug.
        preview (list, optional): 需要实时显示的波形, 对应etc.preview.filter.

    Raises:
        TypeError: _description_


    任务字典整体分两个字段: toserver
    >>> metainfo (dict):
      > name (str): filename:/s21, filename表示数据将存储于filename.hdf5中, s21为实验名字, 以:/分隔
      > user (str): 实验者代号. 默认为usr. 
      > tid (int): 任务id, 全局唯一, 如不指定, 则由系统生成. 
      > priority (int): 优先级, 任务同时提交时, 优先级数值小的先执行. 默认为0. 
      > other (dict): 其他参数, 如shots、signal等, 作为kwds传递给ccompile(见envelope.assembler)
    >>> taskinfo (dict):
      > STEP (dict): 大写, 描述任务执行的变量(即for循环变量)与执行步骤(即for循环体)
      > CIRQ (list | str): 大写, 描述任务线路, 长度等于STEP中for循环变量长度. 可为空. 
      > INIT (list): 大写, 任务初始化设置. 可为空. 
      > RULE (list): 大写, 变量关系列表, 可为表达式或空, 如[f'<gate.rfUnitary.{q}.params.frequency>=<freq.{q}>']. 可为空. 
      > LOOP (dict): 大写, 定义循环执行所用变量, 与STEP中main的值对应, STEP中main所用变量为LOOP的子集
    """

    _s.feed(0, 0, {'reset': reset})

    app.toserver = 'ready'
    app.run(dry_run=True, quiet=True)
    time.sleep(3)

    loop, index = [], ()
    filepath = Path(path)/f'{app.name.replace(".","_")}_{suffix}.cirq'
    with open(filepath, 'w', encoding='utf-8') as f:
        for step in tqdm(app.circuits(), desc='CircuitExpansion'):
            if isinstance(step, StepStatus):
                cc = step.kwds['circuit']
                if not encoding:
                    f.writelines(str(cc)+'\n')
                else:
                    f.writelines(str(dill.dumps(cc))+'\n')
                loop.append(step.iteration)
                index = step.index
            else:
                raise TypeError('Wrong type of step!')
    app.datashape = [i+1 for i in index]
    # return
    _s.update('etc.preview.filter', preview)

    loops = {}
    for k, v in app.loops.items():
        loops[k] = [(k, v, 'au')]

    deps = []
    for k, v in app.mapping.items():
        if isinstance(app[v], str):
            deps.append(f'<{k}>="{app[v]}"')
        elif isinstance(app[v],dict):
            for _k,_v in flattenDictIter(app[v]):
                if isinstance(_v, str):
                    deps.append(f'<{k}.{_k}>="{_v}"')
                else:
                    deps.append(f'<{k}.{_k}>={_v}')
        else:
            deps.append(f'<{k}>={app[v]}')

    sample = _s.query('station.sample')
    trigger = _s.query('station.triggercmds')

    init = [(f'{t.split(".")[0]}.CH1.Shot', app.shots, 'any') for t in trigger]

    toserver = Task(dict(metainfo={'name': f'{sample}:/{app.name.replace(".","_")}_{suffix}',
                                   'user': _s.query('etc.username'),
                                   'tid': app.id,
                                   'priority': app.task_priority,
                                   'other': {'shots': app.shots,
                                             'signal': app.signal,
                                             'lib': app.lib,
                                             'align_right': app.align_right,
                                             'waveform_length': app.waveform_length,
                                             'autorun': not dry_run,
                                             'timeout': 1000.0}},

                         taskinfo={'STEP': {'main': ['WRITE', tuple(loops.keys())],
                                            'trigger': ['WRITE', 'trig'],
                                            'READ': ['READ', 'read'],
                                            },
                                   'INIT': init,
                                   'RULE': deps,
                                   'CIRQ': str(filepath.resolve()),
                                   'LOOP': loops | {'trig': [(t, 0, 'au') for t in trigger]}
                                   }))
    toserver.timeout = 1e9 if block else None
    toserver.app = app
    app.toserver = toserver
    app.run()
    app.bar()


def get_data_by_tid(tid: int, shape: tuple | list = [], snapshot: bool = False):
    """根据任务id从hdf5获取数据

    Args:
        tid (int): 任务id
        shape (tuple|list): data shape, 如果不指定尝试从记录中推出
        snapshot (bool): 是否返回cfg表, 默认为False

    Returns:
        tuple: 数据体、元信息、cfg表
    """
    filename, dataset = _s.track(tid)['file'].rsplit(':', 1)    

    info, data = {}, {}
    with h5py.File(filename) as f:
        group = f[dataset]
        info = loads(dict(group.attrs)['snapshot'])
        if not shape:
            shape = []
            for k, v in info['taskinfo']['meta']['axis'].items():
                shape.extend(tuple(v.values())[0].shape)

        for k in group.keys():
            ds = group[f'{k}']
            data[k] = np.full((*shape, *ds.shape[1:]), 0, ds.dtype)
            data[k][np.unravel_index(np.arange(ds.shape[0]), shape)] = ds[:]

    snp = info['snapshot'] if info and snapshot else {}

    return {'data': data, 'meta': info['taskinfo']['meta'], 'snapshot': snp}


def showave(task: Task | int, index: int = 0,
            start: float = 0, stop: float = 99e-6, sample_rate: float = 6e9,
            keys: tuple = ('Q0',), stage: str = 'raw', step: str = 'main', backend: str = 'mpl'):
    if isinstance(task, Task):
        cmds = task.step(index)[stage][step]
    else:
        cmds = _s.review(task, index)[stage][step]

    _stop = round(stop * sample_rate)
    _start = round(start * sample_rate)
    # n = round((stop - start) * sample_rate)
    xt = np.arange(_stop - _start) / sample_rate + start

    wdict = {}
    if stage in ['ini', 'raw']:
        for target, (ctype, value, unit, kwds) in cmds.items():
            if kwds['target'].split('.')[0] not in keys:  # qubit name
                continue
            
            if isinstance(value,str):
                value = wave_eval(value)
            
            if isinstance(value, Waveform):
                wdict[target] = value(xt)
    elif stage in ['debug', 'trace']:
        for dev, chqval in cmds.items():
            if dev not in keys:  # device name
                continue
            for chq, value in chqval.items():
                if chq.endswith('Waveform'):
                    wdict[f'{dev}.{chq}'] = value[_start:_stop]

    if backend == 'mpl':
        sdict = {k: wdict[k] for k in sorted(wdict)}
        plt.figure()
        for i, (target, wave) in enumerate(sdict.items()):
            plt.plot(xt, wave+i*0)
        plt.legend(list(sdict))
    else:
        sdict = {k: {'xdata': xt, 'ydata':wdict[k]} for k in sorted(wdict)}
        _cs.plot([[sdict]])
