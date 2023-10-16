#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import locale
import os
import platform
import sys
from datetime import datetime

from blessed import Terminal
from six.moves import cStringIO as StringIO
from typing import (TYPE_CHECKING, Any, Callable, Dict, Iterable, List,
                    Optional, Sequence, Union, cast)

from .gcu_smi import GetCardStatusWithGcuSmi

IS_WINDOWS = "windows" in platform.platform().lower()

# Types
Megabytes = int
Celcius = int
Percentage = float
Watts = float


EnflameGCUInfo = TypedDict('EnflameGCUInfo', {
    'index': int,
    'logicid' : int,
    'name': str,
    'uuid': str,
    'busid' : str,
    'temperature.gcu': Optional[Celcius],
    'utilization.gcu': Optional[Percentage],
    'utilization.mem': Optional[Percentage],
    'power.draw': Optional[Watts],
    'power.limit': Optional[Watts],
    'memory.used': Megabytes,
    'memory.total': Megabytes,
}, total=False) if TYPE_CHECKING else dict  # type: ignore

class GCU:
    """ 该类表示每个 GCU 的信息 """

    def __init__(self, entry: EnflameGCUInfo, term, light=False, *args, **kwargs):
        if not isinstance(entry, dict):
            raise TypeError("entry should be a dict, {} given".format(type(entry)))
        self.entry = entry
        self.show_busid = True
        self.show_power = True
        self.term = term
        self.light = light

        if 'show_busid' in kwargs.keys():
            self.show_busid = kwargs['show_busid']
        if 'show_power' in kwargs.keys():
            self.show_power = kwargs['show_power']

    def __repr__(self):
        return self.print_to(StringIO()).getvalue()

    def keys(self):
        return self.entry.keys()

    def __getitem__(self, key):
        return self.entry[key]

    @property
    def index(self) -> int:
        return self.entry["index"]

    @property
    def name(self) -> str:
        return self.entry["name"]

    @property
    def logicid(self) -> id:
        return self.entry["logicid"]

    @property
    def uuid(self) -> str:
        return self.entry["uuid"]

    @property
    def temperature(self) -> Optional[Celcius]:
        return self.entry["temperature.gcu"]

    @property
    def utilization(self) -> Optional[Percentage]:
        return self.entry["utilization.gcu"]

    @property
    def utilization_mem(self) -> Optional[Percentage]:
        return self.entry["utilization.mem"]

    @property
    def memory_used(self) -> Megabytes:
        return self.entry["memory.used"]

    @property
    def memory_total(self) -> Megabytes:
        return self.entry["memory.total"]

    @property
    def power_draw(self) -> Optional[Watts]:
        return self.entry["power.draw"]

    @property
    def power_limit(self) -> Optional[Watts]:
        return self.entry["power.limit"]

    @property
    def busid(self) -> str:
        return self.entry["busid"]

    def get_color(self):
        def _conditional(cond_fn, true_value, false_value, error_value=self.term.bold_black):
            try:
                return cond_fn() and true_value or false_value
            except Exception:
                return error_value

        colors = dict()
        colors["C0"] = self.term.normal
        colors["C1"] = self.term.cyan

        if self.light:
            colors["GCUtemp"] = self.term.bold_red
        else:
            colors["GCUtemp"] = _conditional(lambda: self.temperature < 60, self.term.red, self.term.bold_red)

        if self.light:
            colors["GCUDUsed"] = self.term.bold_blue
        else:
            colors["GCUDUsed"] = _conditional(lambda: self.utilization < 50, self.term.blue, self.term.bold_blue)

        if self.light:
            colors["GCUMemCur"] = self.term.bold_yellow
        else:
            colors["GCUMemCur"] = _conditional(lambda: self.utilization_mem < 50, self.term.yellow, self.term.bold_yellow)

        colors["GCUMemCap"] = self.term.bold_yellow

        colors["BUS-ID"] = self.term.green
        colors["GCUPwr"] = self.term.orange

        return colors

    def print_to(self, fp, *args, **kwargs):
        colors = self.get_color()

        # build one-line display information
        reps = ""
        reps += "%(C1)s[{entry[index]}] [{entry[name]}]%(C0)s" + " |"
        reps += "%(GCUtemp)s{entry[temperature.gcu]:>4}°C%(C0)s" + ", "
        reps += "%(GCUDUsed)s{entry[utilization.gcu]:>4} %%%(C0)s" + " |"
        reps += "%(C1)s%(GCUMemCur)s{entry[memory.used]:>5}%(C0)s" + " / " + "%(GCUMemCap)s{entry[memory.total]:>5} MB%(C0)s" + " |"
        if self.show_busid:
            reps += "%(BUS-ID)s{entry[busid]:>4}%(C0)s" + " "
        if self.show_power:
            reps += "%(GCUPwr)s{entry[power.draw]:>4}%(C0)s" + " "

        def _repr(v, none_value="??"):
            return none_value if v is None else v

        reps = reps % colors
        reps = reps.format(entry={k: _repr(v) for k, v in self.entry.items()})
        fp.write(reps)
        return fp

    def jsonify(self):
        o = self.entry.copy()

        # todo 目前还没有任何方法获取进程信息
        # if self.entry["processes"] is not None:
        #     o["processes"] = [{k: v for (k, v) in p.items() if k != "gpu_uuid"} for p in self.entry["processes"]]
        return o

