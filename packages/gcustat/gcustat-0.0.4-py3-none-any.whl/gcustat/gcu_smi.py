#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

sub_space_p = re.compile(r"[ ]{2,}")  # 用于将多个连续空格替换成单个空格
global_gcu_card_info = None


class GetEntryCardListV1:
    """

               -----------------------------------------------------------------------
               ----------------- Enflame System Management Interface -----------------
               -------- Enflame Tech, All Rights Reserved. 2023 Copyright (C) --------
               -----------------------------------------------------------------------
                                                                                      
               *Sat Oct  7 15:54:28 2023-------------------------------------------------*
               *EFSMI    V1.20.0          Driver Ver: 2.4.20230829                       *
               *-------------------------------------------------------------------------*
               *-------------------------------------------------------------------------*
               * DEV    NAME                | FW VER          | BUS-ID     ECC           *
               * TEMP   DPM   Pwr(Usage/Cap)| Mem         vGCU| DEV-Util   UUID          *
               *-------------------------------------------------------------------------*
    line 1 ==> * 0      T20                 | 10.19.3         | 00:3d:0.0  Enable        *
    line 2 ==> * 30C    Sleep   48.0W  300W | 32G      Disable|   0.0%     W28001210504  *
               *-------------------------------------------------------------------------*
               *-------------------------------------------------------------------------*
    line 1 ==> * 1      T20                 | 10.19.3         | 00:3e:0.0  Enable        *
    line 2 ==> * 30C    Sleep   48.0W  300W | 32G      Disable|   0.0%     W28001010604  *
               *-------------------------------------------------------------------------*

    """

    # card id/DEV, chip name/NAME, FW VER, BUS-ID, ECC
    pattern = r""
    pattern += r"(\d{1,2})" + r" "  # card id
    pattern += r"([a-zA-Z]\d{1,5})" + r" \| "  # chip name, 比如 T20/I20 等
    pattern += r"([\d.]{1,10})" + r" \| "  #10.19.3
    pattern += r"([a-zA-Z\d:\.]{8,20})" + r" "  # 00:3d:0.0
    pattern += r"([a-zA-Z]{1,10})"  # Enable
    line_1_p = re.compile(pattern)

    # TEMP, DPM, Pwr_Usage, Pwr_Cap, Mem, vGCU, DEV-Util, UUID
    pattern = r""
    pattern += r"(\d{1,2})C" + r" "  # temperature
    pattern += r"([A-Za-z0-9]{1,8})" + r" "  # Dpm
    pattern += r"([\d.]{1,5})W" + r" "  # power usage
    pattern += r"([\d.]{1,5})W" + r" \| "  # power cap
    pattern += r"(\d{1,6})G" + r" "  # total memory
    pattern += r"([a-zA-Z]{1,10}) ?\|" + r" "  # Disable
    pattern += r"([\d.]{1,10})%" + r" " #DEV-Util
    pattern += r"([a-zA-Z0-9]\d{1,20})" + r" " #UUID
    line_2_p = re.compile(pattern)

    @staticmethod
    def get_dmon_info():
        # GCU, Logic, Pwr, DTemp, DUsed, Dpm, M1Temp, M2Temp, MUsed, Dclk, Mclk
        pattern = r""
        pattern += r"(\d{1,2})" + r" "  # GCU Idx
        pattern += r"(\d{1,2})" + r" "  # Logic Id
        pattern += r"([\d.]{1,5})" + r" "  # Pwr
        pattern += r"([\d.]{1,5})" + r" "  # DTemp
        pattern += r"([\d.]{1,5})" + r" "  # DUsed
        pattern += r"([A-Za-z0-9]{1,8})" + r" "  # Dpm
        pattern += r"([\d.]{1,5})" + r" "  # M1Temp
        pattern += r"([\d.]{1,5})" + r" "  # M2Temp
        pattern += r"([\d.]{1,5})" + r" "  # MUsed
        pattern += r"([A-Za-z0-9]{1,5})" + r" "  # Dclk
        pattern += r"([A-Za-z0-9]{1,5})"   # Mclk
        line_d_p = re.compile(pattern)

        dmon_result = os.popen(f"efsmi --dmon -c 1").read()
        match_list = []
        for line in dmon_result.split("\n"):
            line = sub_space_p.sub(" ", line).strip()
            if line_d_p.search(line):
                match_list.append(line_d_p.search(line).groups())
    
        entry_list = []
        for dev_id, logic_id, gcu_pwr, dtemp, dused, _, _, _, mused, _, _ in match_list:
            entry = dict()
            entry["index"] = dev_id
            entry["logicid"] = logic_id
            entry["power.draw"] = float(gcu_pwr)
            entry["temperature.gcu"] = float(dtemp)
            entry["utilization.gcu"] = float(dused)
            entry["utilization.mem"] = float(mused)
            entry_list.append(entry)
    
        return entry_list

    def get_card_entry(self, gcu_card_info):
        line_1_list, line_2_list = [], []
        for line in gcu_card_info.split("\n"):
            line = sub_space_p.sub(" ", line)
            m1 = self.line_1_p.search(line)
            m2 = self.line_2_p.search(line)

            if m1 is not None and m2 is not None:
                raise RuntimeError(f"解析 efsmi 结果失败，同一行匹配上两个正则，"
                                   f"line: {line}")

            if m1:
                line_1_list.append(m1.groups())
            if m2:
                line_2_list.append(m2.groups())

        if len(line_1_list) != len(line_2_list):
            raise RuntimeError(f"解析 efsmi 结果失败，两个正则匹配上的行数不同\n"
                               f"{gcu_card_info}")

        dmon_list= GetEntryCardListV1.get_dmon_info()
        if len(dmon_list) != len(line_1_list):
            raise RuntimeError(f"解析 efsmi --dmon 结果失败，两次正则匹配上的行数不同\n"
                               f"{dmon_list}")

        card_entry_list = []
        card_entry = dict()

        for line1, line2 in zip(line_1_list, line_2_list):
            dev_id, chip_name, fw_ver, bus_id, ecc = line1
            temp, dpm, pwr_usage, pwr_cap, mem, vgcu, dev_util, uuid = line2

            card_entry = dict()
            card_entry["name"] = chip_name
            card_entry["busid"] = bus_id
            card_entry["memory.total"] = int(mem) * 1024
            card_entry["power.limit"] = pwr_cap
            card_entry["uuid"] = uuid

            MUsed_percent = dmon_list[int(dev_id)]["utilization.mem"]
            card_entry["memory.used"] = round(card_entry["memory.total"] * MUsed_percent / 100)

            card_entry.update(dmon_list[int(dev_id)])
            card_entry_list.append(card_entry)

        if len(card_entry_list) == 0:
            raise RuntimeError(f"无法获取到GCU信息\n")

        return card_entry_list

