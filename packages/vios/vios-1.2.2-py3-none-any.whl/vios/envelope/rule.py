"""任务结束之后对结果进行后处理
"""

import json
import shutil
import time
from pathlib import Path

import numpy as np
import requests

from .. import startup

try:
    with open(Path(startup.get('site', ''))/'etc/cloud.json', 'r') as f:
        CLOUD = json.loads(f.read())
except Exception as e:
    # print(e)
    CLOUD = {}


def savefig(result):
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('agg')


    fig, ax = plt.subplots(2, 2, figsize=[9, 9])
    ax = ax.flatten()
    for a in ax:
        a.plot([1,2,3])
    plt.savefig('test.png')


def schedule():
    """执行事先设定好的定时任务, 默认为每天凌晨2点到6点.

    >>> 定时规则由etc.schedule指定, 规则如下
    - year(int | str): 年(4位数字)
    - month(int | str): 月(范围1-12)
    - day(int | str): 日(范围1-31)
    - week(int | str): 周(范围1-53)
    - day_of_week(int | str): 周内第几天或者星期几(0-6 或 mon,tue,wed,thu,fri,stat,sun)
    - hour(int | str): 时(0-23)
    - minute(int | str): 分(0-59)
    - second(int | str): 秒(0-59)
    """
    # dst = shutil.move(Path('../../home/dat/144v3-swj-221013-normalJJ_2023-03-01-22-37-23.hdf5'),Path.home())
    # for path in sorted(Path('../../home/dat').glob('**/*.hdf5')):
    #     print((time.time() - path.stat().st_mtime)/(24*60*60),shutil.disk_usage(path))
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'do something ...')
    return [(r'C:\Usersddd\sesam\Desktop\home\dat\baqis\testtask_2023-08-31-12-35-12.hdf5',r'\home\dat\baqis\testtask_2023-08-31-12-35-12.hdf5')]


def postprocess(result: dict):
    """任务执行完后对数据的操作, 如存储到自定义路径或回传到云平台等

    Args:
        result (dict): 任务结果, 包含
          - meta: task中metainfo字段的内容, 执行时会扩充坐标轴、id、priority、执行状态等信息
          - data: 值为np.array, 形如{'iq':np.array,'count':np.array}
          - info: 任务执行过程中记录下的系统信息, 包括CPU、内存、网络等
          - task: 原始任务
          - snapshot: 当前任务对应的cfg表快照
    """
    def _delete_dict(ret: dict, num: int = 0):
        while num > 0:
            tmp = np.cumsum(list(ret.values()))
            ran_num = np.random.randint(tmp[-1]+1)
            ran_pos = np.searchsorted(tmp, ran_num)
            ret[list(ret.keys())[ran_pos]] -= 1
            if ret[list(ret.keys())[ran_pos]] == 0:
                ret.pop(list(ret.keys())[ran_pos], 0)
            num -= 1

    # print(result.keys(),result['meta'].keys())

    meta = result['meta']
    # savefig(result)
    print('Send result back  to', meta['user'])
    if not meta['user'].startswith('quafu'):
        return
    
    if not CLOUD:
        return
    
    srv = CLOUD[meta['user']]

    task_id = hex(meta['tid'])[2:].upper()
    task_status = 'failed'
    if meta['status'] in ['Finished','Archived']:
        task_status = 'finished'
        try:
            data: list[dict] = result['data']['count']
        except Exception as e:
            print('Failed to process result',e)
            task_status = 'failed'
    
    if task_status == 'finished':
        dres = {}
        for dat in data:
            for k, v in dat.items():
                dres[k] = dres.get(k, 0)+v

        try:
            shots = meta['other']['shots']*len(meta['axis']['repeat']['repeat'])
            _delete_dict(dres, shots - (shots//1000)*1000)
        except Exception as e:
            print('Failed to dropout', e)

        dic_res = {}
        for k, v in dres.items():
            dic_res[''.join((str(i) for i in k))] = v

        rshot = sum(dic_res.values())

        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": str(dic_res).replace("\'", "\""),
                     "res": str(dic_res).replace("\'", "\""),
                     "server": 2}

    elif task_status == 'failed':
        rshot = 0
        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": "",
                     "res": "",
                     "server": 2}
    # print(post_data)
    try:
        resp = requests.post(url=f"http://{srv['server']}/scq_result/",
                             data=post_data,
                             headers={'api_token': srv['token']})
        print(time.strftime('%Y-%m-%d %H:%M:%S'), resp.text, rshot)
    except:
        print('POST ERROR')