class GCUCardCollection:
    """ 当前机器上所有 GCU 的信息 """

    def __init__(self, entry_list, eol_char=os.linesep, light=False, *args, **kwargs):
        self.hostname = platform.node()
        self.query_time = datetime.now()
        self.no_header = False
        self.no_title = False
        self.show_busid = True
        self.show_power = True
        self.force_color = False
        self.no_color = True

        if 'no_header' in kwargs.keys():
            self.no_header = kwargs['no_header']
        if 'no_title' in kwargs.keys():
            self.no_title = kwargs['no_title']
        if 'show_busid' in kwargs.keys():
            self.show_busid = kwargs['show_busid']
        if 'show_power' in kwargs.keys():
            self.show_power = kwargs['show_power']
        if 'force_color' in kwargs.keys():
            self.force_color = kwargs['force_color']
        if 'no_color' in kwargs.keys():
            self.no_color = kwargs['no_color']

        self.eol_char = eol_char
        self.term = self.get_term(self.force_color)
        # 是否以较亮的模式显示，如果指定了该参数，那么所有的字段都使用加粗显示
        self.light = light  

        self.title_colors = self.get_title_colors()

        gcu_list = []
        for entry in entry_list:
            gcu_list.append(GCU(entry, self.term, light=light, *args, **kwargs))
        self.gcu_list = gcu_list

    def get_term(self, force_color=False):
        if force_color:
            TERM = os.getenv("TERM") or "xterm-256color"
            t_color = Terminal(kind=TERM, force_styling=True)

            # workaround of issue #32 (watch doesn"t recognize sgr0 characters)
            t_color._normal = u"\x1b[0;10m"
        else:
            t_color = Terminal()  # auto, depending on isatty
        return t_color

    def print_header(self, fp, eol_char, term):
        if IS_WINDOWS:
            # no localization is available; just use a reasonable default same as str(time_str) but without ms
            time_str = self.query_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_format = locale.nl_langinfo(locale.D_T_FMT)
            time_str = self.query_time.strftime(time_format)

        header_template = "{t.bold_white}{hostname}{t.normal}  "
        header_template += "{time_str}"

        header_msg = header_template.format(
            hostname=self.hostname,
            time_str=time_str,
            t=term,
        )

        fp.write(header_msg.strip())
        fp.write(eol_char)

    def get_title_colors(self):
        colors = dict()
        colors["C0"] = self.term.normal
        colors["C1"] = self.term.cyan
        colors["GCUtemp"] = self.term.bold_red if self.light else self.term.red
        colors["GCUDUsed"] = self.term.bold_blue if self.light else self.term.blue
        colors["GCUMemCur"] = self.term.bold_yellow
        colors["GCUMemCap"] = self.term.bold_yellow if self.light else self.term.yellow
        colors["BUS-ID"] = self.term.bold_green if self.light else self.term.green
        colors["GCUPwr"] = self.term.bold_orange if self.light else self.term.orange
        return colors

    def print_title(self, fp, eol_char):
        # build one-line display information
        title = ""
        title += "%(C1)s[{entry[index]}] {entry[name]}%(C0)s" + "  |"
        title += "%(GCUtemp)s{entry[temperature.gcu]:>4}°C%(C0)s" + ", "
        title += "%(GCUDUsed)s{entry[utilization.gcu]:>4} %%%(C0)s" + " |"
        title += "%(C1)s%(GCUMemCur)s{entry[memory.used]:>5}%(C0)s" + " / " + "%(GCUMemCap)s{entry[memory.total]:>5} MB%(C0)s" + " |"
        if self.show_busid:
            title += "%(BUS-ID)s{entry[busid]:>4}%(C0)s"
        if self.show_power:
            title += "%(GCUPwr)s{entry[power.draw]:>4}%(C0)s"

        def _repr(v, none_value="??"):
            return none_value if v is None else v

        title = title % self.title_colors
        my_dict = {"index": "ID", "name": "名字", "temperature.gcu": "温度", "utilization.gcu": "占用率", "memory.used": "已用内存", 
                   "memory.total": "总内存", "busid": "总线ID", "power.draw": "功耗"}
        title = title.format(entry={k: _repr(v) for k, v in my_dict.items()})

        fp.write(title.strip())
        fp.write(eol_char)

    def print_formatted(self, fp=sys.stdout, *args, **kwargs):
        # ANSI color configuration
        if self.force_color and self.no_color:
            raise ValueError("--color and --no_color can't"
                             " be used at the same time")

        if self.force_color:
            TERM = os.getenv('TERM') or 'xterm-256color'
            t_color = Terminal(kind=TERM, force_styling=True)

            # workaround of issue #32 (watch doesn't recognize sgr0 characters)
            t_color._normal = '\x1b[0;10m'
        elif self.no_color:
            t_color = Terminal(force_styling=None)
        else:
            t_color = Terminal()   # auto, depending on isatty

        # header
        if not self.no_header:
            self.print_header(fp=fp, eol_char=self.eol_char, term=self.term)

        # title
        if not self.no_title:
            self.print_title(fp=fp, eol_char=self.eol_char)

        # body
        for gcu in self:
            gcu.print_to(fp)
            fp.write(self.eol_char)

        fp.flush()
        return fp

    def jsonify(self):
        return {
            "hostname": self.hostname,
            "query_time": self.query_time,
            "gcu": [gcu.jsonify() for gcu in self]
        }

    def print_json(self, fp=sys.stdout):
        def date_handler(obj):
            if hasattr(obj, "isoformat"):
                return obj.isoformat()
            else:
                raise TypeError(type(obj))

        o = self.jsonify()
        json.dump(o, fp, indent=4, separators=(",", ": "), default=date_handler)
        fp.write(os.linesep)
        fp.flush()

    def __len__(self):
        return len(self.gcu_list)

    def __iter__(self):
        return iter(self.gcu_list)

    def __getitem__(self, index):
        return self.gcu_list[index]

    def __repr__(self):
        s = "GCUCollection(host=%s, [\n" % self.hostname
        s += "\n".join("  " + str(g) for g in self.gcu_list)
        s += "\n])"
        return s


def new_query(*args, **kwargs):
    """Query the information of all the GCU Card on local machine"""

    flag_cache = True
    if 'cache' in kwargs.keys():
        flag_cache = kwargs['cache']

    version, card_entry_list = GetCardStatusWithGcuSmi(flag_cache).new_query()

    return GCUCardCollection(card_entry_list, version=version, *args, **kwargs)
