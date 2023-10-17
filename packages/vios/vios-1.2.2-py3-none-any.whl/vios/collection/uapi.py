import random
import time
from datetime import datetime
from pathlib import Path

import matplotlib.image as mim
import matplotlib.pyplot as plt
import numpy as np
from quark import loads
from storage.crud.record import query_record, update_tags
from storage.utils import session

URL = f'sqlite:///{Path.home()/"data/waveforms.db"}'
LIMIT = 50

# region Record Table
def _format_tag(tag):
    if tag.startswith('!'):
        return f'<code style="color: white; background: red">{tag}</code>'
    elif tag.startswith('?'):
        return f'<code style="background: orange">{tag}</code>'
    elif tag.startswith('@'):
        return f'<code style="color: white; background: green">{tag}</code>'
    elif tag.startswith('#'):
        return f'<code style="color: white; background: blue">{tag}</code>'
    elif tag.startswith('$'):
        return f'<code style="color: white; background: purple">{tag}</code>'
    elif tag.startswith('%'):
        return f'<code style="color: white; background: brown">{tag}</code>'
    else:
        return f'<code>{tag}</code>'


def query(page: int = 1, app: str = None, tags: str = '', after: datetime = None, before: datetime = None):
    """从数据库查询测量记录

    Args:
        page (int, optional): 页码. Defaults to 1.
        app (str, optional): 类别. Defaults to None.
        tags (str, optional): 标签. Defaults to ''.
        after (datetime, optional): 起始时间. Defaults to None.
        before (datetime, optional): 终止时间. Defaults to None.

    Returns:
        tuple: 表头，表内容，总页数，类别列表
    """
    # try:
    #     import portalocker
    # except SyntaxError as e:
    #     print(e)
    print('query database: ', page, app, tags, before, after)
    try:
        with session(url=URL) as db:
            if tags == 'None':
                tags = []
            else:
                tags = tags.split(',')

            if app == '*':
                app = None

            total, apps, table = query_record(db,
                                              offset=(page-1)*LIMIT,
                                              limit=LIMIT,
                                              app=app,
                                              tags=tags,
                                              before=before,
                                              after=after)
    except Exception as e:
        print(e)
        total, apps, table = 100, ['t1', 't2', 't3'], {}

    # table = {}
    header = table.get('header', ['a', 'b', 'c', 'd'])  #
    data = table.get('body', [['id', 'app', [
                     f'<font color=green><b>tags</b></font>,Q1,Q2,Q3'], 'timestamp']])  #
    for row in data:
        ftags = []
        for tag in row[2]:
            ftags.append(_format_tag(tag))
        row[2] = ','.join(ftags)
        # row[-1] = str(row[-1]).split('.')[0]
    pages = total//LIMIT+1

    return header, data, pages, apps


def update(rid: int, tags: str):
    """更新记录标签

    Args:
        rid (int): 记录id，为连续递增的整数
        tags (str): 标签，以逗号分隔
    """
    print(rid, tags, type(tags))
    with session(url=URL) as db:
        update_tags(db, rid, tags.split(','))


def load(rid: int):
    """结果索引id，返回结果暂存于剪贴板。

    Args:
        rid (int): 记录id，为连续递增的整数

    Returns:
        _type_: _description_
    """
    return f'get_data_by_id({rid})'
# endregion Record Table


# region plot

def mplot(fig, data):
    ax = fig.add_subplot(1, 1, 1)
    # ax.plot(np.random.randn(1024), '-o')
    # First create the x and y coordinates of the points.
    n_angles = 36
    n_radii = 8
    min_radius = 0.25
    radii = np.linspace(min_radius, 0.95, n_radii)

    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles

    x = (radii * np.cos(angles)).flatten()
    y = (radii * np.sin(angles)).flatten()

    # Create the Triangulation; no triangles so Delaunay triangulation created.
    import matplotlib.tri as tri
    triang = tri.Triangulation(x, y)

    # Mask off unwanted triangles.
    triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                             y[triang.triangles].mean(axis=1))
                    < min_radius)

    ax.set_aspect('equal')
    ax.triplot(triang, 'bo-', lw=1)
    ax.set_title('triplot of Delaunay triangulation')
    return 3000, 3000


def demo(fig):
    # demo: read image file
    img = np.rot90(mim.imread(
        Path(__file__).parents[2]/'tests/test/mac.png'), 2)
    img = np.moveaxis(img, [0, -1], [-1, 0])
    fig.layer({'name':'example of image', 'zdata':img})

    # demo: show image from array
    fig.layer({'name':'example of image[array]', 'zdata':np.random.randn(5, 101, 201)})

    # demo: plot layer by layer
    tlist = np.arange(-2*np.pi, 2*np.pi, 0.05)
    for i in range(8):
        fig.layer(dict(name=f'example of layer plot[{i}]',
                       ydata=np.random.random(1)*np.sin(2*np.pi*0.707*tlist)/tlist,
                       xdata=tlist,
                       title='vcplot',
                       legend='scatter',
                       clear=False,
                       marker=random.choice(
                           ['o', 's', 't', 'd', '+', 'x', 'p', 'h', 'star']),
                       markercolor='r',
                       markersize=12,
                       xlabel='this is xlabel',
                       ylabel='this is ylabel',
                       xunits='xunits',
                       yunits='yunits'))
        fig.layer(dict(name=f'example of layer plot[{i}]',
                       ydata=np.random.random(1)*2*np.sin(2*np.pi*0.707*tlist)/tlist,
                       xdata=tlist))
    # demo: subplot like matplotlib
    axes = fig.subplot(4, 4)
    for ax in axes[::2]:
        cmap = random.choice(plt.colormaps())
        ax.imshow(img[0, :, :], colormap=cmap, title=cmap)
    for ax in axes[1::2]:
        ax.plot(np.sin(2*np.pi*0.707*tlist)/tlist,
                title='vcplot',
                xdata=tlist,
                marker=random.choice(
                    ['o', 's', 't', 'd', '+', 'x', 'p', 'h', 'star']),
                markercolor=random.choice(
                    ['r', 'g', 'b', 'k', 'c', 'm', 'y', (255, 0, 255)]),
                linestyle=random.choice(
            ['-', '.', '--', '-.', '-..', 'none']),
            linecolor=random.choice(
                    ['r', 'g', 'b', 'k', 'c', 'm', 'y', (31, 119, 180)]))


def qplot(fig, dataset: list):
    """Plot 1D array
    """
    # print('ptype', dataset)
    return demo(fig)

    data, meta = dataset
    cfg = loads(meta)
    data = np.asarray(data)

    name = cfg['meta']['arguments'].get('name', 'None')
    print(cfg['meta']['index'].keys(), data.shape)

    qubits = cfg['meta']['arguments'].get('qubits', 'None')

    axes = fig.subplot(2, 2)
    for i, qubit in enumerate(qubits):
        freq = cfg['meta']['index']['time']
        res = data[:, i]

        sf = freq[np.argmin(np.abs(res))]
        # print(sf)
        axes[i].plot(np.abs(res),
                     title=qubit,
                     xdata=freq,
                     legend=str(sf),
                     marker='o',
                     markercolor='b',
                     linestyle='-.',
                     linecolor=random.choice(
            ['r', 'g', 'b', 'k', 'c', 'm', 'y', (31, 119, 180)]))

# endregion plot

