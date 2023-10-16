# -*- coding:UTF-8 -*-

# region 导入依赖项
import math
import os as _os
import webbrowser as _webbrowser
from enum import Enum as _Enum
from enum import unique as _unique
from copy import deepcopy as _deepcopy
from copy import copy as _copy
from datetime import datetime as _datetime
import re as _re

模块名 = 'folium'
try:
    import folium as _folium
    from folium import plugins as _plugins
except ImportError as impErr:
    print(f"尝试导入 {模块名} 依赖时检测到异常：{impErr}")
    print(f"尝试安装 {模块名} 模块：")
    try:
        _os.system(f"pip install {模块名}")
    except OSError as osErr:
        print(f"尝试安装模块 {模块名} 时检测到异常：{osErr}")
        raise osErr
    else:
        try:
            import folium as _folium
            from folium import plugins as _plugins
        except ImportError as impErr:
            print(f"再次尝试导入 {模块名} 依赖时检测到异常：{impErr}")
            raise impErr

模块名 = 'DebugInfo'
try:
    from DebugInfo.DebugInfo import 打印模板 as _打印模板
    from DebugInfo.DebugInfo import 黄字 as _黄字
    from DebugInfo.DebugInfo import 青字 as _青字
except ImportError as impErr:
    print(f"尝试导入 {模块名} 依赖时检测到异常：{impErr}")
    print(f"尝试安装 {模块名} 模块：")
    try:
        _os.system(f"pip install {模块名}")
    except OSError as osErr:
        print(f"尝试安装模块 {模块名} 时检测到异常：{osErr}")
        raise osErr
    else:
        try:
            from DebugInfo.DebugInfo import 打印模板 as _打印模板
            from DebugInfo.DebugInfo import 黄字 as _黄字
            from DebugInfo.DebugInfo import 青字 as _青字
        except ImportError as impErr:
            print(f"再次尝试导入 {模块名} 依赖时检测到异常：{impErr}")
            raise impErr

try:
    from src.GpsAndMap.GpsModule import *
except ImportError:
    try:
        from GpsAndMap.GpsModule import *
    except ImportError as impErr:
        print('尝试导入 GpsModule 模块遇到异常:', impErr)
        raise impErr

# endregion

# 指定 js/css 资源的网络地址
_网络资源字典: dict = {r'cdn.jsdelivr.net': {'isReg': False, 'isDelet': False, 'tgtStr': r'fastly.jsdelivr.net'},
                 r'https.*/jquery.*.min.js': {'isReg': True, 'isDelet': False, 'tgtStr': r'https://fastly.jsdelivr.net/npm/jquery/dist/jquery.min.js'},
                 r'netdna.bootstrapcdn.com': {'isReg': False, 'isDelet': True, 'tgtStr': r'fastly.jsdelivr.net'}}


def _更新网络资源字典(字典: dict[str, dict], 清空旧配置: bool = False) -> int:
    """
    使用指定的字典更新 _网络资源字典 中的配置,返回更新的配置项数
    :param 字典: 以字典方式定义的配置参数{资源项目/名称: {'isReg": bool, 'isDelet": bool, 'tgtStr': str}}
    :param 清空旧配置: bool, 是否完全清空现存的配置项
    :return: int 更新的配置数量
    """
    global _网络资源字典
    if 清空旧配置:
        _网络资源字典 = {}

    更新配置数量: int = 0
    if isinstance(字典, dict) and 字典:
        for 键, 配置 in 字典.items():
            键 = str(键).strip()
            if 键 and isinstance(配置, dict):
                isReg: bool = 配置['isReg'] if hasattr(配置, 'isReg') else False
                isDelet: bool = 配置['isDelet'] if hasattr(配置, 'isDelet') else False
                tgtStr: str = str(配置['tgtStr']) if hasattr(配置, 'tgtStr') and 配置['tgtStr'] is not None else ''

                _网络资源字典[键] = {'isReg': isReg, 'isDelet': isDelet, 'tgtStr': tgtStr}
                更新配置数量 += 1

    return 更新配置数量


# 指定 js/css 资源的本地地址
_本地资源字典: dict = {r'src="https.*/jquery.*.min.js"': {'isReg': True, 'isDelet': False, 'tgtStr': r'src="./src/jQuery/jquery-2.0.0.js"'},
                 r'src="https.*/leaflet.js"': {'isReg': True, 'isDelet': False, 'tgtStr': r'src="./src/leaflet/leaflet.js"'},
                 r'src="https.*/bootstrap.min.js"': {'isReg': True, 'isDelet': False, 'tgtStr': r'src="./src/bootstrap-3.3.7/js/bootstrap.min.js"'},
                 r'src="https.*/leaflet.awesome-markers.js"': {'isReg': True, 'isDelet': False,
                                                               'tgtStr': r'src="./src/Leaflet.awesome-markers-2.0.2/dist/leaflet.awesome-markers.js"'},
                 r'src="https.*/leaflet.markercluster.js"': {'isReg': True, 'isDelet': False,
                                                             'tgtStr': r'src="./src/leaflet.markercluster/dist/leaflet.markercluster.js"'},
                 r'src="https.*/leaflet-dvf.markers.min.js"': {'isReg': True, 'isDelet': False,
                                                               'tgtStr': r'src="./src/leaflet-dvf/leaflet-dvf.markers.min.js"'},
                 r'src="https.*/dist/js/bootstrap.bundle.min.js"': {'isReg': True, 'isDelet': False,
                                                                    'tgtStr': r'src="./src/bootstrap-5.2.2/dist/js/bootstrap.bundle.min.js"'},
                 r'src="https.*/dist/leaflet-measure.min.js"': {'isReg': True, 'isDelet': False,
                                                                'tgtStr': r'src="./src/leaflet-measure-2.1.7/dist/leaflet-measure.min.js"'},
                 r'src="https.*/leaflet.textpath.min.js"': {'isReg': True, 'isDelet': False,
                                                            'tgtStr': r'src="./src/leaflet-textpath-1.2.3/leaflet.textpath.min.js"'},
                 r'src="https.*/templates/leaflet_heat.min.js"': {'isReg': True, 'isDelet': False, 'tgtStr': r'src="./src/leaflet/leaflet_heat.min.js"'},
                 r'src="https.*/dist/leaflet-ant-path.min.js"': {'isReg': True, 'isDelet': False,
                                                                 'tgtStr': r'src="./src/leaflet-ant-path-1.1.2/dist/leaflet-ant-path.min.js"'},
                 r'href="https.*/dist/leaflet.css"': {'isReg': True, 'isDelet': False, 'tgtStr': r'href="./src/leaflet/leaflet.css"'},
                 r'href="https.*/bootstrap.min.css"': {'isReg': True, 'isDelet': False, 'tgtStr': r'href="./src/bootstrap-3.3.7/css/bootstrap.min.css"'},
                 r'href="https.*/bootstrap-theme.min.css"': {'isReg': True, 'isDelet': False,
                                                             'tgtStr': r'href="./src/bootstrap-3.3.7/css/bootstrap-theme.min.css"'},
                 r'href="https.*/css/font-awesome.min.css"': {'isReg': True, 'isDelet': False,
                                                              'tgtStr': r'href="./src/font-awesome-4.7.0/css/font-awesome.min.css"'},
                 r'href="https.*/leaflet.awesome-markers.css"': {'isReg': True, 'isDelet': False,
                                                                 'tgtStr': r'href="./src/Leaflet.awesome-markers-2.0.2/dist/leaflet.awesome-markers.css"'},
                 r'href="https:.*/leaflet.awesome.rotate.min.css"': {'isReg': True, 'isDelet': False,
                                                                     'tgtStr': r'href="./src/leaflet.awesome.rotate/leaflet.awesome.rotate.css"'},
                 r'href="https.*/MarkerCluster.css"': {'isReg': True, 'isDelet': False, 'tgtStr': r'href="./src/leaflet.markercluster/dist/MarkerCluster.css"'},
                 r'href="https.*/MarkerCluster.Default.css"': {'isReg': True, 'isDelet': False,
                                                               'tgtStr': r'href="./src/leaflet.markercluster/dist/MarkerCluster.Default.css"'},
                 r'href="https.*/fontawesome.*/css/all.min.css"': {'isReg': True, 'isDelet': False,
                                                                   'tgtStr': r'href="./src/fontawesome-free-6.2.0/css/all.min.css"'},
                 r'href="https.*/dist/leaflet-measure.min.css"': {'isReg': True, 'isDelet': False,
                                                                  'tgtStr': r'href="./src/leaflet-measure-2.1.7/dist/leaflet-measure.min.css"'}}


def _更新本地资源字典(字典: dict[str, dict], 清空旧配置: bool = False) -> int:
    """
    使用指定的字典更新 _本地资源字典 中的配置,返回更新的配置项数
    :param 字典: 以字典方式定义的配置参数{资源项目/名称: {'isReg": bool, 'isDelet": bool, 'tgtStr': str}}
    :param 清空旧配置: bool, 是否完全清空现存的配置项
    :return: int 更新的配置数量
    """
    global _本地资源字典
    if 清空旧配置:
        _本地资源字典 = {}

    更新配置数量: int = 0
    if isinstance(字典, dict) and 字典:
        for 键, 配置 in 字典.items():
            键 = str(键).strip()
            if 键 and isinstance(配置, dict):
                isReg: bool = 配置['isReg'] if hasattr(配置, 'isReg') else False
                isDelet: bool = 配置['isDelet'] if hasattr(配置, 'isDelet') else False
                tgtStr: str = str(配置['tgtStr']) if hasattr(配置, 'tgtStr') and 配置['tgtStr'] is not None else ''

                _本地资源字典[键] = {'isReg': isReg, 'isDelet': isDelet, 'tgtStr': tgtStr}
                更新配置数量 += 1

    return 更新配置数量


# 指定一个字典,用于管理参考距离与地图缩放级别的映射, 键:参考距离km; 值: 地图缩放倍率
_缩放倍率字典: dict[float or int, int] = {0.5: 18,
                                    1: 17,
                                    2: 16,
                                    5: 15,
                                    10: 14,
                                    25: 13,
                                    50: 12,
                                    90: 11,
                                    150: 10,
                                    350: 9,
                                    700: 8,
                                    1600: 7,
                                    3000: 6}


def _更新缩放倍率字典(字典: dict[float or int, int], 清空旧配置: bool = False) -> int:
    """
    使用指定的字典内容, 更新 _ 缩放倍率表 中对应键值位置的内容, 如果待更新的键不存在,则在对应的位置插入该键:值对
    :param 字典: 以字典方式定义的配置参数{参考距离(km)上限(>0): 适用的地图缩放倍率(0~18)}
    :param 清空旧配置: bool, 是否完全清空现存的配置项
    :return: int 更新的配置数量
    """
    global _缩放倍率字典
    if 清空旧配置:
        _缩放倍率字典 = {}

    更新配置数量: int = 0
    if isinstance(字典, dict) and 字典:
        for 距离, 倍率 in 字典.items():
            if 距离 > 0 and 0 <= 倍率 <= 18:
                _缩放倍率字典[距离] = 倍率
                更新配置数量 += 1

    # 对字典按键值进行排序处理(距离由小到大)
    升序的距离表: list = sorted(_缩放倍率字典.keys())
    临时字典: dict[float or int, int] = {}
    for 距离 in 升序的距离表:
        临时字典[距离] = _缩放倍率字典[距离]

    # 使用排序后的字典替换原字典
    _缩放倍率字典 = 临时字典

    return 更新配置数量


# 根据参考距离, 计算缩放倍率
def _缩放倍率(参考距离km: float) -> int:
    参考距离km = 参考距离km if type(参考距离km) in [float, int] else 0
    if 参考距离km <= 0:
        return 18

    global _缩放倍率字典
    默认倍率: int = 5
    for 距离, 倍率 in _缩放倍率字典.items():
        if 参考距离km <= 距离:
            默认倍率 = 倍率
            break

    return 默认倍率


@_unique
class 颜色名(_Enum):
    """
    这是一个 Enum， 定义了一些常用的颜色名称
    """
    红: str = 'red'
    蓝: str = 'blue'
    灰: str = 'gray'
    深红: str = 'darkred'
    浅红: str = 'lightred'
    橘色: str = 'orange'
    浅褐色: str = 'beige'
    绿: str = 'green'
    深绿: str = 'darkgreen'
    浅绿: str = 'lightgreen'
    深蓝: str = 'darkblue'
    浅蓝: str = 'lightblue'
    紫: str = 'purple'
    深紫: str = 'darkpurple'
    粉色 = 'pink'
    军校蓝: str = 'cadetblue'
    浅灰: str = 'lightgray'
    黑: str = 'black'


