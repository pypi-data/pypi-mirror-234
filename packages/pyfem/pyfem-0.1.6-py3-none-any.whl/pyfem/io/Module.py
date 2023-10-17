# -*- coding: utf-8 -*-
"""

"""
from pyfem.io.BaseIO import BaseIO


class Module(BaseIO):
    """
    定义边界条件。

    :ivar name: 边界条件名称
    :vartype name: str

    :ivar category: 边界条件类别
    :vartype category: str

    :ivar type: 边界条件类型
    :vartype type: str

    :ivar dof: 自由度列表
    :vartype dof: list[str]

    :ivar node_sets: 节点集合列表
    :vartype node_sets: list[str]

    :ivar element_sets: 单元集合列表
    :vartype element_sets: list[str]

    :ivar bc_element_sets: 边界单元集合列表
    :vartype bc_element_sets: list[str]

    :ivar value: 边界条件数值
    :vartype value: float

    :ivar amplitude_name: 边界条件幅值名称
    :vartype amplitude_name: str
    """

    __slots_dict__: dict = {
        'name': ('str', '用户自定义模块名称'),
        'category': ('str', '用户自定义模块类别'),
        'path': ('str', '用户自定义模块路径'),
        'module': ('class', '用户自定义模块')
    }

    __slots__: list = [slot for slot in __slots_dict__.keys()]

    def __init__(self) -> None:
        super().__init__()
        self.name: str = None  # type: ignore
        self.category: str = None  # type: ignore
        self.path: str = None  # type: ignore
        self.module: dict = None


if __name__ == "__main__":
    from pyfem.utils.visualization import print_slots_dict

    print_slots_dict(Module.__slots_dict__)

    module = Module()
    module.show()
