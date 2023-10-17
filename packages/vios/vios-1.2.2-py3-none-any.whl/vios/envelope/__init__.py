"""本模块为实验中可由用户实现的部分构成. 模块调用所需参数见各自模块的说明文档. 
每个实验Step的执行依次流经以下环节(@标注, &表示相应环节所执行方法, 箭头表示执行顺序). 

--->@assembler      @calculator       @device          @processor       @rule
        ↓           ↑    ↓            ↑  ↓             ↑     ↓          ↑   ↓ 
        &ccompile   ↑    &calculate -->  &read|write -->     &process -->   &postprocess --->
        ↓           ↑
        &assemble -->
"""


import dill

from .assembler import MAPPING, assemble, ccompile, decode, initialize
from .calculator import calculate, preview
from .device import read, write
from .processor import process
from .rule import postprocess, schedule

loads = dill.loads
dumps = dill.dumps


class Future(object):
    def __init__(self, index: int = -1) -> None:
        self.index = index

    def result(self, timeout: float = 3.0):
        return self.quark.result(self.index, timeout=timeout)