class 热力点类:
    """
    定义了热力点数据结构，您可以通过 热力点类.帮助文档() 或者 热力点类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 位置: GPS坐标类 = None,
                 权值: float = None):
        self.__位置: GPS坐标类 = 位置
        self.权值: float = 权值

    # region 访问器
    @property
    def 有效(self) -> bool:
        return isinstance(self.__位置, GPS坐标类) and self.__位置.有效

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 位置(self) -> GPS坐标类:
        return self.__位置 if isinstance(self.__位置, GPS坐标类) else GPS坐标类()

    @位置.setter
    def 位置(self, 坐标: GPS坐标类):
        self.__位置 = 坐标 if isinstance(坐标, GPS坐标类) else None

    @property
    def 副本(self) -> '热力点类':
        return 热力点类(self.位置.副本, self.权值)

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('热力点类定义了一个热力点的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('位置:', 'GPS坐标类对象,用于体现热力点的位置信息')
        画板.添加一行('权值:', 'float数据,用于体现该热力点的权重信息,默认为 1')
        画板.添加一行('有效:', 'GPS坐标对象的娄提是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', 'GPS坐标对象的娄提是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个热力点类对象,数据复制自当前对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class _线段中点类:
    """
    定义了线段中点类数据结构，包括 位置(GPS坐标类对象), 倾角(int or float, 线段的倾角, 终点相对于起点正东方向,逆时针旋转角度)
    """

    def __init__(self,
                 位置: GPS坐标类 = GPS坐标类(),
                 倾角: int or float = 0.0):
        self.位置: GPS坐标类 = 位置
        self.倾角: int or float = 倾角


class 图标样式类:
    """
    定义了图标样式的数据结构，您可以通过 图标样式类.帮助文档() 或者 图标样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 名称: str = None,
                 颜色: 颜色名 or str = None,
                 角度_度: int or float = 0.0):
        self.名称: str = 名称
        self.__颜色: 颜色名 or str = 颜色
        self.__角度_度: int or float = 角度_度 if type(角度_度) in [int, float] else 0

        # 圆整到 360 度以内
        if self.__角度_度 < 0:
            self.__角度_度 = -((-self.__角度_度) % 360)
        else:
            self.__角度_度 = self.__角度_度 % 360

        # 圆整到 0 - 360 以内
        self.__角度_度 = self.__角度_度 if self.__角度_度 > 0 else 360 + self.__角度_度

        if self.名称 and not self.颜色:
            self.__颜色 = 颜色名.灰

    # region 访问器
    @property
    def 角度_度(self) -> float:
        return self.__角度_度

    @角度_度.setter
    def 角度_度(self, 角度值deg: int or float) -> None:
        self.__角度_度 = 角度值deg if type(角度值deg) in [int, float] else 0

        # 圆整到 360 度以内
        if self.__角度_度 < 0:
            self.__角度_度 = -((-self.__角度_度) % 360)
        else:
            self.__角度_度 = self.__角度_度 % 360

        # 圆整到 0 - 360 以内
        self.__角度_度 = self.__角度_度 if self.__角度_度 > 0 else 360 + self.__角度_度

    @property
    def 颜色(self) -> str or None:
        if self.__颜色 is None:
            return None
        elif isinstance(self.__颜色, 颜色名):
            return str(self.__颜色.value)
        else:
            return str(self.__颜色)

    @颜色.setter
    def 颜色(self, 颜色值: str or 颜色名):
        self.__颜色 = 颜色值

    @property
    def _icon对象(self) -> _folium.Icon:
        return None if self.无效 else _folium.Icon(icon=self.名称, color=self.颜色, angle=int(self.__角度_度))

    @property
    def 有效(self) -> bool:
        return True if self.名称 else False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '图标样式类':
        return 图标样式类(self.名称, self.__颜色)

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('图标样式类定义了一个图标样式的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('名称:', '指定图标的名称')
        画板.添加一行('', '图标名称可以参考 https://v3.bootcss.com/components/ 获取')
        画板.添加一行('', '例如: glyphicon-ok, glyphicon-map-marker, glyphicon-fire')
        画板.添加一行('颜色:', '指定图标的颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('角度_度:', '指定图标的旋转角度,以度为单位, 需要介于 0~360 之间, 旋转方向为顺时针')
        画板.添加一行('有效:', '图标样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '图标样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的图标样式类对象,数据复制自当前的对象')
        画板.添加一行('_icon对象:', '基于当前的样式设置,生成并返回一个 folium.Icon 对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 提示样式类:
    """
    定义了提示样式的数据结构，您可以通过 提示样式类.帮助文档() 或者 提示样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 消息: str = None,
                 样式: str = None,
                 粘性: bool = True):
        self.消息: str = 消息
        self.样式: str = 样式
        self.粘性: bool = 粘性

    # region 访问器
    @property
    def 副本(self) -> '提示样式类':
        return 提示样式类(self.消息, self.样式, self.粘性)

    @property
    def 有效(self) -> bool:
        if not self.消息:
            return False
        elif not str(self.消息).strip():
            return False
        return True

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def _toolTip对象(self) -> _folium.Tooltip:
        return None if self.无效 else _folium.Tooltip(text=str(self.消息).strip(),
                                                    style=str(self.样式).strip(),
                                                    sticky=self.粘性)

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('提示样式类定义了一个提示样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('消息:', '提示消息的文本内容')
        画板.添加一行('样式:', 'html的style定义,例如: "background: blue; color: red"')
        画板.添加一行('粘性:', '提示消息是否跟随鼠标移动')
        画板.添加一行('有效:', '提示样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '提示样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的提示样式类对象,数据复制自当前的对象')
        画板.添加一行('_toolTip对象:', '基于当前的样式设置,生成并返回一个 folium.Tooltip 对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 消息样式类:
    """
    定义了消息样式的数据结构，您可以通过 消息样式类.帮助文档() 或者 消息样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 消息: str = None,
                 渲染html: bool = False,
                 最大像素宽度: int = 240,
                 最大比例宽度: str = None,
                 默认显示: bool = False,
                 粘性: bool = False):
        self.消息: str = 消息
        self.渲染html: bool = 渲染html
        self.最大像素宽度: int = 最大像素宽度
        self.最大比例宽度: str = 最大比例宽度
        self.默认显示: bool = 默认显示
        self.粘性: bool = 粘性

    # region 访问器
    @property
    def _popup对象(self) -> _folium.Popup:
        return None if self.无效 else _folium.Popup(html=self.消息,
                                                  parse_html=self.渲染html,
                                                  max_width=self.最大宽度有效值,
                                                  show=self.默认显示,
                                                  sticky=self.粘性)

    @property
    def 有效(self) -> bool:
        return True if self.消息 else False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 最大宽度有效值(self) -> int or str:
        if self.最大比例宽度:
            return self.最大比例宽度
        elif self.最大像素宽度 > 0:
            return self.最大像素宽度
        else:
            return '100%'

    @property
    def 副本(self) -> '消息样式类':
        return 消息样式类(self.消息, self.渲染html, self.最大像素宽度, self.最大比例宽度, self.默认显示, self.粘性)

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('消息样式类定义了一个消息样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('消息:', '消息的文本内容')
        画板.添加一行('渲染html:',
                '定义消息有展示是否进行html元素的渲染, 如果你的消息文本中包括html元素, 则是需要渲染的')
        画板.添加一行('最大像素宽度:', '消息框的最大宽度,以像素值来定义,如果消息的内容超过了这个宽度,则会换行处理')
        画板.添加一行('最大比例宽度',
                '消息框的最大宽度,以消息的html元素的父元素的宽度的比例来定义,如果消息内容超宽,则换行处理')
        画板.添加一行('最大宽度有效值',
                '综合 最大像素宽度和最大比例宽度的设置,优先使用最大比例宽度的设置,次优使用最大像素宽度的设置')
        画板.添加一行('有效:', '消息样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '消息样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的消息样式类对象,数据复制自当前的对象')
        画板.添加一行('_popup对象:', '基于当前的样式设置,生成并返回一个 folium.Popup 对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 封闭图形样式类:
    """
    定义了封闭图形样式的数据结构，您可以通过 封闭图形样式类.帮助文档() 或者 封闭图形样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 线条颜色: 颜色名 or str = None,
                 线条宽度: float = -1,
                 线条透明度: float = 1,
                 填充: bool = True,
                 填充色: 颜色名 or str = None,
                 填充透明度: float = 0.25):
        self.__线条颜色: 颜色名 or str = 线条颜色
        self.线条宽度: float = 线条宽度
        self.线条透明度: float = 线条透明度
        self.填充: bool = 填充
        self.__填充色: 颜色名 or str = 填充色
        self.填充透明度: float = 填充透明度

        if not self.填充:
            self.填充透明度 = 0

    # region 访问器
    @property
    def 线条颜色(self) -> str or None:
        if self.__线条颜色 is None or not str(self.__线条颜色).strip():
            return None
        elif isinstance(self.__线条颜色, 颜色名):
            return str(self.__线条颜色.value)
        else:
            return str(self.__线条颜色)

    @线条颜色.setter
    def 线条颜色(self, 颜色值: str or 颜色名):
        self.__线条颜色 = 颜色值

    @property
    def 填充色(self) -> str or None:
        if self.__填充色 is None or not str(self.__填充色).strip():
            return None
        elif isinstance(self.__填充色, 颜色名):
            return self.__填充色.value
        else:
            return str(self.__填充色)

    @填充色.setter
    def 填充色(self, 颜色值: str or 颜色名):
        self.__填充色 = 颜色值

    @property
    def 副本(self) -> '封闭图形样式类':
        return 封闭图形样式类(self.线条颜色, self.线条宽度, self.线条透明度, self.填充, self.填充色, self.填充透明度)

    @property
    def 有效(self) -> bool:
        if self.线条颜色 is None:
            return False
        elif self.填充 and self.填充色 is None:
            return False
        else:
            return True

    @property
    def 无效(self) -> bool:
        return not self.有效

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('封闭图形样式类定义了一个封闭图形样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('线条颜色:', '指定封闭图形的边框/线条颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('线条宽度:', '指定封闭图形的边框/线条宽度值, 单位是px')
        画板.添加一行('线条透明度:', '指定封闭图形的边框/线条透明度值, 0: 完全透明; 1: 不透明')
        画板.添加一行('填充:', '指定封闭图形的内部区域是否进行颜色填充')
        画板.添加一行('填充色:', '指定封闭图形的内部填充颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('填充透明度:', '指定封闭图形内部区域的填充颜色的透明度值, 0: 完全透明; 1: 不透明')
        画板.添加一行('有效:', '封闭图形样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '封闭图形样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的封闭图形样式类对象,数据复制自当前的对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 线条样式类:
    """
    定义了线条样式的数据结构，您可以通过 线条样式类.帮助文档() 或者 线条样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 颜色: 颜色名 or str = None,
                 宽度: float = -1,
                 透明度: float = 1):
        self.__颜色: 颜色名 or str = 颜色
        self.宽度: float = 宽度
        self.透明度: float = 透明度

    # region 访问器
    @property
    def 有效(self) -> bool:
        return self.__颜色 is not None

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 颜色(self) -> str or None:
        if self.__颜色 is None:
            return None
        elif isinstance(self.__颜色, 颜色名):
            return str(self.__颜色.value)
        else:
            return str(self.__颜色)

    @颜色.setter
    def 颜色(self, 颜色值: str or 颜色名):
        self.__颜色 = 颜色值

    @property
    def 副本(self) -> '线条样式类':
        return 线条样式类(self.颜色, self.宽度, self.透明度)

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('线条样式类定义了一个线条样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('颜色:', '指定线条颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('宽度:', '指定线条宽度值, 单位是px')
        画板.添加一行('透明度:', '指定线条透明度值, 0: 完全透明; 1: 不透明')
        画板.添加一行('有效:', '线条样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '线条样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的线条样式类对象,数据复制自当前的对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 线上文本样式类:
    """
    定义了线上文本样式的数据结构，您可以通过 线上文本样式类.帮助文档() 或者 线上文本样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 文本: str = None,
                 文本颜色: str or 颜色名 = None,
                 文本尺寸px: int = None,
                 重复: bool = True,
                 居中: bool = True,
                 显示于路径下方: bool = False,
                 偏移量px: int = 0,
                 旋转deg: int or float = 0.0,
                 文本属性字典: dict = None):
        self.文本: str = 文本
        self.文本颜色: str or 颜色名 = 文本颜色
        self.文本尺寸px: int = 文本尺寸px
        self.重复: bool = 重复
        self.居中: bool = 居中
        self.显示于路径下方: bool = 显示于路径下方
        self.偏移量px: int = 偏移量px
        self.旋转deg: int or float = 旋转deg
        self.__文本属性字典: dict = 文本属性字典

    # region 访问器
    @property
    def 有效(self) -> bool:
        文本有效: bool = False
        if self.文本 and str(self.文本).strip():
            文本有效 = True
        return 文本有效

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 文本属性字典(self) -> dict or None:
        if not self.__文本属性字典 and not self.文本颜色 and not self.文本尺寸px:
            return None

        if not self.文本颜色 and not self.文本尺寸px:
            return self.__文本属性字典

        文本颜色值 = str(self.文本颜色.value if isinstance(self.文本颜色, 颜色名) else self.文本颜色).strip()
        文本尺寸值 = self.文本尺寸px if isinstance(self.文本尺寸px, int) else 0

        if not 文本颜色值 and not 文本尺寸值:
            return self.__文本属性字典

        self.__文本属性字典 = {} if not isinstance(self.__文本属性字典, dict) else self.__文本属性字典

        if self.文本颜色 and 文本颜色值:
            if 'fill' not in self.__文本属性字典:
                self.__文本属性字典['fill'] = 文本颜色值
        if self.文本尺寸px and 文本尺寸值:
            if 'font-size' not in self.__文本属性字典:
                self.__文本属性字典['font-size'] = 文本尺寸值

        return self.__文本属性字典

    @property
    def 副本(self) -> '线上文本样式类':
        return 线上文本样式类(self.文本, self.文本颜色, self.文本尺寸px, self.重复, self.居中, self.显示于路径下方,
                       self.偏移量px, self.旋转deg,
                       _copy(self.__文本属性字典))

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('线上文本样式类定义了一个线上文本样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('文本:', '线上文本的文本内容')
        画板.添加一行('文本颜色:', '指定线上文本的文本颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('文本尺寸px:', '指定线上文本的文本尺寸, 单位: px')
        画板.添加一行('重复:', '指定指定线上文本是否重复填充整个线段')
        画板.添加一行('居中:', '指定指定线上文本是否居中填充整个线段')
        画板.添加一行('显示于路径下方:',
                '指定线上文本内容是否显示在指定的线段的下层, 如果此时线段较宽且不透明,则可能文本内容被遮挡')
        画板.添加一行('偏移量px:', '指定线上文本是否相对于指定的线段法线方向进行偏移')
        画板.添加一行('旋转deg:', '指定线上文本是否相对于指定的线段方向进行旋转, 单位: 度')
        画板.添加一行('文本属性字典', '以字典方式定义的线上文本的html属性')
        画板.添加一行('', '例如: {"font-size":"16px","fill": "blue"}')
        画板.添加一行('有效:', '线上文本样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '线上文本样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的线上文本样式类对象,数据复制自当前的对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 网页标题样式类:
    """
    定义了网页标题样式的数据结构，您可以通过 网页标题样式类.帮助文档() 或者 网页标题样式类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 标题文本: str = None,
                 标题级别: int = 4,
                 文本尺寸px: int = None,
                 文本颜色: str or 颜色名 = None,
                 文本对齐: str = 'c',
                 文本字体: str = None,
                 文本属性字典: dict = None):
        self.标题文本: str = 标题文本
        self.标题级别: str or int = 标题级别
        self.文本对齐: str = 文本对齐
        self.文本尺寸px: int = 文本尺寸px
        self.文本颜色: str or 颜色名 = 文本颜色
        self.文本字体: str = 文本字体
        self.文本属性字典: dict = 文本属性字典

    # region 访问器
    @property
    def html(self) -> str:
        self.标题文本 = str(self.标题文本 if self.标题文本 else '').strip()
        if not self.标题文本:
            return '<h1><>'

        标题级别字: str = ''
        if isinstance(self.标题级别, int):
            self.标题级别 = min(max(0, self.标题级别), 5)
            标题级别字 = f"h{self.标题级别}"
        elif isinstance(self.标题级别, str):
            if len(self.标题级别) > 1:
                self.标题级别 = self.标题级别.lower()
                if self.标题级别[:2] in 'h1h2h3h4h5':
                    标题级别字 = self.标题级别[:2]
            elif len(self.标题级别) == 1:
                if self.标题级别 in '12345':
                    标题级别字 = f"h{self.标题级别}"
        if not self.标题级别:
            标题级别字 = 'h1'

        对齐字: str = ''
        self.文本对齐 = str(self.文本对齐 if self.文本对齐 else 'c').lower().strip()
        if self.文本对齐:
            if self.文本对齐[0] in 'lcr':
                if self.文本对齐[0] == 'l':
                    对齐字 = 'left'
                elif self.文本对齐[0] == 'r':
                    对齐字 = 'right'
        if not 对齐字:
            对齐字 = 'center'

        self.文本属性字典 = {} if not isinstance(self.文本属性字典, dict) else self.文本属性字典
        if 'font-color' not in self.文本属性字典.keys():
            if self.文本颜色:
                文本颜色值: str = str(
                    self.文本颜色.value if isinstance(self.文本颜色, 颜色名) else self.文本颜色).strip()
                if 文本颜色值:
                    self.文本属性字典['color'] = 文本颜色值
        if 'font-size' not in self.文本属性字典.keys():
            if self.文本尺寸px:
                文本尺寸值: int = self.文本尺寸px if isinstance(self.文本尺寸px, int) else 0
                if 文本尺寸值 > 0:
                    self.文本属性字典['font-size'] = f"{文本尺寸值}px"
        if 'font-family' not in self.文本属性字典.keys():
            if self.文本字体:
                self.文本字体 = str(self.文本字体).strip()
                if self.文本字体:
                    self.文本属性字典['font-family'] = self.文本字体

        属性字: str = ''
        if self.文本属性字典:
            属性字 = ';'.join([f'{项}:{值}' for 项, 值 in self.文本属性字典.items()])

        if 属性字:
            return f"<{标题级别字} align='{对齐字}' style='{属性字}'><b>{self.标题文本}</b></h3>"
        else:
            return f"<{标题级别字} align='{对齐字}'><b>{self.标题文本}</b></h3>"

    @property
    def 有效(self) -> bool:
        return self.标题文本 and str(self.标题文本).strip() != ''

    @property
    def 无效(self) -> bool:
        return not self.有效

    # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('网页标题样式类定义了一个网页标题样式类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('标题文本:', '网页标题的文本内容')
        画板.添加一行('标题级别:', '网页标题的级别, 取值范围为 1~5, 对应于 h1~h5')
        画板.添加一行('文本尺寸px:', '网页标题的文本字体尺寸')
        画板.添加一行('文本颜色:', '网页标题的文本颜色,可通过 颜色名枚举来指定,或者通过16进制颜色值来指定')
        画板.添加一行('', '例如: yellow, #3186cc, 颜色名.粉色, 等')
        画板.添加一行('文本对齐:', '网页标题文本的对齐方式。 l: 左对齐; c: 居中对齐; r: 右对齐')
        画板.添加一行('文本字体:', '网页标题的文本字体')
        画板.添加一行('文本属性字典', '以字典方式定义的网页标题文本的html属性')
        画板.添加一行('', '例如: {"font-size":"16px","fill": "blue"}')
        画板.添加一行('有效:', '网页标题样式数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '网页标题样式数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的网页标题样式类对象,数据复制自当前的对象')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 图标标记类:
    """
    定义了图标标记的数据结构，您可以通过 图标标记类.帮助文档() 或者 图标标记类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 位置: GPS坐标类 = GPS坐标类(),
                 消息: str or 消息样式类 = None,
                 图标: str or 图标样式类 = None,
                 提示: str or 提示样式类 = None):
        """
        folium.Marker 对象
        :param 位置: gps坐标
        :param 消息: str or 消息样式, 定义一个popup消息
        :param 图标: 图标样式
        """
        self.位置: GPS坐标类 = 位置
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.图标: 图标样式类 = 图标 if isinstance(图标, 图标样式类) else 图标样式类(
            名称=str(图标).strip() if 图标 else None)
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)

    # region 访问器
    @property
    def 有效(self) -> bool:
        return self.位置.有效 and (self.图标.有效 or self.消息.有效)

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '图标标记类':
        return 图标标记类(self.位置.副本, self.消息.副本, self.图标.副本, self.提示.副本)

    # endregion

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                _folium.Marker(location=self.位置.目标坐标(目标坐标系)[::-1],
                               popup=self.消息._popup对象,
                               icon=self.图标._icon对象,
                               tooltip=self.提示._toolTip对象).add_to(图层)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('图标标记类定义了一个图标标记类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('位置:', 'GPS坐标类对象,用于定义图标标记在地图上的坐标信息')
        画板.添加一行('消息:', '消息样式类对象,用于定义图标标记需要显示的消息样式信息')
        画板.添加一行('图标:', '图标样式类对象,用于定义图标标记需要显示的图标样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义图标标记需要显示的提示样式信息')
        画板.添加一行('有效:', '图标标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '图标标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的图标标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('_添加到图层:',
                '根据图标标记类数据结构的定义, 生成一个 folium.Marker 对象,并将该 folium.Marker 对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 folium.Marker 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.Marker 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 圆圈标记类:
    """
    定义了圆圈标记的数据结构，您可以通过 圆圈标记类.帮助文档() 或者 圆圈标记类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 位置: GPS坐标类 = GPS坐标类(),
                 半径m: int = 0,
                 半径px: int = 0,
                 消息: str or 消息样式类 = None,
                 圆圈: 封闭图形样式类 = 封闭图形样式类(),
                 提示: str or 提示样式类 = None):
        self.位置: GPS坐标类 = 位置
        self.半径m: int = 半径m
        self.半径px: int = 半径px
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.圆圈: 封闭图形样式类 = 圆圈
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)

    # region 访问器
    @property
    def 有效(self) -> bool:
        if isinstance(self.位置, GPS坐标类) and self.位置.有效:
            if isinstance(self.半径m, int) and self.半径m > 0:
                return True
            elif isinstance(self.半径px, int) and self.半径px > 0:
                return True
        return False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '圆圈标记类':
        return 圆圈标记类(self.位置.副本, self.半径m, self.半径px, self.消息.副本, self.圆圈.副本, self.提示.副本)

    # endregion

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                # 处理线条样式
                if self.圆圈.线条颜色 is None:
                    self.圆圈.线条颜色 = 颜色名.黑
                if self.圆圈.线条宽度 < 0:
                    self.圆圈.线条宽度 = 1
                if self.圆圈.线条透明度 < 0:
                    self.圆圈.线条透明度 = 0.5
                if self.圆圈.填充:
                    if self.圆圈.填充色 is None:
                        self.圆圈.填充色 = 颜色名.灰
                    if self.圆圈.填充透明度 < 0:
                        self.圆圈.填充透明度 = 0.5

                if isinstance(self.半径m, int) and self.半径m > 0:
                    _folium.Circle(location=self.位置.目标坐标(目标坐标系)[::-1],
                                   radius=self.半径m,
                                   color=self.圆圈.线条颜色,
                                   weight=self.圆圈.线条宽度,
                                   opacity=self.圆圈.线条透明度,
                                   fill=self.圆圈.填充,
                                   fill_color=self.圆圈.填充色,
                                   fill_opacity=self.圆圈.填充透明度,
                                   popup=self.消息._popup对象,
                                   tooltip=self.提示._toolTip对象).add_to(图层)

                if isinstance(self.半径px, int) and self.半径px > 0:
                    _folium.CircleMarker(location=self.位置.目标坐标(目标坐标系)[::-1],
                                         radius=self.半径px,
                                         color=self.圆圈.线条颜色,
                                         weight=self.圆圈.线条宽度,
                                         opacity=self.圆圈.线条透明度,
                                         fill=self.圆圈.填充,
                                         fill_color=self.圆圈.填充色,
                                         fill_opacity=self.圆圈.填充透明度,
                                         popup=self.消息._popup对象,
                                         tooltip=self.提示._toolTip对象).add_to(图层)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('圆圈标记类定义了一个圆圈标记类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('位置:', 'GPS坐标类对象,用于定义圆圈标记在地图上的坐标信息')
        画板.添加一行('半径m:', 'folium.Circle对象的半径值,单位: m; folium.Circle对象的显示大小会随着地图的缩放而缩放')
        画板.添加一行('半径px:',
                'folium.CircleMarker对象的半径值,单位: px; folium.CircleMarker对象的显示大小不随着地图的缩放而变化')
        画板.添加一行('消息:', '消息样式类对象,用于定义圆圈标记需要显示的消息样式信息')
        画板.添加一行('圆圈:', '封闭图形样式类对象,用于定义圆圈标记图形样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义圆圈标记需要显示的提示样式信息')
        画板.添加一行('有效:', '圆圈标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '圆圈标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的圆圈标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('_添加到图层:',
                '根据图标标记类数据结构的定义, 生成一个 folium.Circle/CircleMarker 对象,并将该 folium.Circle/CircleMarker 对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:',
                '指定需要添加 folium.Circle/CircleMarker 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.Circle/CircleMarker 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 正多边形标记类:
    """
    定义了正多边形标记的数据结构，您可以通过 正多边形标记类.帮助文档() 或者 正多边形标记类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 位置: GPS坐标类 or 图标标记类 = None,
                 边数: int = 0,
                 半径px: int = 0,
                 角度deg: int or float = 0.0,
                 图形: 封闭图形样式类 = 封闭图形样式类(),
                 消息: str or 消息样式类 = None,
                 提示: str or 提示样式类 = None):
        self.位置: GPS坐标类 or 图标标记类 = 位置 if 位置 is not None else GPS坐标类()
        self.边数: int = 边数
        self.半径px: int = 半径px
        self.角度deg: int or float = 角度deg
        self.图形: 封闭图形样式类 = 图形
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)

    # region 访问器
    @property
    def 有效(self) -> bool:
        return isinstance(self.半径px, int) and self.半径px > 0 and self.位置.有效 and isinstance(self.边数,
                                                                                          int) and self.边数 > 2

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '正多边形标记类':
        return 正多边形标记类(self.位置.副本, self.边数, self.半径px, self.角度deg, self.图形.副本, self.消息.副本,
                       self.提示.副本)

    # endregion

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                # 处理线条样式
                if self.图形.线条颜色 is None:
                    self.图形.线条颜色 = 颜色名.黑
                if self.图形.线条宽度 < 0:
                    self.图形.线条宽度 = 1
                if self.图形.线条透明度 < 0:
                    self.图形.线条透明度 = 0.5
                if self.图形.填充:
                    if self.图形.填充色 is None:
                        self.图形.填充色 = 颜色名.灰
                    if self.图形.填充透明度 < 0:
                        self.图形.填充透明度 = 0.5

                位置: GPS坐标类 = self.位置.位置 if isinstance(self.位置, 图标标记类) else self.位置
                _folium.RegularPolygonMarker(location=位置.目标坐标(目标坐标系=目标坐标系)[::-1],
                                             number_of_sides=self.边数,
                                             rotation=self.角度deg,
                                             radius=self.半径px,
                                             color=self.图形.线条颜色,
                                             weight=self.图形.线条宽度,
                                             opacity=self.图形.线条透明度,
                                             fill=self.图形.填充,
                                             fill_color=self.图形.填充色,
                                             fill_opacity=self.图形.填充透明度,
                                             popup=self.消息._popup对象,
                                             tooltip=self.提示._toolTip对象).add_to(图层)
                if isinstance(self.位置, 图标标记类):
                    self.位置._添加到图层(图层=图层, 目标坐标系=目标坐标系)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('正多边形标记类定义了一个正多边形标记类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('位置:', 'GPS坐标类对象,用于定义正多边形标记在地图上的坐标信息')
        画板.添加一行('边数:', '指定了正多边形对象的边数, 边数不应小于3')
        画板.添加一行('半径px:', '正多边形对象的半径值')
        画板.添加一行('角度deg:', '正多边开对象的旋转角度')
        画板.添加一行('图形:', '封闭图形样式类对象,用于定义正式边形标记的图形样式信息')
        画板.添加一行('消息:', '消息样式类对象,用于定义正多边形标记需要显示的消息样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义正多边形标记需要显示的提示样式信息')
        画板.添加一行('有效:', '正多边形标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '正多边形标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的正多边形标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('_添加到图层:',
                '根据图标标记类数据结构的定义, 生成一个 folium.RegularPolygonMarker 对象,并将该 folium.RegularPolygonMarker 对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:',
                '指定需要添加 folium.RegularPolygonMarker 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.RegularPolygonMarker 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 蚂蚁路径标记类:
    """
    定义了蚂蚁路径的数据结构, 相关参数参考: https://github.com/rubenspgcavalcante/leaflet-ant-path/
    您可以通过 蚂蚁路径标记类.帮助文档() 或者 蚂蚁路径类对象.帮助文档() 查阅更多信息
    """

    def __init__(self,
                 路径点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = None,
                 显示: bool = False,
                 暂停动画: bool = False,
                 反转动画: bool = False,
                 动画周期ms: int = None,
                 硬件加速: bool = False,
                 间断色: list[str or 颜色名] = None,
                 透明度: float = 0.5,
                 间断长度px: list[int] = None,
                 消息: str or 消息样式类 = None,
                 提示: str or 提示样式类 = None,
                 ):
        self.路径点序列: list[
            GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = [] if 路径点序列 is None else 路径点序列
        self.显示: bool = 显示
        self.透明度: float = 透明度
        self.__暂停动画: bool = 暂停动画
        self.__反转动画: bool = 反转动画
        self.__动画周期ms: int = 动画周期ms if isinstance(动画周期ms, int) and 动画周期ms > 0 else 400
        self.__硬件加速: bool = 硬件加速
        self.__间断色: list[str or 颜色名] = 间断色
        self.__间断长度px: list[int] = 间断长度px
        self.__GPS坐标系推理基准: GPS坐标系类型 = GPS坐标系类型.wgs84
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)

    # region 访问器
    @property
    def 有效(self) -> bool:
        if self.路径点序列 or self.显示:
            return True
        return False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 暂停动画(self) -> bool:
        return True if self.__暂停动画 else False

    @暂停动画.setter
    def 暂停动画(self, 值: bool):
        self.__暂停动画 = 值

    @property
    def 反转动画(self) -> bool:
        return True if self.__反转动画 else False

    @反转动画.setter
    def 反转动画(self, 值: bool):
        self.__反转动画 = 值

    @property
    def 动画周期ms(self) -> int:
        return self.__动画周期ms if isinstance(self.__动画周期ms, int) and self.__动画周期ms > 0 else 400

    @动画周期ms.setter
    def 动画周期ms(self, 周期: int):
        self.__动画周期ms = 周期

    @property
    def 硬件加速(self) -> bool:
        return True if self.__硬件加速 else False

    @硬件加速.setter
    def 硬件加速(self, 值: bool):
        self.__硬件加速 = 值

    @property
    def 间断色(self) -> list[str]:
        if isinstance(self.__间断色, list):
            return [str(颜色.value if isinstance(颜色, 颜色名) else 颜色).strip() for 颜色 in self.__间断色]
        return []

    @间断色.setter
    def 间断色(self, 颜色表: list[str or 颜色名]):
        self.__间断色 = 颜色表

    @property
    def 间断长度px(self) -> list[int]:
        if isinstance(self.__间断长度px, list):
            return [int(长度值 if type(长度值) in [int, float] else 20) for 长度值 in self.__间断长度px]
        return []

    @间断长度px.setter
    def 间断长度px(self, 长度表: list[int]):
        self.__间断长度px = 长度表

    @property
    def 副本(self) -> '蚂蚁路径标记类':
        return 蚂蚁路径标记类(_deepcopy(self.路径点序列),
                       self.显示,
                       self.__暂停动画,
                       self.__反转动画,
                       self.__动画周期ms,
                       self.__硬件加速,
                       _copy(self.__间断色),
                       self.透明度,
                       _copy(self.__间断长度px),
                       self.消息.副本,
                       self.提示.副本)

    def 添加路径点(self, 路径点: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类 or list) -> '蚂蚁路径标记类':
        """
        将指定的坐标点添加到该蚂蚁路径类对象的路径点序列中来
        :param 路径点: GPS坐标类对象, 图标标记类对象, 圆圈标记类对象, 正多边形标记类对象, 或者以上对象的列表
        :return: self
        """
        待添加路径点: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = []
        if isinstance(路径点, list):
            待添加路径点 = 路径点
        else:
            待添加路径点.append(路径点)

        for 点 in 待添加路径点:
            if type(点) in [GPS坐标类, 图标标记类, 圆圈标记类, 正多边形标记类]:
                位置 = 点 if isinstance(点, GPS坐标类) else 点.位置
                if 位置.坐标系 == GPS坐标系类型.智能推理坐标:
                    位置.坐标系 = self.__GPS坐标系推理基准
                else:
                    self.__GPS坐标系推理基准 = 位置.坐标系
                self.路径点序列.append(点)
        return self

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                if 目标坐标系 is None or 目标坐标系 == GPS坐标系类型.智能推理坐标:
                    目标坐标系 = self.__GPS坐标系推理基准

                # 生成路径点序列
                纬经度坐标序列: list[list[float, float]] = []
                for 路径点 in self.路径点序列:
                    if isinstance(路径点, GPS坐标类) and 路径点.有效:
                        纬经度坐标序列.append(list(路径点.目标坐标(目标坐标系=目标坐标系))[::-1])
                    elif type(路径点) in [图标标记类, 圆圈标记类, 正多边形标记类] and 路径点.位置.有效:
                        纬经度坐标序列.append(list(路径点.位置.目标坐标(目标坐标系=目标坐标系))[::-1])

                if not 纬经度坐标序列:
                    return None

                # 处理样式
                间断色: list[str] = self.间断色
                间色: str = None if not 间断色 else 间断色[0]
                断色: str = None if (not 间断色) or len(间断色) < 2 else 间断色[1]

                间断长度px: list[int] = self.间断长度px
                if not 间断长度px:
                    间断长度px = [10, 20]
                elif len(间断长度px) < 2:
                    间断长度px = 间断长度px + [20]
                else:
                    间断长度px = 间断长度px[:2]
                间断长度px = [20 if 长度 < 1 else 长度 for 长度 in 间断长度px]

                _plugins.AntPath(locations=纬经度坐标序列,
                                 paused=self.暂停动画,
                                 reverse=self.反转动画,
                                 hardware_acceleration=self.硬件加速,
                                 delay=self.动画周期ms,
                                 dash_array=间断长度px,
                                 opacity=min(max(self.透明度, 0), 1) if type(self.透明度) in [int, float] else 0.5,
                                 pulse_color='white' if not 间色 else 间色,
                                 color='blue' if not 断色 else 断色,
                                 popup=None if self.消息.无效 else self.消息._popup对象,
                                 tooltip=None if self.提示.无效 else self.提示._toolTip对象).add_to(图层)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('蚂蚁路径类定义了一个蚂蚁路径类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('路径点序列:',
                '以包括有位置[GPS坐标类]成员的类型对象或者GPS坐标类对象组成的对象列表,以定义蚂蚁路径的各路径点位置')
        画板.添加一行('', '可作为路径点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('显示:',
                '定义是否显示蚂蚁路径,可以在折线或者多边形对象中使用该属性,以共享折线或者多边形对象的路径点,生成蚂蚁路径')
        画板.添加一行('暂停动画:', '读取或者设置蚂蚁路径的 pause 属性')
        画板.添加一行('反转动画:', '读取或者设置蚂蚁路径的 reverse 属性')
        画板.添加一行('动画周期ms:', '读取或者设置蚂蚁路径的 delay 属性')
        画板.添加一行('硬件加速:', '读取或者设置蚂蚁路径的 hardware_acceleration 属性')
        画板.添加一行('间断色:', '读取或者设置蚂蚁路径的 pulseColor 和 color 属性')
        画板.添加一行('间断长度px:', '读取或者设置蚂蚁路径的 dashArray 属性')
        画板.添加一行('消息:', '消息样式类对象,用于定义蚂蚁路径需要显示的消息样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义蚂蚁路径需要显示的提示样式信息')
        画板.添加一行('有效:', '蚂蚁路径数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '蚂蚁路径数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的蚂蚁路径类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加路径点:', '将指定的坐标点对象添加到蚂蚁路径的路径点列表中')
        画板.添加一行('**路径点',
                '可被添加为路径点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('_添加到图层:',
                '根据蚂蚁路径类数据结构的定义, 生成一个 plugins.AntPath 对象,并将该对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 plugins.AntPath 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 plugins.AntPath 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 矩形标记类:
    """
    定义了矩形标记的数据结构，您可以通过 矩形标记类.帮助文档() 或者 矩形标记类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 对角点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = None,
                 图形: 封闭图形样式类 = 封闭图形样式类(),
                 消息: str or 消息样式类 = None,
                 提示: str or 提示样式类 = None):
        self.对角点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = 对角点序列 if isinstance(
            对角点序列, list) else []
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.图形: 封闭图形样式类 = 图形 if isinstance(图形, 封闭图形样式类) else 封闭图形样式类()
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)
        self.__GPS坐标系推理基准: GPS坐标系类型 = GPS坐标系类型.wgs84

    # region 访问器
    @property
    def 有效(self) -> bool:
        return True if isinstance(self.对角点序列, list) and len(self.对角点序列) > 1 else False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '矩形标记类':
        return 矩形标记类(_deepcopy(self.对角点序列),
                     self.图形.副本,
                     self.消息.副本,
                     self.提示.副本)

    def 添加角点(self, 角点: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类 or list) -> '矩形标记类':
        """
        将指定的角点对象添加到该多矩形标记类对象的对角点序列中来
        :param 角点: GPS坐标类对象, 图标标记类对象, 圆圈标记类对象, 正多边形标记类对象, 或者以上对象的列表
        :return: self
        """
        待添加角点: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = []
        if isinstance(角点, list):
            待添加角点 = 角点
        else:
            待添加角点.append(角点)

        for 点 in 待添加角点:
            if type(点) in [GPS坐标类, 图标标记类, 圆圈标记类, 正多边形标记类]:
                位置 = 点 if isinstance(点, GPS坐标类) else 点.位置
                if 位置.坐标系 == GPS坐标系类型.智能推理坐标:
                    位置.坐标系 = self.__GPS坐标系推理基准
                else:
                    self.__GPS坐标系推理基准 = 位置.坐标系
                self.对角点序列.append(点)
        return self

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                if 目标坐标系 is None or 目标坐标系 == GPS坐标系类型.智能推理坐标:
                    目标坐标系 = self.__GPS坐标系推理基准

                # 生成路径点序列
                纬经度坐标序列: list[list[float, float]] = []
                for 路径点 in self.对角点序列:
                    if isinstance(路径点, GPS坐标类) and 路径点.有效:
                        纬经度坐标序列.append(list(路径点.目标坐标(目标坐标系=目标坐标系))[::-1])
                    elif type(路径点) in [图标标记类, 圆圈标记类, 正多边形标记类] and 路径点.位置.有效:
                        纬经度坐标序列.append(list(路径点.位置.目标坐标(目标坐标系=目标坐标系))[::-1])

                # 处理线条样式
                if self.图形.线条颜色 is None:
                    self.图形.线条颜色 = 颜色名.黑
                if self.图形.线条宽度 < 0:
                    self.图形.线条宽度 = 1
                if self.图形.线条透明度 < 0:
                    self.图形.线条透明度 = 0.5
                if self.图形.填充:
                    if self.图形.填充色 is None:
                        self.图形.填充色 = 颜色名.灰
                    if self.图形.填充透明度 < 0:
                        self.图形.填充透明度 = 0.5

                _folium.Rectangle(bounds=纬经度坐标序列,
                                  color=self.图形.线条颜色,
                                  weight=self.图形.线条宽度,
                                  opacity=self.图形.线条透明度,
                                  fill=self.图形.填充,
                                  fill_color=self.图形.填充色,
                                  fill_opacity=self.图形.填充透明度,
                                  popup=self.消息._popup对象,
                                  tooltip=self.提示._toolTip对象).add_to(图层)

                for 点坐标 in self.对角点序列:
                    if type(点坐标) in [图标标记类, 圆圈标记类, 正多边形标记类]:
                        点坐标._添加到图层(图层=图层, 目标坐标系=目标坐标系)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('矩形标记类定义了一个矩形标记类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('对角点序列:',
                '以包括有位置[GPS坐标类]成员的类型对象或者GPS坐标类对象组成的对象列表,以定义矩形的对角线位置')
        画板.添加一行('', '可作为角点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('图形:', '封闭图形样式类, 定义了矩形标记的边框/线条样式以及内部区域的填充样式')
        画板.添加一行('消息:', '消息样式类对象,用于定义矩形标记需要显示的消息样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义矩形标记需要显示的提示样式信息')
        画板.添加一行('有效:', '矩形标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '矩形标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的矩形标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加角点:', '将指定的坐标点对象添加到矩形标记的对角点列表中')
        画板.添加一行('**角点', '可被添加为角点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('_添加到图层:',
                '根据矩形标记类数据结构的定义, 生成一个 folium.Rectangle 对象,并将该对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 folium.Rectangle 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.Rectangle 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 多边形标记类:
    """
    定义了多边形标记的数据结构，您可以通过 多边形标记类.帮助文档() 或者 多边形标记类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 角点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = None,
                 图形: 封闭图形样式类 = 封闭图形样式类(),
                 消息: str or 消息样式类 = None,
                 提示: str or 提示样式类 = None,
                 蚂蚁路径: 蚂蚁路径标记类 = 蚂蚁路径标记类()):
        self.角点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = 角点序列 if isinstance(角点序列,
                                                                                  list) else []
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.图形: 封闭图形样式类 = 图形 if isinstance(图形, 封闭图形样式类) else 封闭图形样式类()
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)
        self.蚂蚁路径: 蚂蚁路径标记类 = 蚂蚁路径 if isinstance(蚂蚁路径, 蚂蚁路径标记类) else 蚂蚁路径标记类()
        self.__GPS坐标系推理基准: GPS坐标系类型 = GPS坐标系类型.wgs84

    # region 访问器
    @property
    def 有效(self) -> bool:
        return True if isinstance(self.角点序列, list) and len(self.角点序列) > 2 else False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '多边形标记类':
        return 多边形标记类(_deepcopy(self.角点序列),
                      self.图形.副本,
                      self.消息.副本,
                      self.提示.副本,
                      self.蚂蚁路径.副本)

    def 添加角点(self, 角点: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类 or list) -> '多边形标记类':
        """
        将指定的角点对象添加到该多边形标记类对象的角点序列中来
        :param 角点: GPS坐标类对象, 图标标记类对象, 圆圈标记类对象, 正多边形标记类对象, 或者以上对象的列表
        :return: self
        """
        待添加角点: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = []
        if isinstance(角点, list):
            待添加角点 = 角点
        else:
            待添加角点.append(角点)

        for 点 in 待添加角点:
            if type(点) in [GPS坐标类, 图标标记类, 圆圈标记类, 正多边形标记类]:
                位置 = 点 if isinstance(点, GPS坐标类) else 点.位置
                if 位置.坐标系 == GPS坐标系类型.智能推理坐标:
                    位置.坐标系 = self.__GPS坐标系推理基准
                else:
                    self.__GPS坐标系推理基准 = 位置.坐标系
                self.角点序列.append(点)
        return self

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                if 目标坐标系 is None or 目标坐标系 == GPS坐标系类型.智能推理坐标:
                    目标坐标系 = self.__GPS坐标系推理基准

                # 生成路径点序列
                纬经度坐标序列: list[list[float, float]] = []
                for 路径点 in self.角点序列:
                    if isinstance(路径点, GPS坐标类) and 路径点.有效:
                        纬经度坐标序列.append(list(路径点.目标坐标(目标坐标系=目标坐标系))[::-1])
                    elif type(路径点) in [图标标记类, 圆圈标记类, 正多边形标记类] and 路径点.位置.有效:
                        纬经度坐标序列.append(list(路径点.位置.目标坐标(目标坐标系=目标坐标系))[::-1])

                # 处理线条样式
                if self.图形.线条颜色 is None:
                    self.图形.线条颜色 = 颜色名.黑
                if self.图形.线条宽度 < 0:
                    self.图形.线条宽度 = 1
                if self.图形.线条透明度 < 0:
                    self.图形.线条透明度 = 0.5
                if self.图形.填充:
                    if self.图形.填充色 is None:
                        self.图形.填充色 = 颜色名.灰
                    if self.图形.填充透明度 < 0:
                        self.图形.填充透明度 = 0.5

                _folium.Polygon(locations=纬经度坐标序列,
                                color=self.图形.线条颜色,
                                weight=self.图形.线条宽度,
                                opacity=self.图形.线条透明度,
                                fill=self.图形.填充,
                                fill_color=self.图形.填充色,
                                fill_opacity=self.图形.填充透明度,
                                popup=self.消息._popup对象,
                                tooltip=self.提示._toolTip对象).add_to(图层)

                for 点坐标 in self.角点序列:
                    if type(点坐标) in [图标标记类, 圆圈标记类, 正多边形标记类]:
                        点坐标._添加到图层(图层=图层, 目标坐标系=目标坐标系)

                if self.蚂蚁路径.显示:
                    if not self.蚂蚁路径.路径点序列:
                        self.蚂蚁路径.路径点序列 = self.角点序列
                    if self.蚂蚁路径.有效:
                        self.蚂蚁路径._添加到图层(图层=图层, 目标坐标系=目标坐标系)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('多边形标记类定义了一个多边形标记类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('点序列:',
                '以包括有位置[GPS坐标类]成员的类型对象或者GPS坐标类对象组成的对象列表,以定义多边形标记的一系列角点位置')
        画板.添加一行('', '可作为角点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('图形:', '封闭图形样式类, 定义了多边形标记的边框/线条样式以及内部区域的填充样式')
        画板.添加一行('消息:', '消息样式类对象,用于定义多边形标记需要显示的消息样式信息')
        画板.添加一行('提示:', '提示样式类对象,用于定义多边形标记需要显示的提示样式信息')
        画板.添加一行('蚂蚁路径:', '定义在多边形标记对象上显示的蚂蚁路径样式')
        画板.添加一行('有效:', '多边形标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '多边形标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的多边形标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加角点:', '将指定的坐标点对象添加到多边形的角点列表中')
        画板.添加一行('**角点', '可被添加为角点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('_添加到图层:',
                '根据多边形标记类数据结构的定义, 生成一个 folium.Polygon 对象,并将该对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 folium.Polygon 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.Polygon 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 折线类:
    """
    定义了折线标记的数据结构，您可以通过 折线类.帮助文档() 或者 折线类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = None,
                 显示转移方向: bool = False,
                 消息: str or 消息样式类 = None,
                 线条样式: 线条样式类 = 线条样式类(),
                 提示: str or 提示样式类 = None,
                 线上文本样式: 线上文本样式类 = 线上文本样式类(),
                 蚂蚁路径: 蚂蚁路径标记类 = 蚂蚁路径标记类()):
        self.路径点序列: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = 点序列 if isinstance(点序列,
                                                                                  list) else []
        self.显示转移方向: bool = 显示转移方向
        self.消息: 消息样式类 = 消息 if isinstance(消息, 消息样式类) else 消息样式类(
            消息=str(消息).strip() if 消息 else None)
        self.线条样式: 线条样式类 = 线条样式 if isinstance(线条样式, 线条样式类) else 线条样式类()
        self.提示: 提示样式类 = 提示 if isinstance(提示, 提示样式类) else 提示样式类(
            消息=str(提示).strip() if 提示 else None)
        self.线上文本样式: 线上文本样式类 = 线上文本样式 if isinstance(线上文本样式,
                                                    线上文本样式类) else 线上文本样式类()
        self.蚂蚁路径: 蚂蚁路径标记类 = 蚂蚁路径 if isinstance(蚂蚁路径, 蚂蚁路径标记类) else 蚂蚁路径标记类()
        self.__GPS坐标系推理基准: GPS坐标系类型 = GPS坐标系类型.wgs84
        if self.路径点序列:
            for 序号 in range(len(self.路径点序列)).__reversed__():
                路径点 = self.路径点序列[序号]
                路径点 = 路径点 if isinstance(路径点, GPS坐标类) else 路径点.位置
                if 路径点.坐标系 != GPS坐标系类型.智能推理坐标:
                    self.__GPS坐标系推理基准 = 路径点.坐标系
                    break

    # region 访问器
    @property
    def 有效(self) -> bool:
        return True if isinstance(self.路径点序列, list) and len(self.路径点序列) > 1 else False

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 副本(self) -> '折线类':
        return 折线类(_deepcopy(self.路径点序列),
                   self.显示转移方向,
                   self.消息.副本,
                   self.线条样式.副本,
                   self.提示.副本,
                   self.线上文本样式.副本,
                   self.蚂蚁路径.副本)

    def 线段中心点序列(self, 目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> list[_线段中点类]:
        """
        计算折线中每个一线段的中点位置,以及该线段的倾角,整理成 list[_线段中点类] 返回
        :param 目标坐标系: 指定坐标计算的基准GPS坐标系
        :return: list[_线段中点类]
        """
        if not self.路径点序列 or len(self.路径点序列) < 2:
            return []
        if 目标坐标系 == GPS坐标系类型.智能推理坐标:
            目标坐标系 = self.__GPS坐标系推理基准
        else:
            self.__GPS坐标系推理基准 = 目标坐标系

        中点序列: list[_线段中点类] = []
        for 路径点序号 in range(len(self.路径点序列) - 1):
            起点位置: GPS坐标类 = self.路径点序列[路径点序号] if isinstance(self.路径点序列[路径点序号], GPS坐标类) else \
                self.路径点序列[路径点序号].位置
            终点位置: GPS坐标类 = self.路径点序列[路径点序号 + 1] if isinstance(self.路径点序列[路径点序号 + 1],
                                                               GPS坐标类) else self.路径点序列[
                路径点序号 + 1].位置

            中点序列.append(_线段中点类(位置=起点位置.中点(目标点=终点位置, 目标坐标系=目标坐标系).墨卡托中点,
                               倾角=起点位置.倾角(目标点=终点位置, 目标坐标系=目标坐标系).墨卡托倾角deg))
        return 中点序列

    def 添加路径点(self, 路径点: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类 or list) -> '折线类':
        """
        将指定的坐标点添加到该折线类对象的路径点序列中来
        :param 路径点: GPS坐标类对象, 图标标记类对象, 圆圈标记类对象, 正多边形标记类对象, 或者以上对象的列表
        :return: self
        """
        待添加路径点: list[GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类] = []
        if isinstance(路径点, list):
            待添加路径点 = 路径点
        else:
            待添加路径点.append(路径点)

        for 点 in 待添加路径点:
            if type(点) in [GPS坐标类, 图标标记类, 圆圈标记类, 正多边形标记类]:
                位置 = 点 if isinstance(点, GPS坐标类) else 点.位置
                if 位置.坐标系 == GPS坐标系类型.智能推理坐标:
                    位置.坐标系 = self.__GPS坐标系推理基准
                else:
                    self.__GPS坐标系推理基准 = 位置.坐标系
                self.路径点序列.append(点)
        return self

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        :param 图层: folium.Map or folium.FeatureGroup; 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: GPS坐标系类型; 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                if 目标坐标系 is None or 目标坐标系 == GPS坐标系类型.智能推理坐标:
                    目标坐标系 = self.__GPS坐标系推理基准

                # 生成路径点序列
                纬经度坐标序列: list[list[float, float]] = []
                for 路径点 in self.路径点序列:
                    if isinstance(路径点, GPS坐标类) and 路径点.有效:
                        纬经度坐标序列.append(list(路径点.目标坐标(目标坐标系=目标坐标系))[::-1])
                    elif type(路径点) in [图标标记类, 圆圈标记类, 正多边形标记类] and 路径点.位置.有效:
                        纬经度坐标序列.append(list(路径点.位置.目标坐标(目标坐标系=目标坐标系))[::-1])

                if not 纬经度坐标序列:
                    return None

                # 处理线条样式
                if self.线条样式.颜色 is None:
                    self.线条样式.颜色 = 颜色名.黑
                if self.线条样式.透明度 < 0:
                    self.线条样式.透明度 = 1
                if self.线条样式.宽度 < 0:
                    self.线条样式.宽度 = 0.3

                # 生成一个 PloyLine 对象, 并将其添加到图层上
                折线 = _folium.PolyLine(
                    locations=纬经度坐标序列,
                    color=self.线条样式.颜色,
                    weight=self.线条样式.宽度,
                    opacity=self.线条样式.透明度,
                    popup=self.消息._popup对象,
                    tooltip=self.提示._toolTip对象).add_to(图层)

                # 如果需要标记线上文本, 则标记之
                if self.线上文本样式.有效:
                    _plugins.PolyLineTextPath(polyline=折线,
                                              text=self.线上文本样式.文本,
                                              repeat=self.线上文本样式.重复,
                                              center=self.线上文本样式.居中,
                                              below=self.线上文本样式.显示于路径下方,
                                              offset=self.线上文本样式.偏移量px,
                                              orientation=self.线上文本样式.旋转deg,
                                              attributes=self.线上文本样式.文本属性字典).add_to(图层)

                # 如果路径点上有图标,圆圈, 或者正多边形,则添加之
                for 点坐标 in self.路径点序列:
                    if type(点坐标) in [图标标记类, 圆圈标记类, 正多边形标记类]:
                        点坐标._添加到图层(图层=图层, 目标坐标系=目标坐标系)

                # 如果需要添加转移方向,则添加之
                if self.显示转移方向:
                    中点序列 = self.线段中心点序列(目标坐标系=目标坐标系)
                    for 中点 in 中点序列:
                        图形: 封闭图形样式类 = 封闭图形样式类(线条颜色=颜色名.红, 填充色=颜色名.红, 填充透明度=1)
                        箭头 = 正多边形标记类(位置=中点.位置, 半径px=8, 边数=3, 角度deg=-中点.倾角, 图形=图形)
                        箭头._添加到图层(图层=图层, 目标坐标系=目标坐标系)

                if self.蚂蚁路径.显示:
                    if not self.蚂蚁路径.路径点序列:
                        self.蚂蚁路径.路径点序列 = self.路径点序列
                    if self.蚂蚁路径.有效:
                        self.蚂蚁路径._添加到图层(图层=图层, 目标坐标系=目标坐标系)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('折线类定义了一个折线类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('点序列:',
                '以包括有位置[GPS坐标类]成员的类型对象或者GPS坐标类对象组成的对象列表,以定义折线形标记的一系列折点位置')
        画板.添加一行('', '可作为折点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('显示转移方向:', '是否在折线上以三角形的方式显示折线绘制的午后次序')
        画板.添加一行('消息:', '消息样式类对象,用于定义折线标记需要显示的消息样式信息')
        画板.添加一行('线条样式:', '线条样式类, 定义了折线标记的线条样式')
        画板.添加一行('提示:', '提示样式类对象,用于定义折线标记需要显示的提示样式信息')
        画板.添加一行('线上文本样式:', '线上文本样式类, 用于定义折线上显示的线上文本的样式信息')
        画板.添加一行('蚂蚁路径:', '定义在折线上显示的蚂蚁路径样式')
        画板.添加一行('有效:', '折线标记数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '折线标记数据是否无效, 无效为True, 有效为False')
        画板.添加一行('副本:', '返回一个新的折线标记类对象, 数据复制自当前的对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加路径点:', '将指定的路径点对象添加到折线的折点列表中')
        画板.添加一行('**路径点',
                '可被添加为路径点的对象类型有: GPS坐标类 or 图标标记类 or 圆圈标记类 or 正多边形标记类')
        画板.添加一行('_添加到图层:',
                '根据图标标记类数据结构的定义, 生成一个 folium.PolyLine 对象,并将该对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 folium.PolyLine 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 folium.PolyLine 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 参考线类:
    """
    定义了参考线的数据结构，您可以通过 参考线类.帮助文档() 或者 参考线类.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 参考点: GPS坐标类 = None,
                 旋转deg: float = 0.0,
                 参考消息: str = None,
                 线条样式: 线条样式类 = 线条样式类()):
        self.参考点: GPS坐标类 = 参考点
        self.旋转deg: float = 旋转deg if type(旋转deg) in [float, int] else 0
        self.参考消息: str = 参考消息
        self.线条样式: 线条样式类 = 线条样式 if isinstance(线条样式, 线条样式类) else 线条样式类()

    # region 访问器
    @property
    def 有效(self) -> bool:
        return self.参考点 and isinstance(self.参考点, GPS坐标类) and self.参考点.有效

    @property
    def 无效(self) -> bool:
        return not self.有效

    # endregion

    def _添加到图层(self, 图层: _folium.Map or _folium.FeatureGroup,
               目标坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> None:
        """
        以参考点为中心, 生成一个符合要求的折线,添加到图层上
        :param 图层: 用于收集 folium 对象的图层 或者 地图
        :param 目标坐标系: 目标图层的坐标系类型
        :return: None
        """
        if self.有效:
            if type(图层) in [_folium.Map, _folium.FeatureGroup]:
                # 处理目标坐标系
                目标坐标系 = GPS坐标系类型.智能推理坐标 if 目标坐标系 is None else 目标坐标系

                # 处理线条样式
                if self.线条样式.颜色 is None:
                    self.线条样式.颜色 = 颜色名.黑
                if self.线条样式.透明度 < 0:
                    self.线条样式.透明度 = 1
                if self.线条样式.宽度 < 0:
                    self.线条样式.宽度 = 0.3

                # 生成参考线上的文本样式
                线上文本样式 = 线上文本样式类(文本属性字典={'fill': 'gray', 'font-size': 14},
                                 偏移量px=12,
                                 重复=True)

                # 生成一个折线对象
                参考线 = 折线类(线条样式=self.线条样式)

                # 生成参考线的两个端点坐标, 及线上文本内容
                参考线端点1: GPS坐标类
                参考线端点2: GPS坐标类
                线上文本: str
                if self.旋转deg == 0:
                    # 这是一个参考纬线, 端点1位于左侧 -720 位置, 端点2位于右侧 720 位置
                    参考线端点1 = GPS坐标类(-720, self.参考点.目标坐标(目标坐标系)[1], 目标坐标系)
                    参考线端点2 = GPS坐标类(720, self.参考点.目标坐标(目标坐标系)[1], 目标坐标系)
                    线上文本 = ' ' * 5 + (
                        f'{"北纬" if 参考线端点1.纬度 > 0 else "南纬"}: {abs(参考线端点1.纬度)}' if not self.参考消息 else self.参考消息).strip() + ' ' * 5
                else:
                    # 暂不支持倾斜的参考线,如果有倾斜角度的,一律处理成经线
                    参考线端点1 = GPS坐标类(self.参考点.目标坐标(目标坐标系)[0], -90, 目标坐标系)
                    参考线端点2 = GPS坐标类(self.参考点.目标坐标(目标坐标系)[0], 90, 目标坐标系)
                    线上文本 = ' ' * 5 + (
                        f'{"东经" if 参考线端点1.经度 > 0 else "西经"}: {abs(参考线端点1.经度)}' if not self.参考消息 else self.参考消息).strip() + ' ' * 5

                # 完善参考线设置
                线上文本样式.文本 = 线上文本
                参考线.线上文本样式 = 线上文本样式
                参考线.添加路径点(参考线端点1)
                参考线.添加路径点(参考线端点2)

                # 把参考线添加到指定图层
                参考线._添加到图层(图层=图层, 目标坐标系=目标坐标系)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('参考线类定义了一个参考线类的数据结构')

        """
                参考点: GPS坐标类 = None,
                 旋转deg: float = 0.0,
                 参考消息: str = None,
                 线条样式: 线条样式类 = 线条样式类()):
                """

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('参考点:', 'GPS坐标类对象,用于定义参考线的位置')
        画板.添加一行('', '可作为参考点对象类型有: GPS坐标类')
        画板.添加一行('旋转deg:', '定义参考线相对于纬线方向的旋转角度。 0deg: 平行于纬线, 非0deg: 平行于经线')
        画板.添加一行('参考消息:', '消息样式类对象,用于定义参考线的需要显示的消息样式信息')
        画板.添加一行('线条样式:', '线条样式类, 定义了参考线的线条样式')
        画板.添加一行('有效:', '参考线数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '参考线数据是否无效, 无效为True, 有效为False')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('_添加到图层:',
                '根据参考线类数据结构的定义, 生成一个 折线类 对象,并将该 折线类 对象添加到指定的 folium.Map 或者 folium.FeatureGroup 对象中')
        画板.添加一行('**图层:', '指定需要添加 折线类 对象的 folium.Map 或者 folium.FeatureGroup 对象')
        画板.添加一行('**目标坐标系:',
                '指定需要添加 折线类 对象的 folium.Map 或者 folium.FeatureGroup 对象 的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class _热力层类:
    """
    定义了热力层的数据结构，您可以通过 热力层类.帮助文档() 或者 热力层类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 热力点序列: list[热力点类] = None,
                 图层名称: str = None,
                 默认显示: bool = False,
                 热力斑半径px: int = 25,
                 晕染宽度px: int = 15,
                 着色梯度字典: dict[float, str or 颜色名] = None):
        self.__热力点序列: list[热力点类] = [] if 热力点序列 is None else 热力点序列
        self.__图层名称: str = str(图层名称 if 图层名称 else '').strip()
        self.默认显示: bool = 默认显示
        self.热力斑半径px: int = 热力斑半径px
        self.晕染宽度px: int = 晕染宽度px
        self.着色梯度字典: dict[float, str or 颜色名] = 着色梯度字典

    # region 访问器
    @property
    def 有效(self) -> bool:
        热力点有效: bool = len(self.__热力点序列) > 0
        if 热力点有效:
            for 热力点 in self.__热力点序列:
                if 热力点.位置.无效:
                    热力点有效 = False
                    break
        return 热力点有效

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 可控制(self) -> bool:
        if self.有效 and self.__图层名称:
            if str(self.__图层名称).strip():
                return True
        return False

    @property
    def 热力点数量(self) -> int:
        return len(self.__热力点序列)

    # endregion

    def 添加热力点(self, 热力点: 热力点类 or GPS坐标类) -> '_热力层类':
        """
        将指定的热力点类, 或者 GPS坐标类, 添加到热力图层中来
        :param 热力点:  热力点类对象, 或者 GPS坐标类对象
        :return: self
        """
        if isinstance(热力点, 热力点类):
            self.__热力点序列.append(热力点)
        elif isinstance(热力点, GPS坐标类):
            self.__热力点序列.append(热力点类(位置=热力点))
        return self

    def _heatMap对象(self, 底图坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标) -> _plugins.HeatMap:
        """
        将热力数据 根据指定的坐标系生成 _plugins.HeatMap 对象并返回该对象
        :param 底图坐标系: 目标地图中的坐标系类型
        :return: _plugins.HeatMap 对象
        """
        if self.无效:
            return _plugins.HeatMap(data=[[0, 0, 1]])

        # 处理目标坐标系
        目标坐标系 = GPS坐标系类型.智能推理坐标 if 底图坐标系 is None else 底图坐标系

        # 处理入参值
        self.热力斑半径px = int(self.热力斑半径px) if type(self.热力斑半径px) in [float, int] else 25
        self.晕染宽度px = int(self.晕染宽度px) if type(self.晕染宽度px) in [float, int] else 15

        着色梯度字典有效: bool = isinstance(self.着色梯度字典, dict)
        着色梯度字典: dict[float, str] = {}
        if 着色梯度字典有效:
            for 分界点, 颜色值 in self.着色梯度字典.items():
                if type(分界点) not in [float, int]:
                    着色梯度字典有效 = False
                    break
                elif type(颜色值) not in [str, 颜色名]:
                    着色梯度字典有效 = False
                    break
                else:
                    着色梯度字典[float(分界点)] = str(颜色值.value if isinstance(颜色值, 颜色名) else 颜色值)
        if not 着色梯度字典有效:
            着色梯度字典 = {}

        # 整理热力点数据为 [lat, lng, weight or 1] 格式的的列表
        热力数据: list[list[float, float, float]] = []
        for 热力点 in self.__热力点序列:
            if 热力点.有效:
                热力数据.append([热力点.位置.目标坐标(目标坐标系)[1],
                             热力点.位置.目标坐标(目标坐标系)[0],
                             热力点.权值 if (type(热力点.权值) in [float, int]) and (热力点.权值 > 0) else 1])
        if 热力数据:
            return _plugins.HeatMap(data=热力数据,
                                    name=str(self.__图层名称).strip() if self.可控制 else None,
                                    radius=self.热力斑半径px,
                                    blur=self.晕染宽度px,
                                    gradient=着色梯度字典 if 着色梯度字典 else None,
                                    overlay=self.可控制,
                                    control=self.可控制,
                                    show=self.默认显示)

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('热力层类定义了一个热力层类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('热力点序列:',
                '一个由 GPS坐标类对象或者 热力点类 对象组成的对象序列, 热力点序列体现了不同位置的热力值信息')
        画板.添加一行('', '可作为热力点的对象类型有: GPS坐标类 or 热力点类')
        画板.添加一行('热力点数量', '热力图层上存在的热力点的数量')
        画板.添加一行('图层名称:', '热力层所在的图层的名称')
        画板.添加一行('默认显示:', '热力层图层是否默认为显示状态')
        画板.添加一行('热力斑半径px:', '每个热力点位置的热力斑点的半径')
        画板.添加一行('晕染宽度px:',
                '每个热力点位置的热力斑颜色梯度下降到零的宽度距离, 晕染宽度范围内的位置不再有热力值残留')
        画板.添加一行('着色梯度字典:', '字典定义了不同比位对应的颜色值')
        画板.添加一行('可控制:', '如果图层名称有效,则该图层可控制,否则不可控制')
        画板.添加一行('有效:', '热力图层数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '热力图层数据是否无效, 无效为True, 有效为False')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加热力点:', '将指定的 GPS坐标类对象 或者 热力点类对象添加到热力点列表中')
        画板.添加一行('**热力点', '可被添加为热力点的对象类型有: GPS坐标类 or 热力点类')
        画板.添加一行('heatMap对象:', '根据热力层数据结构的定义, 生成一个 plugins.HeatMap 对象, 并返回该对象')
        画板.添加一行('**目标坐标系:', '指定需要生成的 plugins.HeatMap 对象 所适配的的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class 图层类:
    """
    定义了图层的数据结构，您可以通过 图层类.帮助文档() 或者 图层类对象.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 图层名称: str = None,
                 默认显示: bool = False):
        self.__图层名称 = str(图层名称 if 图层名称 else '').strip()
        self.默认显示: bool = 默认显示
        self.标记序列: list[
            图标标记类 or 圆圈标记类 or 折线类 or 矩形标记类 or 多边形标记类 or 正多边形标记类 or 蚂蚁路径标记类] = []

    # region 访问器
    @property
    def 图层名称(self) -> str:
        return self.__图层名称

    @property
    def 有效(self) -> bool:
        return isinstance(self.标记序列, list) and len(self.标记序列) > 0

    @property
    def 无效(self) -> bool:
        return not self.有效

    @property
    def 可控制(self) -> bool:
        if self.有效 and self.__图层名称:
            if str(self.__图层名称).strip():
                return True
        return False

    # endregion
    def _featureGroup对象(self, 底图坐标系: GPS坐标系类型 = GPS坐标系类型.wgs84) -> _folium.FeatureGroup:
        # 生成 FeatureGroup 对象
        图层: _folium.FeatureGroup
        if self.可控制:
            图层 = _folium.FeatureGroup(name=str(self.__图层名称).strip(), control=True, show=self.默认显示)
        else:
            图层 = _folium.FeatureGroup(control=False)

        # 将元素添加到 FeatureGroup 对上上
        if self.标记序列:
            for 标记 in self.标记序列:
                标记._添加到图层(图层=图层, 目标坐标系=底图坐标系)

        # return FeatureGroup 对象
        return 图层

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('图层类定义了一个图层类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('图层名称:', '指定图层的名称')
        画板.添加一行('默认显示:', '图层是否默认为显示状态')
        画板.添加一行('标记序列:', '一个标记对象序列, 记录一不同位置处的不同的标记信息')
        画板.添加一行('',
                '可作标记对象的类型有: 图标标记类 or 圆圈标记类 or 折线类 or 多边形标记类 or 正多边形标记类 or 蚂蚁路径标记类')
        画板.添加一行('可控制:', '如果图层名称有效,则该图层可控制,否则不可控制')
        画板.添加一行('有效:', '图层数据是否有效, 有效为True, 无效为False')
        画板.添加一行('无效:', '图层数据是否无效, 无效为True, 有效为False')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('_featureGroup对象:', '根据图层数据结构的定义, 生成一个 folium.FeatureGroup 对象, 并返回该对象')
        画板.添加一行('**目标坐标系:', '指定需要生成的 folium.FeatureGroup 对象 所适配的的坐标系类型')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)


class _添加瓦片工具箱类:
    """
    本工具箱中所搜集的地图瓦片信息,参考自: https://blog.csdn.net/yz_weixiao/article/details/121971334
    您可以通过兴趣的瓦片地图方法查阅其 __doc__ 信息, 例如 对象.添加瓦片.高德地图.__doc__
    """

    def __init__(self, 地图: '地图类' = None):
        self.地图: '地图类' = 地图

    @property
    def 添加所有(self) -> '_添加瓦片工具箱类':
        self.OpenStreetMap()
        self.StamenToner()
        self.高德地图()
        self.高德中英地图()
        self.高德路网地图()
        self.高德卫星地图()
        self.智图GeoQ()
        self.智图GeoQ灰色版()
        self.智图GeoQ行政区划()
        self.智图GeoQ水系()
        self.智图GeoQ灰度路网()
        self.智图GeoQ暖色路网()
        self.腾讯地图()
        return self

    def OpenStreetMap(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def StamenToner(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 高德地图(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 高德中英地图(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 高德路网地图(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 高德卫星地图(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ灰色版(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ行政区划(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ水系(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ灰度路网(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 智图GeoQ暖色路网(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass

    def 腾讯地图(self, 瓦片名称: str = '') -> '_添加瓦片工具箱类':
        pass


class 地图类:
    """
    定义了地图的数据结构，您可以通过 地图类.帮助文档() 或者 地图类.帮助文档() 来打印相关的帮助信息
    """

    def __init__(self,
                 中心点: GPS坐标类 = None,
                 基准坐标系: GPS坐标系类型 = GPS坐标系类型.智能推理坐标,
                 初始缩放倍数: int = 5,
                 显示比例尺: bool = True):
        self.Map: _folium.Map or None = None
        self.初始缩放倍数: int = 初始缩放倍数
        self.显示比例尺: bool = 显示比例尺

        self.__基准瓦片: list[_folium.TileLayer] = []

        self.__本地资源优化器: callable = None
        self.__网络资源优化器: callable = None

        self.底图坐标系: GPS坐标系类型 = 基准坐标系
        self.__GPS坐标系推理基准: GPS坐标系类型 = self.底图坐标系

        self.__中心点: GPS坐标类 = 中心点 if isinstance(中心点, GPS坐标类) else GPS坐标类()

        # 地图数据
        self.__基地列表: list[图标标记类] = []

        self.__参考线列表: list[参考线类] = []

        self.__图层表: list[图层类 or _热力层类] = []

        # 是否允许位置拾取
        self.__位置拾取: bool = False

        # 是否允许点击标记
        self.__点击标记: bool = False

        # 是否允许鼠标绘图
        self.__鼠标绘图: bool = False

        # 是否允许测距
        self.__测距: bool = True

        # 网页标题, html 元素
        self.__网页标题: list[网页标题样式类] = []

        # 准备一个添加瓦片的工具箱
        self.添加瓦片 = _添加瓦片工具箱类(地图=self)
        self.添加瓦片.OpenStreetMap = self.__添加OpenStreetMap瓦片
        self.添加瓦片.StamenToner = self.__添加StamenToner瓦片
        self.添加瓦片.高德地图 = self.__添加高德地图瓦片
        self.添加瓦片.高德中英地图 = self.__添加高德中英地图瓦片
        self.添加瓦片.高德路网地图 = self.__添加高德路网地图瓦片
        self.添加瓦片.高德卫星地图 = self.__添加高德卫星地图瓦片
        self.添加瓦片.智图GeoQ = self.__添加智图GeoQ瓦片
        self.添加瓦片.智图GeoQ灰色版 = self.__添加智图GeoQ灰色版瓦片
        self.添加瓦片.智图GeoQ行政区划 = self.__添加智图GeoQ中国行政区划边界瓦片
        self.添加瓦片.智图GeoQ水系 = self.__添加智图GeoQ中国水系瓦片
        self.添加瓦片.智图GeoQ灰度路网 = self.__添加智图GeoQ灰度路网瓦片
        self.添加瓦片.智图GeoQ暖色路网 = self.__添加智图GeoQ暖色路网瓦片
        self.添加瓦片.腾讯地图 = self.__添加腾讯瓦片

    # region 访问器
    @property
    def 测距状态(self) -> bool:
        return self.__测距

    @property
    def 鼠标绘图状态(self) -> bool:
        return self.__鼠标绘图

    @property
    def 点击标记状态(self) -> bool:
        return self.__点击标记

    @property
    def 坐标拾取状态(self) -> bool:
        return self.__位置拾取

    @property
    def 中心点(self) -> GPS坐标类:
        if self.__中心点.有效:
            return self.__中心点.副本
        elif 有效基地坐标列表 := [标记.位置 for 标记 in self.__基地列表 if 标记.位置.有效]:
            经度和: float = sum([位置.wgs84坐标[0] for 位置 in 有效基地坐标列表])
            纬度和: float = sum([位置.wgs84坐标[1] for 位置 in 有效基地坐标列表])
            坐标数: int = len(有效基地坐标列表)
            return GPS坐标类(经度=经度和 / 坐标数, 纬度=纬度和 / 坐标数, 坐标系=GPS坐标系类型.wgs84)
        return GPS坐标类(0, 0)

    @中心点.setter
    def 中心点(self, 坐标: GPS坐标类):
        if isinstance(坐标, GPS坐标类):
            self.__中心点 = 坐标
        else:
            self.__中心点 = GPS坐标类()

    @property
    def 图层数量(self) -> int:
        return len(self.__图层表)

    @property
    def 网络资源字典(self) -> dict:
        global _网络资源字典
        return _deepcopy(_网络资源字典)

    @网络资源字典.setter
    def 网络资源字典(self, 字典: dict):
        _更新网络资源字典(字典=字典, 清空旧配置=True)

    @property
    def 本地资源字典(self) -> dict:
        global _本地资源字典
        return _本地资源字典

    @本地资源字典.setter
    def 本地资源字典(self, 字典: dict):
        _更新本地资源字典(字典=字典, 清空旧配置=True)

    @property
    def 缩放倍率字典(self) -> dict:
        global _缩放倍率字典
        return _缩放倍率字典

    @缩放倍率字典.setter
    def 缩放倍率字典(self, 字典: dict[float or int, int]):
        _更新缩放倍率字典(字典=字典, 清空旧配置=True)

    # endregion

    # region 瓦片处理
    def 添加地图瓦片(self, 瓦片: _folium.TileLayer, 瓦片坐标系: GPS坐标系类型 = GPS坐标系类型.wgs84) -> '地图类':
        """
        向 folium.Map 对象中添加 tiles 信息
        :param 瓦片: 指定要添加的瓦片对象(folium.TileLayer对象)
        :param 瓦片坐标系: 指定要添加的瓦片对象的坐标系, 如果这是每一个被添加的瓦片,则该座坐标系被识为 folium.Map 的基准坐标系
        :return:self
        """
        if isinstance(瓦片, _folium.TileLayer):
            瓦片可添加: bool = True
            if 瓦片.tiles in [瓦片.tiles for 瓦片 in self.__基准瓦片]:
                瓦片可添加 = False
            if 瓦片可添加 and 瓦片.tile_name and 瓦片.tile_name in [瓦片.tile_name for 瓦片 in self.__基准瓦片]:
                瓦片可添加 = False

            if 瓦片可添加:
                if not self.__基准瓦片 and self.__GPS坐标系推理基准 == GPS坐标系类型.智能推理坐标:
                    # 第一个添加的瓦片,会联动调整底图坐标系
                    self.底图坐标系 = 瓦片坐标系
                    self.__GPS坐标系推理基准 = self.底图坐标系
                self.__基准瓦片.append(瓦片)

        return self

    def __添加地图瓦片(self,
                 瓦片链接: str,
                 瓦片属性: str,
                 瓦片名称: str,
                 tms: bool = False,
                 瓦片坐标系: GPS坐标系类型 = GPS坐标系类型.wgs84) -> _添加瓦片工具箱类:
        瓦片属性 = str(瓦片属性).strip()
        瓦片链接 = str(瓦片链接).strip()
        瓦片名称 = str(瓦片名称 if 瓦片名称 else 'OpenStreetMap').strip()

        if 瓦片链接:
            瓦片: _folium.TileLayer
            if tms:
                瓦片 = _folium.TileLayer(tiles=瓦片链接,
                                       tms='true',
                                       attr=瓦片属性 if 瓦片属性 else None,
                                       name=瓦片名称 if 瓦片名称 else None)
            else:
                瓦片 = _folium.TileLayer(tiles=瓦片链接,
                                       attr=瓦片属性 if 瓦片属性 else None,
                                       name=瓦片名称 if 瓦片名称 else None)

            瓦片可添加: bool = True
            if 瓦片.tiles in [瓦片.tiles for 瓦片 in self.__基准瓦片]:
                瓦片可添加 = False
            if 瓦片可添加 and 瓦片.tile_name and 瓦片.tile_name in [瓦片.tile_name for 瓦片 in self.__基准瓦片]:
                瓦片可添加 = False

            if 瓦片可添加:
                if not self.__基准瓦片 and self.__GPS坐标系推理基准 == GPS坐标系类型.智能推理坐标:
                    # 第一个添加的瓦片,会联动调整底图坐标系
                    self.底图坐标系 = 瓦片坐标系
                    self.__GPS坐标系推理基准 = self.底图坐标系
                self.__基准瓦片.append(瓦片)
        return self.添加瓦片

    def __添加OpenStreetMap瓦片(self, 瓦片名称: str = 'OpenStreetMap') -> _添加瓦片工具箱类:
        """
        添加谷歌 OpenStreetMap 瓦片
        :param 瓦片名称: 默认值为 OpenStreetMap
        :return:_添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='OpenStreetMap',
            瓦片属性="",
            瓦片名称=瓦片名称)

    def __添加StamenToner瓦片(self, 瓦片名称: str = 'Stamen Toner') -> _添加瓦片工具箱类:
        """
        添加谷歌 Stamen Toner 瓦片, 黑白图瓦片
        :param 瓦片名称: 默认值为 Stamen Toner
        :return:_添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='Stamen Toner',
            瓦片属性="",
            瓦片名称=瓦片名称)

    def __添加高德地图瓦片(self, 瓦片名称: str = '高德地图') -> _添加瓦片工具箱类:
        """
        添加高德街景地图瓦片
        :param 瓦片名称: 默认值为 高德地图
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
            瓦片属性="&copy; <a target='_blank' href=https://www.amap.com>高德地图</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.高德地图坐标)

    def __添加高德中英地图瓦片(self, 瓦片名称: str = '高德中英地图') -> _添加瓦片工具箱类:
        """
        添加高德中英地图瓦片
        :param 瓦片名称: 默认值为 高德中英地图
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
            瓦片属性="&copy; <a target='_blank' href=https://www.amap.com>高德地图</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.高德地图坐标)

    def __添加高德路网地图瓦片(self, 瓦片名称: str = '高德路网地图') -> _添加瓦片工具箱类:
        """
        添加高德路网地图瓦片
        :param 瓦片名称: 默认值为 高德路网地图
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8&ltype=11',
            瓦片属性="&copy; <a target='_blank' href=https://www.amap.com>高德地图</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.高德地图坐标)

    def __添加高德卫星地图瓦片(self, 瓦片名称: str = '高德卫星地图') -> _添加瓦片工具箱类:
        """
        添加高德卫星地图瓦片
        :param 瓦片名称: 默认值为 高德卫星地图
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
            瓦片属性="&copy; <a target='_blank' href=https://www.amap.com>高德地图</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.高德地图坐标)

    def __添加智图GeoQ瓦片(self, 瓦片名称: str = '智图GeoQ') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ瓦片
        :param 瓦片名称: 默认值为 智图GeoQ
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加智图GeoQ灰色版瓦片(self, 瓦片名称: str = '智图GeoQ灰色版') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ灰色版瓦片
        :param 瓦片名称: 默认值为 智图GeoQ灰色版
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加智图GeoQ中国行政区划边界瓦片(self, 瓦片名称: str = '智图GeoQ中国行政区划边界') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ中国行政区划边界瓦片
        :param 瓦片名称: 默认值为 智图GeoQ中国行政区划边界
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://thematic.geoq.cn/arcgis/rest/services/ThematicMaps/administrative_division_boundaryandlabel/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加智图GeoQ中国水系瓦片(self, 瓦片名称: str = '智图GeoQ中国水系') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ中国水系瓦片
        :param 瓦片名称: 默认值为 智图GeoQ中国水系
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://thematic.geoq.cn/arcgis/rest/services/ThematicMaps/WorldHydroMap/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加智图GeoQ灰度路网瓦片(self, 瓦片名称: str = '智图GeoQ灰度路网') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ灰度路网瓦片
        :param 瓦片名称: 默认值为 智图GeoQ灰度路网
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://thematic.geoq.cn/arcgis/rest/services/StreetThematicMaps/Gray_OnlySymbol/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加智图GeoQ暖色路网瓦片(self, 瓦片名称: str = '智图GeoQ暖色路网') -> _添加瓦片工具箱类:
        """
        添加智图GeoQ暖色路网瓦片
        :param 瓦片名称: 默认值为 智图GeoQ暖色路网
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='http://thematic.geoq.cn/arcgis/rest/services/StreetThematicMaps/Warm_OnlySymbol/MapServer/tile/{z}/{y}/{x}',
            瓦片属性="&copy; <a target='_blank' href=https://www.geoq.cn>智图GeoQ</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.gcj02)

    def __添加腾讯瓦片(self, 瓦片名称: str = '腾讯地图') -> _添加瓦片工具箱类:
        """
        添加腾讯街景地图瓦片
        :param 瓦片名称: 腾讯地图
        :return: _添加瓦片工具箱类
        """
        return self.__添加地图瓦片(
            瓦片链接='https://rt0.map.gtimg.com/tile?z={z}&x={x}&y={-y}',
            瓦片属性="&copy; <a target='_blank' href=https://map.qq.com/m/index/map>腾讯地图</a>",
            瓦片名称=瓦片名称,
            瓦片坐标系=GPS坐标系类型.腾讯地图坐标)

    # endregion

    def 添加图层(self,
             图层名称: str = None,
             默认显示: bool = False) -> int:
        """
        向图层表中添加一个图层对象,并返回所添加的图层的图层号
        :param 图层名称: 图层的名称
        :param 默认显示: 是否默认显示这个图层
        :return: 所添加听图层的图层号, 如果添加不成功,则为-1
        """
        图层名称 = str(图层名称 if 图层名称 else '').strip()
        可添加: bool = True

        if 图层名称:
            if self.__图层表:
                if 图层名称 in [图层.图层名称 for 图层 in self.__图层表]:
                    可添加 = False

        if 可添加:
            # 如果图层可以添加, 则添加一个新的图层,并返回图层号
            self.__图层表.append(图层类(图层名称=图层名称, 默认显示=默认显示))
            return len(self.__图层表) - 1
        else:
            for 图层号 in range(len(self.__图层表)):
                if self.__图层表[图层号].图层名称 == 图层名称 and isinstance(self.__图层表[图层号], 图层类):
                    return 图层号

        # 如果以上努力均没有成果,则返回-1, 不指向任何图层
        return -1

    def 添加热力层(self,
              图层名称: str = None,
              默认显示: bool = False,
              热力斑半径px: int = 25,
              晕染宽度px: int = 15,
              着色梯度字典: dict[float, str or 颜色名] = None) -> int:
        """
        向图层表中添加一个热力层的图层, 并返回添加的图层号
        :param 图层名称: 所添加的图层的名称
        :param 默认显示: 是否默认显示这个图层
        :param 热力斑半径px: 热力点的斑点的半径
        :param 晕染宽度px: 热力点周围热力值消退的范围宽度
        :param 着色梯度字典: 定义给定的百分比位置处的颜色值
        :return: 所添加的图层的图层号, 如果添加不成功,则为-1
        """
        图层名称 = str(图层名称 if 图层名称 else '').strip()
        可添加: bool = True

        if 图层名称:
            if self.__图层表:
                if 图层名称 in [图层.图层名称 for 图层 in self.__图层表]:
                    可添加 = False

        if 可添加:
            # 如果图层可以添加, 则添加一个新的图层,并返回图层号
            self.__图层表.append(_热力层类(热力点序列=[],
                                    图层名称=图层名称,
                                    默认显示=默认显示,
                                    热力斑半径px=热力斑半径px,
                                    晕染宽度px=晕染宽度px,
                                    着色梯度字典=着色梯度字典))
            return len(self.__图层表) - 1
        else:
            for 图层号 in range(len(self.__图层表)):
                if self.__图层表[图层号].图层名称 == 图层名称 and isinstance(self.__图层表[图层号], _热力层类):
                    return 图层号

        # 如果以上努力均没有成果,则返回-1, 不指向任何图层
        return -1

    def 添加基地(self, 基地标记: GPS坐标类 or 图标标记类 or list[GPS坐标类 or 图标标记类]) -> '地图类':
        """
        向地图的底图中添加标记点,做为基地标记
        :param 基地标记: GPS坐标类, 或者 图标标记类, 或者是列表, 指定要添加的基地的位置
        :return: self
        """

        def 添加基地标记(标记: GPS坐标类 or 图标标记类) -> None:
            基地图标: 图标标记类
            if isinstance(标记, GPS坐标类):
                基地图标 = 图标标记类(位置=标记)
            elif isinstance(标记, 图标标记类):
                基地图标 = 标记
            else:
                基地图标 = 图标标记类()

            if 基地图标.位置.有效:
                if 基地图标.图标.无效:
                    if not 基地图标.图标.名称:
                        基地图标.图标.名称 = 'glyphicon-home'
                    if not 基地图标.图标.颜色:
                        基地图标.图标.颜色 = 颜色名.黑

                if 基地图标.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                    基地图标.位置.坐标系 = self.__GPS坐标系推理基准
                else:
                    self.__GPS坐标系推理基准 = 基地图标.位置.坐标系

                self.__基地列表.append(基地图标)

        待添加标记列表: list[GPS坐标类 or 图标标记类]
        if type(基地标记) is list:
            待添加标记列表 = 基地标记
        else:
            待添加标记列表 = [基地标记]

        for 标记 in 待添加标记列表:
            添加基地标记(标记=标记)
        return self

    def 添加热力点(self, 图层号: int, 热力点: GPS坐标类 or 热力点类 or list[GPS坐标类 or 热力点类]) -> '地图类':
        """
        将指定的 GPS坐标 或者 热力点 添加到指定的图层上
        :param 图层号: 指定的目标图层, 如果指定的图层不是热力层,则无法添加
        :param 热力点: GPS坐标对象, 或者是 热力点对象
        :return: self
        """
        if 0 <= 图层号 < self.图层数量 and isinstance(self.__图层表[图层号], _热力层类):
            待添加热力点: list[热力点类] = []
            if isinstance(热力点, 热力点类):
                待添加热力点.append(热力点)
            elif isinstance(热力点, GPS坐标类):
                待添加热力点.append(热力点类(位置=热力点))
            elif isinstance(热力点, list):
                for 这个点 in 热力点:
                    if isinstance(这个点, 热力点类):
                        待添加热力点.append(这个点)
                    elif isinstance(这个点, GPS坐标类):
                        待添加热力点.append(热力点类(位置=这个点))

            if 待添加热力点:
                # 推理GPS坐标系
                for 热点 in 待添加热力点:
                    if 热点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                        热点.位置.坐标系 = self.__GPS坐标系推理基准
                    else:
                        self.__GPS坐标系推理基准 = 热点.位置.坐标系

                    # 添加标记点
                    self.__图层表[图层号].添加热力点(热点)
        return self

    def 添加标记(self, 图层号: int, 标记点) -> '地图类':
        """
        向指定的图层添加标记点
        :param 图层号:  指定的目标图层, 如果指定的图层不是图层类,则无法添加
        :param 标记点: 类型为[图标标记类, 圆圈标记类, 折线类, 矩形标记类 , 多边形标记类, 正多边形标记类, 蚂蚁路径标记类]之一的对象
        :return: self
        """
        if 0 <= 图层号 < self.图层数量 and isinstance(self.__图层表[图层号], 图层类):
            # 整理出待添加的标记点
            待添加标记: list[
                图标标记类, 圆圈标记类, 折线类, 矩形标记类, 多边形标记类, 正多边形标记类, 蚂蚁路径标记类] = []
            if type(标记点) in [图标标记类, 圆圈标记类, 折线类, 矩形标记类, 多边形标记类, 正多边形标记类,
                             蚂蚁路径标记类]:
                待添加标记.append(标记点)
            elif isinstance(标记点, list):
                for 这个点 in 标记点:
                    if type(这个点) in [图标标记类, 圆圈标记类, 折线类, 矩形标记类, 多边形标记类, 正多边形标记类,
                                     蚂蚁路径标记类]:
                        待添加标记.append(这个点)

            if 待添加标记:
                for 标记 in 待添加标记:
                    # 推理坐标系类型
                    if type(标记) in [图标标记类, 圆圈标记类]:
                        if 标记.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                            标记.位置.坐标系 = self.__GPS坐标系推理基准
                        else:
                            self.__GPS坐标系推理基准 = 标记.位置.坐标系
                    elif isinstance(标记, 折线类) or isinstance(标记, 蚂蚁路径标记类):
                        if 标记.路径点序列:
                            for 路径点 in 标记.路径点序列:
                                if type(路径点) in [图标标记类, 圆圈标记类]:
                                    if 路径点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                        路径点.位置.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 路径点.位置.坐标系
                                elif isinstance(路径点, GPS坐标类):
                                    if 路径点.坐标系 == GPS坐标系类型.智能推理坐标:
                                        路径点.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 路径点.坐标系
                        if isinstance(标记, 折线类):
                            if 标记.蚂蚁路径.路径点序列:
                                for 路径点 in 标记.蚂蚁路径.路径点序列:
                                    if type(路径点) in [图标标记类, 圆圈标记类]:
                                        if 路径点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                            路径点.位置.坐标系 = self.__GPS坐标系推理基准
                                        else:
                                            self.__GPS坐标系推理基准 = 路径点.位置.坐标系
                                    elif isinstance(路径点, GPS坐标类):
                                        if 路径点.坐标系 == GPS坐标系类型.智能推理坐标:
                                            路径点.坐标系 = self.__GPS坐标系推理基准
                                        else:
                                            self.__GPS坐标系推理基准 = 路径点.坐标系
                    elif isinstance(标记, 多边形标记类):
                        if 标记.角点序列:
                            for 角点 in 标记.角点序列:
                                if type(角点) in [图标标记类, 圆圈标记类]:
                                    if 角点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                        角点.位置.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 角点.位置.坐标系
                                elif isinstance(角点, GPS坐标类):
                                    if 角点.坐标系 == GPS坐标系类型.智能推理坐标:
                                        角点.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 角点.坐标系
                        if 标记.蚂蚁路径.路径点序列:
                            for 角点 in 标记.蚂蚁路径.路径点序列:
                                if type(角点) in [图标标记类, 圆圈标记类]:
                                    if 角点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                        角点.位置.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 角点.位置.坐标系
                                elif isinstance(角点, GPS坐标类):
                                    if 角点.坐标系 == GPS坐标系类型.智能推理坐标:
                                        角点.坐标系 = self.__GPS坐标系推理基准
                                    else:
                                        self.__GPS坐标系推理基准 = 角点.坐标系
                    elif isinstance(标记, 矩形标记类):
                        for 角点 in 标记.对角点序列:
                            if type(角点) in [图标标记类, 圆圈标记类]:
                                if 角点.位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                    角点.位置.坐标系 = self.__GPS坐标系推理基准
                                else:
                                    self.__GPS坐标系推理基准 = 角点.位置.坐标系
                            elif isinstance(角点, GPS坐标类):
                                if 角点.坐标系 == GPS坐标系类型.智能推理坐标:
                                    角点.坐标系 = self.__GPS坐标系推理基准
                                else:
                                    self.__GPS坐标系推理基准 = 角点.坐标系
                    elif isinstance(标记, 正多边形标记类):
                        位置: GPS坐标类 = 标记.位置 if isinstance(标记, 图标标记类) else 标记.位置
                        if 位置.有效:
                            if 位置.坐标系 == GPS坐标系类型.智能推理坐标:
                                位置.坐标系 = self.__GPS坐标系推理基准
                            else:
                                self.__GPS坐标系推理基准 = 位置.坐标系
                    # 添加标记点
                    self.__图层表[图层号].标记序列.append(标记)
        return self

    def 添加参考纬线(self,
               参考点: GPS坐标类 or list[GPS坐标类] = GPS坐标类(0, 0),
               参考消息: str = None,
               线条样式: 线条样式类 = 线条样式类()) -> None:
        """
        向地图的底图中添加一个平行于纬线的折线线段作为参考线,这个参考线经过指定的坐标点
        :param 参考点: 所添加的参考线需要经过的参考点, GPS坐标类对象,或者是列表
        :param 参考消息: 所添加的参考线需要显示的弹窗消息
        :param 线条样式: 所添加的参考线的线形样式
        :return: self
        """
        if isinstance(参考点, GPS坐标类) and 参考点.有效:
            参考线: 参考线类 = 参考线类(参考点=参考点,
                             旋转deg=0,
                             参考消息=参考消息,
                             线条样式=线条样式)
            self.__参考线列表.append(参考线)
        elif isinstance(参考点, list):
            for 点 in 参考点:
                if isinstance(点, GPS坐标类) and 点.有效:
                    参考线: 参考线类 = 参考线类(参考点=点,
                                     旋转deg=0,
                                     参考消息=参考消息,
                                     线条样式=线条样式)
                    self.__参考线列表.append(参考线)

    def 添加参考经线(self,
               参考点: GPS坐标类 or list[GPS坐标类] = GPS坐标类(0, 0),
               参考消息: str = None,
               线条样式: 线条样式类 = 线条样式类()) -> None:
        """
        向地图的底图中添加一个平行于经线的折线线段作为参考线,这个参考线经过指定的坐标点
        :param 参考点: 所添加的参考线需要经过的参考点, GPS坐标类对象,或者是列表
        :param 参考消息: 所添加的参考线需要显示的弹窗消息
        :param 线条样式: 所添加的参考线的线形样式
        :return: self
        """
        if isinstance(参考点, GPS坐标类) and 参考点.有效:
            参考线: 参考线类 = 参考线类(参考点=参考点,
                             旋转deg=90,
                             参考消息=参考消息,
                             线条样式=线条样式)
            self.__参考线列表.append(参考线)
        elif isinstance(参考点, list):
            for 点 in 参考点:
                if isinstance(点, GPS坐标类) and 点.有效:
                    参考线: 参考线类 = 参考线类(参考点=点,
                                     旋转deg=90,
                                     参考消息=参考消息,
                                     线条样式=线条样式)
                    self.__参考线列表.append(参考线)

    def 添加参考经纬线(self,
                参考点: GPS坐标类 or list[GPS坐标类] = GPS坐标类(0, 0),
                参考消息: str = None,
                线条样式: 线条样式类 = None):
        """
        根据指定参数,向指定的参考点位置添加一条平行于纬线的参考线,再添加一条平行于经线的参考线
        :param 参考点: 指定要添加的参考线所经过的参考点
        :param 参考消息: 所添加的参考线需要显示的弹窗消息
        :param 线条样式: 所添加的参考线的线形样式
        :return: self
        """
        # 先添加经线
        self.添加参考经线(参考点=参考点, 参考消息=参考消息, 线条样式=线条样式)
        # 再添加纬线
        self.添加参考纬线(参考点=参考点, 参考消息=参考消息, 线条样式=线条样式)

    def 添加网页标题(self,
               标题样式或者文本: 网页标题样式类 or str = None,
               标题级别: int = None,
               文本尺寸px: int = None,
               文本颜色: str or 颜色名 = None,
               文本对齐: str = None,
               文本字体: str = None,
               文本属性字典: dict = None) -> '地图类':
        """
        向地图中添加一行 html h1/h2/h3/h4/h5 元素作为标题,这个标题将独站一行显示于地图内容的上方
        @param 标题样式或者文本: 网页标题样式类 对象,或者直接是标题文本
        @param 标题级别: 用于定义标题的级别, 1~5
        @param 文本尺寸px: 用于定义标题的字体尺寸
        @param 文本颜色: 用于定义标题的字体颜色
        @param 文本对齐: 用于定义标题的文本对齐方式
        @param 文本字体: 用于定义标题的字体
        @param 文本属性字典: 一个字典, 用于定义标题的属性及对应值
        @return: self
        """
        这个标题: 网页标题样式类
        if isinstance(标题样式或者文本, 网页标题样式类):
            这个标题 = 标题样式或者文本
        else:
            这个标题 = 网页标题样式类(标题文本=str(标题样式或者文本).strip())

        if type(标题级别) in [int, float] and 0 < 标题级别 <= 5:
            这个标题.标题级别 = 标题级别
        if isinstance(文本尺寸px, int):
            这个标题.文本尺寸px = 文本尺寸px
        if type(文本颜色) in [str, 颜色名]:
            这个标题.文本颜色 = 文本颜色
        if str(文本对齐) in 'lcr':
            这个标题.文本对齐 = str(文本对齐)[0]
        if 文本字体:
            这个标题.文本字体 = str(文本字体).strip()
        if isinstance(文本属性字典, dict):
            这个标题.文本属性字典 = 文本属性字典

        self.__网页标题.append(这个标题)
        return self

    def 支持测距(self) -> '地图类':
        """
        在folium对象中增加测距插件
        """
        self.__测距 = True
        return self

    def 禁止测距(self) -> '地图类':
        """
        在folium对象中不增加测距插件
        """
        self.__测距 = False
        return self

    def 支持鼠标绘图(self) -> '地图类':
        """
        在folium对象中增加鼠标绘图支持
        """
        self.__鼠标绘图 = True
        return self

    def 禁止鼠标绘图(self) -> '地图类':
        """
        在folium对象中不增加鼠标绘图支持
        """
        self.__鼠标绘图 = False
        return self

    def 支持点击标记(self) -> '地图类':
        """
        在folium对象中增加鼠标点南增加marker的支持
        """
        self.__点击标记 = True
        return self

    def 禁止点击标记(self) -> '地图类':
        """
        在folium对象中不增加鼠标点南增加marker的支持
        """
        self.__点击标记 = False
        return self

    def 支持坐标拾取(self) -> '地图类':
        """
        在folium对象中增加鼠标拾取GPS坐标的能力
        """
        self.__位置拾取 = True
        return self

    def 禁止坐标拾取(self) -> '地图类':
        """
        在folium对象中不增加鼠标拾取GPS坐标的能力
        """
        self.__位置拾取 = False
        return self

    def 智能定心(self, *参考点) -> bool:
        """
        根据给定的参考点,设置地图的中心点,如果给定的参考点有多个,则根据 _缩放倍率字典 的设置自适应调整地图的缩放倍率
        :return: 如果检测到至少有一个有效的 GPS坐标类 对象,则返回True
        """
        有效坐标点序列: list[GPS坐标类] = []
        for 点 in 参考点:
            if isinstance(点, GPS坐标类) and 点.有效:
                有效坐标点序列.append(点)

        if not 有效坐标点序列:
            return False
        if len(有效坐标点序列) == 1:
            self.__中心点 = 有效坐标点序列[0]
            return True

        最高纬度wgs84: float = max([点.wgs84坐标[1] for 点 in 有效坐标点序列])
        最低纬度wgs84: float = min([点.wgs84坐标[1] for 点 in 有效坐标点序列])
        最大经度wgs84: float = max([点.wgs84坐标[0] for 点 in 有效坐标点序列])
        最小经度wgs84: float = min([点.wgs84坐标[0] for 点 in 有效坐标点序列])

        距离参考纬度wgs84: float = 0
        if 最高纬度wgs84 * 最低纬度wgs84 > 0:
            距离参考纬度wgs84 = 最低纬度wgs84 if math.fabs(最低纬度wgs84) < math.fabs(最高纬度wgs84) else 最高纬度wgs84

        # 以最大轮廓的矩形几何中心点为地图中心点
        self.__中心点 = GPS坐标类(经度=(最大经度wgs84 + 最小经度wgs84) * 0.5,
                            纬度=(最高纬度wgs84 + 最低纬度wgs84) * 0.5,
                            坐标系=GPS坐标系类型.wgs84)

        东西距离西端点: GPS坐标类 = GPS坐标类(经度=最小经度wgs84, 纬度=距离参考纬度wgs84, 坐标系=GPS坐标系类型.wgs84)
        东西距离东端点: GPS坐标类 = GPS坐标类(经度=最大经度wgs84, 纬度=距离参考纬度wgs84, 坐标系=GPS坐标系类型.wgs84)
        东西宽度km: float = math.fabs(东西距离西端点.球面距离(东西距离东端点).km)

        南北距离北端点: GPS坐标类 = GPS坐标类(经度=最大经度wgs84, 纬度=最高纬度wgs84, 坐标系=GPS坐标系类型.wgs84)
        南北距离南端点: GPS坐标类 = GPS坐标类(经度=最大经度wgs84, 纬度=最低纬度wgs84, 坐标系=GPS坐标系类型.wgs84)
        南北宽度km: float = math.fabs(南北距离南端点.球面距离(南北距离北端点).km)

        参考宽度km: float = max(东西宽度km, 南北宽度km)

        self.初始缩放倍数 = _缩放倍率(参考距离km=参考宽度km)
        return True

    @classmethod
    def 网络资源字典调整(cls, 字典: dict) -> int:
        """
        使用指定的字典配置来调整 _网络资源字典 中的对应的配置项目,如果 _网络资源字典 中不存在的项目,则增加之
        :param 字典: 以字典方式定义的配置参数{资源项目/名称: {'isReg": bool, 'isDelet": bool, 'tgtStr': str}}
        :return: int 更新的配置数量
        """
        return _更新网络资源字典(字典=字典, 清空旧配置=False)

    @classmethod
    def 本地资源字典调整(cls, 字典: dict) -> int:
        """
        使用指定的字典配置来调整 _本地资源字典 中的对应的配置项目,如果 _网络资源字典 中不存在的项目,则增加之
        :param 字典: 以字典方式定义的配置参数{资源项目/名称: {'isReg": bool, 'isDelet": bool, 'tgtStr': str}}
        :return: int 更新的配置数量
        """
        return _更新本地资源字典(字典=字典, 清空旧配置=False)

    @classmethod
    def 缩放倍率字典调整(cls, 字典: dict[float or int, int]) -> int:
        """
        使用指定的字典配置来调整 _缩放倍率字典 中的对应的配置项目,如果 _缩放倍率字典 中不存在的项目,则增加之
        :param 字典: 以字典方式定义的配置参数{参考距离(km)上限(>0): 适用的地图缩放倍率(0~18)}
        :return: int 更新的配置数量
        """
        return _更新缩放倍率字典(字典=字典, 清空旧配置=False)

    def 优化网络资源(self) -> '地图类':
        """
        使用 _网络资源字典 中定义优化配置,对html文档中的 js/css 资源引用进行优化
        """

        def 网络资源优化(html文档: str):
            if not _os.path.isfile(html文档):
                return None

            global _网络资源字典
            if not (isinstance(_网络资源字典, dict) and _网络资源字典):
                return None

            try:
                with open(html文档, "r", encoding="utf-8") as 原文档, open("%s.bak" % html文档, "w",
                                                                      encoding="utf-8") as 目标文档:
                    for 行数据 in 原文档:
                        if '<script src=' in 行数据 or ('<link' in 行数据 and 'href=' in 行数据):
                            # 如果这行是一个script标签,或者是一个 link标签,则判断是否需要做处理, 并在必要的时候进行处理
                            for 键, 配置 in _网络资源字典.items():
                                # 对每一个配置项,判断是否命中和处理
                                if 键 and isinstance(配置, dict):
                                    # 提取配置项和配置参数
                                    isReg: bool = 配置['isReg'] if 配置['isReg'] else False
                                    isDelet: bool = 配置['isDelet'] if 配置['isDelet'] else False
                                    tgtStr: str = str(配置['tgtStr']) if 配置['tgtStr'] else ''

                                    # 判断是否命中/是否需要处理
                                    需要处理: bool
                                    if isReg:
                                        需要处理 = _re.search(键, 行数据) is not None
                                    else:
                                        需要处理 = 键 in 行数据

                                    # 如果需要处理,则处理之
                                    if 需要处理:
                                        if isDelet:
                                            行数据 = ''
                                        elif isReg:
                                            行数据 = _re.sub(键, tgtStr, 行数据)
                                        else:
                                            行数据 = 行数据.replace(键, tgtStr)
                        目标文档.write(行数据)
                _os.remove(html文档)
                _os.rename("%s.bak" % html文档, html文档)
            except Exception as exp:
                raise exp
            return None

        self.__网络资源优化器 = 网络资源优化
        return self

    def 网络资源本地化(self) -> '地图类':
        """
        使用 _本地资源字典 中定义优化配置,对html文档中的 js/css 资源引用进行优化
        """

        def 网络资源重定向(html文档: str):
            if not _os.path.isfile(html文档):
                return None

            global _本地资源字典
            if not (isinstance(_本地资源字典, dict) and _本地资源字典):
                return None

            try:
                with open(html文档, "r", encoding="utf-8") as 原文档, open("%s.bak" % html文档, "w",
                                                                      encoding="utf-8") as 目标文档:
                    for 行数据 in 原文档:
                        if '<script src=' in 行数据 or ('<link' in 行数据 and 'href=' in 行数据):
                            # 如果这行是一个script标签,或者是一个 link标签,则判断是否需要做处理, 并在必要的时候进行处理
                            for 键, 配置 in _本地资源字典.items():
                                # 对每一个配置项,判断是否命中和处理
                                if 键 and isinstance(配置, dict):
                                    # 提取配置项和配置参数
                                    isReg: bool = 配置['isReg'] if 配置['isReg'] else False
                                    isDelet: bool = 配置['isDelet'] if 配置['isDelet'] else False
                                    tgtStr: str = str(配置['tgtStr']) if 配置['tgtStr'] else ''

                                    # 判断是否命中/是否需要处理
                                    需要处理: bool
                                    if isReg:
                                        需要处理 = _re.search(键, 行数据) is not None
                                    else:
                                        需要处理 = 键 in 行数据

                                    # 如果需要处理,则处理之
                                    if 需要处理:
                                        if isDelet:
                                            行数据 = ''
                                        elif isReg:
                                            行数据 = _re.sub(键, tgtStr, 行数据)
                                        else:
                                            行数据 = 行数据.replace(键, tgtStr)
                        目标文档.write(行数据)
                _os.remove(html文档)
                _os.rename("%s.bak" % html文档, html文档)
            except Exception as exp:
                raise exp
            return None

        self.__本地资源优化器 = 网络资源重定向
        return self

    def 生成Map对象(self,
                画板: _打印模板 = None) -> _folium.Map:
        """
        处理地图对象中的数据,整理生成folium.Map对象
        @param 画板: 调试模板对象,用于输出控制台消息
        @return: folium.Map
        """
        画板 = 画板 if 画板 else _打印模板()
        画板.执行位置(self.生成Map对象)

        # region 生成 Map 对象
        self.Map = _folium.Map(location=self.中心点.目标坐标(self.底图坐标系)[::-1],
                               zoom_start=self.初始缩放倍数,
                               control_scale=self.显示比例尺,
                               min_zoom=0,
                               max_zoom=19,
                               tiles=None if self.__基准瓦片 else 'OpenStreetMap')
        # endregion

        # region 如果有网页标题,则添加网页标题
        if self.__网页标题:
            for 标题 in self.__网页标题:
                if 标题.有效:
                    self.Map.get_root().html.add_child(_folium.Element(标题.html))
        # endregion

        # region 处理瓦片层底图
        瓦片数量: int = 0
        if self.__基准瓦片:
            瓦片数量 = len(self.__基准瓦片)
            for 瓦片 in self.__基准瓦片:
                瓦片.control = 瓦片数量 > 1
                瓦片.overlay = False  # 瓦片层设置为单选模式
                瓦片.add_to(self.Map)
        # endregion

        # region 插件准备
        # region 添加 坐标拾取功能
        if self.__位置拾取:
            self.Map.add_child(_folium.LatLngPopup())
        # endregion

        # region 添加 点击标记功能
        if self.__点击标记:
            self.Map.add_child(_folium.ClickForMarker(popup="标记点"))
        # endregion

        # region 添加 鼠标绘图功能
        if self.__鼠标绘图:
            self.Map.add_child(_plugins.Draw())
        # endregion

        # region 添加测距能力
        if self.__测距:
            self.Map.add_child(_plugins.MeasureControl())
        # endregion
        # endregion

        # region 处理底图上的元素
        # region 添加基地标记
        if 有效基地列表 := [标记 for 标记 in self.__基地列表 if 标记.有效]:
            for 标记 in 有效基地列表:
                标记._添加到图层(图层=self.Map, 目标坐标系=self.底图坐标系)
        # endregion
        # region 添加参考线
        if self.__参考线列表:
            for 参考线 in self.__参考线列表:
                参考线._添加到图层(图层=self.Map, 目标坐标系=self.底图坐标系)
        # endregion
        # endregion

        # region 处理图层信息
        控制层数量: int = 0
        if self.__图层表:
            for 图层 in self.__图层表:
                if isinstance(图层, 图层类) and 图层.有效:
                    self.Map.add_child(图层._featureGroup对象(底图坐标系=self.底图坐标系))
                elif isinstance(图层, _热力层类) and 图层.有效:
                    图层._heatMap对象(底图坐标系=self.底图坐标系).add_to(self.Map)
                if 图层.可控制:
                    控制层数量 += 1
        # endregion

        # region 如果有控制需求, 或者瓦片数量大于1, 则添加控制层以体现控制层信息和瓦片信息
        if 控制层数量 > 0 or 瓦片数量 > 1:
            self.Map.add_child(
                _folium.LayerControl(
                    collapsed=False if (控制层数量 + (瓦片数量 if 瓦片数量 > 1 else 0) < 10) else True,
                    autoZIndex=True))
        # endregion

        return self.Map

    def 展示地图(self, dispaly: callable, 重新生成Map数据: bool = True, 画板: _打印模板 = None) -> None:
        """
        使用指定的 display 方法处理 folium.Map 对象
        :param 重新生成Map数据: 在展示 folium.Map 前是否根据地图类结构的数据重新生成 folium.Map 对象
        :param dispaly: 指定的处理方法
        :param 画板: 调试模板对象,用于进行控制台消息的打印输出
        :return: None
        """
        画板 = 画板 if 画板 else _打印模板()
        画板.执行位置(self.展示地图)

        # 生成地图
        if not isinstance(self.Map, _folium.Map) or 重新生成Map数据:
            self.生成Map对象(画板=画板.副本.缩进())

        # 展示地图
        if callable(dispaly):
            dispaly(self.Map)
        else:
            画板.提示错误('display 方法不可调用')

    def 保存html(self, 文档名: str = None, 目标路径: str = None, 重新生成Map数据: bool = True, 画板: _打印模板 = None):
        """
        将 folium.Map 对象保存为 html 文档, 并根据需要将其自动打印
        :param 重新生成Map数据: 在保存html前是否根据地图类结构的数据重新生成 folium.Map 对象
        :param 文档名: 生成的html文档名称
        :param 目标路径: 生成的html文档的路径
        :param 画板: 调试模板对象,用于输出控制台文本
        :return: None
        """
        画板 = 画板 if 画板 else _打印模板()
        画板.执行位置(self.保存html)

        class 次级方法:
            def __init__(self, 地图文档: str = None, 画板: _打印模板 = None):
                self.地图文档 = 地图文档
                self.__画板 = 画板 if 画板 else _打印模板()

            def 打开(self) -> None:
                self.__画板.执行位置(self.打开)

                if self.地图文档:
                    if _os.path.isfile(self.地图文档):
                        _webbrowser.open(self.地图文档)
                    else:
                        self.__画板.提示错误(f'无法打开地图文档,文档[{self.地图文档}]不存在')

                return None

            def __str__(self) -> str:
                return str(self.地图文档)

        生成结果 = 次级方法(画板=画板.副本.缩进())

        # region 处理 html 文档名
        画板.准备表格()
        if not 文档名 or not (文档名 := str(文档名).strip()):
            文档名 = f"foliumMap {_datetime.now().strftime('%Y%m%dT%H%M%S')}"
        文档名 = 文档名 if 文档名.endswith('.html') else f'{文档名}.html'
        画板.添加一行('文档名', 文档名)

        if not 目标路径 or not _os.path.isdir(目标路径) or not _os.path.exists(目标路径):
            画板.提示错误(f'目标路径[{目标路径}]无效')
            目标路径 = _os.path.dirname(__file__)

        if _os.path.dirname(__file__) == 目标路径:
            画板.提示错误(f'目标路径[{目标路径}]不允许生成 html 文档,请重新指定')
            return 生成结果

        目标路径 = 目标路径 if not 目标路径.endswith('\\') else 目标路径[:-1]
        画板.添加一行('目标路径', 目标路径)

        画板.展示表格()
        # endregion

        # region 生成 html 文档
        if not isinstance(self.Map, _folium.Map) or 重新生成Map数据:
            self.生成Map对象(画板=画板.副本.缩进())

        try:
            生成结果.地图文档 = f'{目标路径}\\{文档名}'
            self.Map.save(生成结果.地图文档)
            画板.消息('地图文档html已经生成:', 生成结果.地图文档)
        except Exception as exp:
            画板.提示错误('生成 html 文档遇到异常:', exp)
            生成结果.地图文档 = ''
        else:
            # html资源置换
            if self.__本地资源优化器 and callable(self.__本地资源优化器):
                try:
                    self.__本地资源优化器(生成结果.地图文档)
                except Exception as exp1:
                    画板.提示错误('资源替换遇到异常:', exp1)
                    生成结果.地图文档 = ''
            # 网络资源优化
            if self.__网络资源优化器 and callable(self.__网络资源优化器):
                try:
                    self.__网络资源优化器(生成结果.地图文档)
                except Exception as exp1:
                    画板.提示错误('优化网络资源(js/css)遇到异常:', exp1)
                    生成结果.地图文档 = ''
        # endregion

        # region 收尾
        return 生成结果
        # endregion

    @staticmethod
    def 帮助文档(打印方法: callable = None) -> None:
        画板: _打印模板 = _打印模板()

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)
        画板.添加分隔行('地图类定义了一个地图类的数据结构')

        if callable(打印方法):
            画板.添加一行('属性', '说明')
        else:
            画板.添加一行('属性', '说明').修饰行(_青字)
        画板.添加一行('地图:', 'folium.Map 对象')
        画板.添加一行('初始缩放倍数:', '地图文档打开时的地图初始缩放倍数')
        画板.添加一行('底图坐标系:', 'folium.Map 对象的基准GPS坐标系')
        画板.添加一行('添加瓦片:',
                '一个工具箱成员,用于向地图添加不同的地图瓦片, 你可以通过 地图类.添加瓦片.__doc__ 查阅更多说明')
        画板.添加一行('测距状态:', '显示当前是否允许向html地图中添加测距插件')
        画板.添加一行('鼠标绘图状态:', '显示当前是否允许向html地图中添加鼠标绘图插件')
        画板.添加一行('点击标记状态:', '显示当前是否允许向html地图中添加点击标记插件')
        画板.添加一行('坐标拾取状态:', '显示当前是否允许向html地图中添加坐标拾取插件')
        画板.添加一行('中心点:',
                '读取或者设置 folium.Map 对像的中心点,如果未指定中心点,则根据已经设置的基地坐标计算数据中心点')
        画板.添加一行('图层数量:',
                '当前 地图类 对象中的 图层类 和 热力层类 对象的数量, 不一定为html地图中显示的图层数量')
        画板.添加一行('网络资源字典', '设置/返回 _网络资源字典 的拷贝, 一个 dict 对象')
        画板.添加一行('本地资源字典', '设置/返回 _本地资源字典 的拷贝, 一个 dict 对象')

        画板.添加分隔行('-', None if callable(打印方法) else _黄字)
        if callable(打印方法):
            画板.添加一行('方法', '说明')
        else:
            画板.添加一行('方法', '说明').修饰行(_青字)
        画板.添加一行('添加图层:', '地图类对象.添加图层.__doc__ 查阅详情')
        画板.添加一行('添加热力层:', '地图类对象.添加热力层.__doc__ 查阅详情')
        画板.添加一行('添加基地:', '地图类对象.添加基地.__doc__ 查阅详情')
        画板.添加一行('添加热力点:', '地图类对象.添加热力点.__doc__ 查阅详情')
        画板.添加一行('添加标记点:', '地图类对象.添加标记点.__doc__ 查阅详情')
        画板.添加一行('添加参考经线:', '地图类对象.添加参考经线.__doc__ 查阅详情')
        画板.添加一行('添加参考纬线:', '地图类对象.添加参考纬线.__doc__ 查阅详情')
        画板.添加一行('添加参考经纬线:', '地图类对象.添加参考经纬线.__doc__ 查阅详情')
        画板.添加一行('添加网页标题:', '地图类对象.添加网页标题.__doc__ 查阅详情')
        画板.添加一行('支持测距:', '地图类对象.支持测距.__doc__ 查阅详情')
        画板.添加一行('禁止测距:', '地图类对象.禁止测距.__doc__ 查阅详情')
        画板.添加一行('支持鼠标绘图:', '地图类对象.支持鼠标绘图.__doc__ 查阅详情')
        画板.添加一行('禁止鼠标绘图:', '地图类对象.禁止鼠标绘图.__doc__ 查阅详情')
        画板.添加一行('支持点击标记:', '地图类对象.支持点击标记.__doc__ 查阅详情')
        画板.添加一行('禁止点击标记:', '地图类对象.禁止点击标记.__doc__ 查阅详情')
        画板.添加一行('支持坐标拾取:', '地图类对象.支持坐标拾取.__doc__ 查阅详情')
        画板.添加一行('禁止坐标拾取:', '地图类对象.禁止坐标拾取.__doc__ 查阅详情')
        画板.添加一行('网络资源字典调整', '地图类对象.网络资源字典调整.__doc__ 查阅详情')
        画板.添加一行('本地资源字典调整', '地图类对象.网络资源字典调整.__doc__ 查阅详情')
        画板.添加一行('优化网络资源', '地图类对象.优化网络资源.__doc__ 查阅详情')
        画板.添加一行('网络资源本地化', '地图类对象.网络资源本地化.__doc__ 查阅详情')
        画板.添加一行('生成Map对象:', '地图类对象.生成Map对象.__doc__ 查阅详情')
        画板.添加一行('展示地图:', '地图类对象.展示地图.__doc__ 查阅详情')
        画板.添加一行('保存html:', '地图类对象.保存html.__doc__ 查阅详情')

        画板.添加分隔行('=', None if callable(打印方法) else _黄字)

        画板.展示表格(打印方法=打印方法)