class GetCardStatusWithGcuSmi:
    def __init__(self, no_cache):
        self.no_cache = no_cache

        # 下面这个正则中：第一个版本是gcu-smi的版本，第二个版本是驱动版本
        self.version_p = re.compile(r"\*EFSMI V([0-9a-z.]{2,20}?) Driver Ver: [0-9a-z.]{2,20}? \*")

        self.version2func = {
            "1.20.0": GetEntryCardListV1,

            # 默认
            "default": GetEntryCardListV1,
        }

    def new_query(self):
        global global_gcu_card_info
        if (global_gcu_card_info is None) or self.no_cache:
            global_gcu_card_info = os.popen("efsmi --").read()
        version = self.get_version(global_gcu_card_info)

        if version in self.version2func:
            my_class = self.version2func[version]()
        else:
            my_class = self.version2func["default"]()

        entry_list = my_class.get_card_entry(global_gcu_card_info)
        return f"efsmi version : {version}", entry_list

    def get_version(self, gcu_card_info):
        result_list = []
        for line in gcu_card_info.split("\n"):
            line = sub_space_p.sub(" ", line)
            my_match = self.version_p.search(line)
            if my_match:
                result_list.append(my_match)

        if len(result_list) == 1:
            return result_list[0].groups()[0]
        return None
