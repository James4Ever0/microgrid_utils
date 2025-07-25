from log_utils import logger_print
from type_def import *
import os
from constants import UNKNOWN

"""static & dynamic topology type checking"""


def logFailedRule(passed: bool, banner: str):
    if not passed:
        logger_print(f"Rule {banner} failed.")
    return passed


def portNameTransformer(port_name):
    result = port_name.split("_")
    result_length = len(result)
    if result_length == 3:
        transformed_port_name = f"{result[0]}_{result[2]}"
    else:
        raise Exception(
            f'Failed to parse port name "{port_name}" (mismatched splited size: {result_length})'
        )
    return transformed_port_name


deviceTypes = [
    "柴油",
    "电负荷",
    "光伏发电",
    "风力发电",
    "柴油发电",
    "锂电池",
    "变压器",
    "双向变压器",
    "变流器",
    "双向变流器",
    "传输线",
    "市政自来水",
    "天然气",
    "电网",
    "氢气",
    "冷负荷",
    "热负荷",
    "蒸汽负荷",
    "氢负荷",
    "燃气发电机",
    "蒸汽轮机",
    "氢燃料电池",
    "平板太阳能",
    "槽式太阳能",
    "余热热水锅炉",
    "余热蒸汽锅炉",
    "浅层地热井",
    "中深层地热井",
    "地表水源",
    "水冷冷却塔",
    "余热热源",
    "浅层双源四工况热泵",
    "中深层双源四工况热泵",
    "浅层双源三工况热泵",
    "中深层双源三工况热泵",
    "水冷螺杆机",
    "双工况水冷螺杆机组",
    "吸收式燃气热泵",
    "空气源热泵",
    "蒸汽溴化锂",
    "热水溴化锂",
    "电热水锅炉",
    "电蒸汽锅炉",
    "天然气热水锅炉",
    "天然气蒸汽锅炉",
    "电解槽",
    "水蓄能",
    "蓄冰槽",
    "储氢罐",
    "输水管道",
    "蒸汽管道",
    "复合输水管道",
    "水水换热器",
    "复合水水换热器",
    "气水换热器",
    "单向线",
    "互斥元件",
]
energyTypes = [
    "蒸汽",
    "冷乙二醇",
    "热乙二醇",
    "电",
    "热水",
    "天然气",
    "烟气",
    "冰乙二醇",
    "自来水",
    "冷水",
    "柴油",
    "氢气",
    "导热油",
]

deviceTypeToTypeInfo = {
    "柴油": {
        "requiredPortFrontendNameToPortPossibleStates": {"燃料接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["柴油"]},
    },
    "电负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "光伏发电": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "风力发电": {
        "requiredPortFrontendNameToPortPossibleStates": {"电接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "柴油发电": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["柴油"], "电接口": ["电"]},
    },
    "锂电池": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "变压器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input"],
            "电输出": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "双向变压器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "变流器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input"],
            "电输出": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "双向变流器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "储能端": ["idle", "input", "output"],
            "线路端": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"储能端": ["电"], "线路端": ["电"]},
    },
    "传输线": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电输入": ["idle", "input", "output"],
            "电输出": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电输入": ["电"], "电输出": ["电"]},
    },
    "市政自来水": {
        "requiredPortFrontendNameToPortPossibleStates": {"水接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"水接口": ["自来水"]},
    },
    "天然气": {
        "requiredPortFrontendNameToPortPossibleStates": {"燃料接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"]},
    },
    "电网": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"]},
    },
    "氢气": {
        "requiredPortFrontendNameToPortPossibleStates": {"氢气接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"氢气接口": ["氢气"]},
    },
    "冷负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"冷源接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"冷源接口": ["冷水"]},
    },
    "热负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"热源接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"热源接口": ["热水"]},
    },
    "蒸汽负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"蒸汽接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"蒸汽接口": ["蒸汽"]},
    },
    "氢负荷": {
        "requiredPortFrontendNameToPortPossibleStates": {"氢气接口": ["idle", "input"]},
        "requiredPortFrontendNameToEnergyTypes": {"氢气接口": ["氢气"]},
    },
    "燃气发电机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "高温烟气余热接口": ["idle", "output"],
            "缸套水余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "燃料接口": ["天然气"],
            "电接口": ["电"],
            "高温烟气余热接口": ["烟气"],
            "缸套水余热接口": ["热水"],
        },
    },
    "蒸汽轮机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蒸汽接口": ["idle", "input"],
            "电接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"蒸汽接口": ["蒸汽"], "电接口": ["电"]},
    },
    "氢燃料电池": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "氢气接口": ["idle", "input"],
            "电接口": ["idle", "output"],
            "设备余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "氢气接口": ["氢气"],
            "电接口": ["电"],
            "设备余热接口": ["热水"],
        },
    },
    "平板太阳能": {
        "requiredPortFrontendNameToPortPossibleStates": {"热接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热接口": ["热水"]},
    },
    "槽式太阳能": {
        "requiredPortFrontendNameToPortPossibleStates": {"热接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热接口": ["导热油"]},
    },
    "余热热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "烟气接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"烟气接口": ["烟气"], "制热接口": ["热水"]},
    },
    "余热蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "烟气接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"烟气接口": ["烟气"], "蒸汽接口": ["蒸汽"]},
    },
    "浅层地热井": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        },
    },
    "中深层地热井": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "热源接口": ["热水"]},
    },
    "地表水源": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
            "热源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
        },
    },
    "水冷冷却塔": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "水接口": ["idle", "input"],
            "冷源接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "水接口": ["自来水"],
            "冷源接口": ["冷水"],
        },
    },
    "余热热源": {
        "requiredPortFrontendNameToPortPossibleStates": {"热源接口": ["idle", "output"]},
        "requiredPortFrontendNameToEnergyTypes": {"热源接口": ["热水"]},
    },
    "浅层双源四工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "中深层双源四工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "浅层双源三工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        },
    },
    "中深层双源三工况热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "热源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "热源接口": ["热水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
            "制热接口": ["热乙二醇"],
        },
    },
    "水冷螺杆机": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
        },
    },
    "双工况水冷螺杆机组": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "制冰接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷乙二醇"],
            "制冰接口": ["冰乙二醇"],
        },
    },
    "吸收式燃气热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "制热接口": ["热水"]},
    },
    "空气源热泵": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
            "蓄冷接口": ["idle", "output"],
            "制热接口": ["idle", "output"],
            "蓄热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "制冷接口": ["冷水"],
            "蓄冷接口": ["冷水"],
            "制热接口": ["热水"],
            "蓄热接口": ["热水"],
        },
    },
    "蒸汽溴化锂": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蒸汽接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "蒸汽接口": ["蒸汽"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        },
    },
    "热水溴化锂": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "热水接口": ["idle", "input"],
            "冷源接口": ["idle", "input"],
            "制冷接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "热水接口": ["热水"],
            "冷源接口": ["冷水"],
            "制冷接口": ["冷水"],
        },
    },
    "电热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "制热接口": ["热水"]},
    },
    "电蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"电接口": ["电"], "蒸汽接口": ["蒸汽"]},
    },
    "天然气热水锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "制热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "制热接口": ["热水"]},
    },
    "天然气蒸汽锅炉": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "燃料接口": ["idle", "input"],
            "蒸汽接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"燃料接口": ["天然气"], "蒸汽接口": ["蒸汽"]},
    },
    "电解槽": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "电接口": ["idle", "input"],
            "制氢接口": ["idle", "output"],
            "设备余热接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "电接口": ["电"],
            "制氢接口": ["氢气"],
            "设备余热接口": ["热水"],
        },
    },
    "水蓄能": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蓄热接口": ["idle", "input", "output"],
            "蓄冷接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"蓄热接口": ["热水"], "蓄冷接口": ["冷水"]},
    },
    "蓄冰槽": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "蓄冰接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"蓄冰接口": ["冰乙二醇"]},
    },
    "储氢罐": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "储氢接口": ["idle", "input", "output"]
        },
        "requiredPortFrontendNameToEnergyTypes": {"储氢接口": ["氢气"]},
    },
    "输水管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "输入接口": ["冷水", "热水"],
            "输出接口": ["冷水", "热水"],
            "电接口": ["电"],
        },
    },
    "蒸汽管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"输入接口": ["蒸汽"], "输出接口": ["蒸汽"]},
    },
    "复合输水管道": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
            "电接口": ["idle", "input"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "冷输入接口": ["冷水"],
            "热输入接口": ["热水"],
            "冷输出接口": ["冷水"],
            "热输出接口": ["热水"],
            "电接口": ["电"],
        },
    },
    "水水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input", "output"],
            "输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "输入接口": ["冰乙二醇", "热乙二醇", "冷乙二醇", "热水", "自来水", "冷水", "导热油"],
            "输出接口": ["冰乙二醇", "热乙二醇", "冷乙二醇", "热水", "自来水", "冷水", "导热油"],
        },
    },
    "复合水水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "冷输入接口": ["idle", "input", "output"],
            "热输入接口": ["idle", "input", "output"],
            "冷输出接口": ["idle", "input", "output"],
            "热输出接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "冷输入接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输入接口": ["热乙二醇", "热水", "导热油"],
            "冷输出接口": ["冷乙二醇", "冰乙二醇", "冷水"],
            "热输出接口": ["热乙二醇", "热水", "导热油"],
        },
    },
    "气水换热器": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input"],
            "输出接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {"输入接口": ["蒸汽"], "输出接口": ["热水"]},
    },
    "单向线": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "输入接口": ["idle", "input"],
            "输出接口": ["idle", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "输入接口": [
                "柴油",
                "天然气",
                "氢气",
                "电",
                "热水",
                "自来水",
                "冷水",
                "蒸汽",
                "烟气",
                "导热油",
                "冰乙二醇",
                "热乙二醇",
                "冷乙二醇",
            ],
            "输出接口": [
                "柴油",
                "天然气",
                "氢气",
                "电",
                "热水",
                "自来水",
                "冷水",
                "蒸汽",
                "烟气",
                "导热油",
                "冰乙二醇",
                "热乙二醇",
                "冷乙二醇",
            ],
        },
    },
    "互斥元件": {
        "requiredPortFrontendNameToPortPossibleStates": {
            "互斥接口A": ["idle", "input", "output"],
            "互斥接口B": ["idle", "input", "output"],
            "外部接口": ["idle", "input", "output"],
        },
        "requiredPortFrontendNameToEnergyTypes": {
            "互斥接口A": [
                "柴油",
                "天然气",
                "氢气",
                "电",
                "热水",
                "自来水",
                "冷水",
                "蒸汽",
                "烟气",
                "导热油",
                "冰乙二醇",
                "热乙二醇",
                "冷乙二醇",
            ],
            "互斥接口B": [
                "柴油",
                "天然气",
                "氢气",
                "电",
                "热水",
                "自来水",
                "冷水",
                "蒸汽",
                "烟气",
                "导热油",
                "冰乙二醇",
                "热乙二醇",
                "冷乙二醇",
            ],
            "外部接口": [
                "柴油",
                "天然气",
                "氢气",
                "电",
                "热水",
                "自来水",
                "冷水",
                "蒸汽",
                "烟气",
                "导热油",
                "冰乙二醇",
                "热乙二醇",
                "冷乙二醇",
            ],
        },
    },
}

port_verifier_lookup_table = {
    "电负荷": {
        "电接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 电接口, 电负荷)"
        ),
    },
    "光伏发电": {
        "电接口": lambda conds: logFailedRule(
            "idle" in conds or "any" in conds, "#0 (port, 电接口, 光伏发电)"
        ),
    },
    "风力发电": {
        "电接口": lambda conds: logFailedRule(
            "idle" in conds or "any" in conds, "#0 (port, 电接口, 风力发电)"
        ),
    },
    "锂电池": {
        "电接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 电接口, 锂电池)"
        ),
    },
    "冷负荷": {
        "冷源接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 冷源接口, 冷负荷)"
        ),
    },
    "热负荷": {
        "热源接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 热源接口, 热负荷)"
        ),
    },
    "蒸汽负荷": {
        "蒸汽接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 蒸汽接口, 蒸汽负荷)"
        ),
    },
    "氢负荷": {
        "氢气接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 氢气接口, 氢负荷)"
        ),
    },
    "水蓄能": {
        "蓄热接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 蓄热接口, 水蓄能)"
        )
        or logFailedRule(
            set(conds).difference({"idle", "any"}) == set(), "#1 (port, 蓄热接口, 水蓄能)"
        ),
        "蓄冷接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 蓄冷接口, 水蓄能)"
        )
        or logFailedRule(
            set(conds).difference({"idle", "any"}) == set(), "#1 (port, 蓄冷接口, 水蓄能)"
        ),
    },
    "蓄冰槽": {
        "蓄冰接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 蓄冰接口, 蓄冰槽)"
        )
        or logFailedRule(
            set(conds).difference({"idle", "any"}) == set(), "#1 (port, 蓄冰接口, 蓄冰槽)"
        ),
    },
    "储氢罐": {
        "储氢接口": lambda conds: logFailedRule(
            "input" in conds or "any" in conds, "#0 (port, 储氢接口, 储氢罐)"
        )
        or logFailedRule(
            set(conds).difference({"idle", "any"}) == set(), "#1 (port, 储氢接口, 储氢罐)"
        ),
    },
}

conjugate_port_verifier_constructor_lookup_table = {
    "柴油": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("燃料接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (燃料接口), 柴油)",
            )
        }.items()
    },
    "电负荷": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (电接口), 电负荷)",
            )
        }.items()
    },
    "光伏发电": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (电接口), 光伏发电)",
            )
        }.items()
    },
    "风力发电": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (电接口), 风力发电)",
            )
        }.items()
    },
    "柴油发电": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("燃料接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (燃料接口, 电接口), 柴油发电)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#1 (conjugate, (燃料接口, 电接口), 柴油发电)",
            )
        }.items()
    },
    "锂电池": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (电接口), 锂电池)",
            )
        }.items()
    },
    "变压器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (电输出, 电输入), 变压器)",
            ),
            ("电输入", "电输出"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电输入, 电输出), 变压器)",
            ),
        }.items()
    },
    "双向变压器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电输出, 电输入), 双向变压器)",
            )
            and logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#1 (conjugate, (电输出, 电输入), 双向变压器)",
            )
            and logFailedRule(
                sum([int(cond1 in ["input"]), int(cond0 in ["input"])]) <= 1,
                "#2 (conjugate, (电输出, 电输入), 双向变压器)",
            ),
            ("电输入", "电输出"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电输入, 电输出), 双向变压器)",
            ),
        }.items()
    },
    "变流器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (电输出, 电输入), 变流器)",
            ),
            ("电输入", "电输出"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电输入, 电输出), 变流器)",
            ),
        }.items()
    },
    "双向变流器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("储能端", "线路端"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (储能端, 线路端), 双向变流器)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#1 (conjugate, (储能端, 线路端), 双向变流器)",
            )
            and logFailedRule(
                sum([int(cond0 in ["input"]), int(cond1 in ["input"])]) <= 1,
                "#2 (conjugate, (储能端, 线路端), 双向变流器)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#3 (conjugate, (储能端, 线路端), 双向变流器)",
            )
        }.items()
    },
    "传输线": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电输出", "电输入"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电输出, 电输入), 传输线)",
            )
            and logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#1 (conjugate, (电输出, 电输入), 传输线)",
            )
            and logFailedRule(
                sum([int(cond1 in ["input"]), int(cond0 in ["input"])]) <= 1,
                "#2 (conjugate, (电输出, 电输入), 传输线)",
            ),
            ("电输入", "电输出"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电输入, 电输出), 传输线)",
            ),
        }.items()
    },
    "市政自来水": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("水接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (水接口), 市政自来水)",
            )
        }.items()
    },
    "天然气": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("燃料接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (燃料接口), 天然气)",
            )
        }.items()
    },
    "电网": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (电接口), 电网)",
            )
        }.items()
    },
    "氢气": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("氢气接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (氢气接口), 氢气)",
            )
        }.items()
    },
    "冷负荷": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("冷源接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (冷源接口), 冷负荷)",
            )
        }.items()
    },
    "热负荷": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热源接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (热源接口), 热负荷)",
            )
        }.items()
    },
    "蒸汽负荷": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (蒸汽接口), 蒸汽负荷)",
            )
        }.items()
    },
    "氢负荷": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("氢气接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (氢气接口), 氢负荷)",
            )
        }.items()
    },
    "燃气发电机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "高温烟气余热接口",
                "缸套水余热接口",
                "燃料接口",
                "电接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                all(
                    [
                        cond2 in ["any", "input"],
                        cond0 in ["any", "output"],
                        cond1 in ["any", "output"],
                    ]
                )
                if cond3 in ["output"]
                else True,
                "#0 (conjugate, (高温烟气余热接口, 缸套水余热接口, 燃料接口, 电接口), 燃气发电机)",
            ),
            (
                "缸套水余热接口",
                "高温烟气余热接口",
                "电接口",
                "燃料接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                all(
                    [
                        cond3 in ["any", "input"],
                        cond2 in ["any", "output"],
                        cond0 in ["any", "output"],
                    ]
                )
                if cond1 in ["output"]
                else True,
                "#0 (conjugate, (缸套水余热接口, 高温烟气余热接口, 电接口, 燃料接口), 燃气发电机)",
            ),
            (
                "高温烟气余热接口",
                "缸套水余热接口",
                "电接口",
                "燃料接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                all(
                    [
                        cond3 in ["any", "input"],
                        cond2 in ["any", "output"],
                        cond0 in ["any", "output"],
                    ]
                )
                if cond1 in ["output"]
                else True,
                "#0 (conjugate, (高温烟气余热接口, 缸套水余热接口, 电接口, 燃料接口), 燃气发电机)",
            ),
            (
                "燃料接口",
                "电接口",
                "高温烟气余热接口",
                "缸套水余热接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (燃料接口, 电接口, 高温烟气余热接口, 缸套水余热接口), 燃气发电机)",
            ),
        }.items()
    },
    "蒸汽轮机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (蒸汽接口, 电接口), 蒸汽轮机)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#1 (conjugate, (蒸汽接口, 电接口), 蒸汽轮机)",
            )
        }.items()
    },
    "氢燃料电池": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "氢气接口",
                "电接口",
                "设备余热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond2 in ["any", "output"]])
                if cond1 in ["output"]
                else True,
                "#0 (conjugate, (氢气接口, 电接口, 设备余热接口), 氢燃料电池)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "output"]])
                if cond2 in ["output"]
                else True,
                "#1 (conjugate, (氢气接口, 电接口, 设备余热接口), 氢燃料电池)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#2 (conjugate, (氢气接口, 电接口, 设备余热接口), 氢燃料电池)",
            )
        }.items()
    },
    "平板太阳能": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (热接口), 平板太阳能)",
            )
        }.items()
    },
    "槽式太阳能": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (热接口), 槽式太阳能)",
            )
        }.items()
    },
    "余热热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("制热接口", "烟气接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (制热接口, 烟气接口), 余热热水锅炉)",
            ),
            ("烟气接口", "制热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (烟气接口, 制热接口), 余热热水锅炉)",
            ),
        }.items()
    },
    "余热蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "烟气接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (蒸汽接口, 烟气接口), 余热蒸汽锅炉)",
            ),
            ("烟气接口", "蒸汽接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (烟气接口, 蒸汽接口), 余热蒸汽锅炉)",
            ),
        }.items()
    },
    "浅层地热井": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热源接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (热源接口, 电接口), 浅层地热井)",
            ),
            ("冷源接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (冷源接口, 电接口), 浅层地热井)",
            ),
            ("冷源接口", "热源接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond0 in ["output"]), int(cond1 in ["output"])]) <= 1,
                "#0 (conjugate, (冷源接口, 热源接口), 浅层地热井)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口), 浅层地热井)",
            ),
        }.items()
    },
    "中深层地热井": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热源接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (热源接口, 电接口), 中深层地热井)",
            ),
            ("电接口", "热源接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电接口, 热源接口), 中深层地热井)",
            ),
        }.items()
    },
    "地表水源": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("冷源接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (冷源接口, 电接口), 地表水源)",
            ),
            ("热源接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (热源接口, 电接口), 地表水源)",
            ),
            ("冷源接口", "热源接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond0 in ["output"]), int(cond1 in ["output"])]) <= 1,
                "#0 (conjugate, (冷源接口, 热源接口), 地表水源)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口), 地表水源)",
            ),
        }.items()
    },
    "水冷冷却塔": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "水接口",
                "冷源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond0 in ["any", "input"]])
                if cond1 in ["output"]
                else True,
                "#0 (conjugate, (水接口, 冷源接口, 电接口), 水冷冷却塔)",
            ),
            (
                "电接口",
                "水接口",
                "冷源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (电接口, 水接口, 冷源接口), 水冷冷却塔)",
            ),
        }.items()
    },
    "余热热源": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("热源接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (热源接口), 余热热源)",
            )
        }.items()
    },
    "浅层双源四工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 浅层双源四工况热泵)",
            ),
            (
                "蓄冷接口",
                "电接口",
                "冷源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond2 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (蓄冷接口, 电接口, 冷源接口), 浅层双源四工况热泵)",
            ),
            (
                "制热接口",
                "热源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (制热接口, 热源接口, 电接口), 浅层双源四工况热泵)",
            ),
            (
                "电接口",
                "热源接口",
                "蓄热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (电接口, 热源接口, 蓄热接口), 浅层双源四工况热泵)",
            ),
            (
                "制热接口",
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                sum(
                    [
                        int(cond3 in ["output"]),
                        int(cond0 in ["output"]),
                        int(cond1 in ["output"]),
                        int(cond2 in ["output"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (制热接口, 蓄冷接口, 蓄热接口, 制冷接口), 浅层双源四工况热泵)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
                "制冷接口",
                "蓄冷接口",
                "制热接口",
                "蓄热接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, cond5, cond6, etype0, etype1, etype2, etype3, etype4, etype5, etype6: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [
                        etype0 != "any",
                        etype1 != "any",
                        etype2 != "any",
                        etype3 != "any",
                        etype5 != "any",
                    ]
                ),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口, 制冷接口, 蓄冷接口, 制热接口, 蓄热接口), 浅层双源四工况热泵)",
            ),
        }.items()
    },
    "中深层双源四工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 中深层双源四工况热泵)",
            ),
            (
                "蓄冷接口",
                "电接口",
                "冷源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond2 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (蓄冷接口, 电接口, 冷源接口), 中深层双源四工况热泵)",
            ),
            (
                "制热接口",
                "热源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (制热接口, 热源接口, 电接口), 中深层双源四工况热泵)",
            ),
            (
                "电接口",
                "热源接口",
                "蓄热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (电接口, 热源接口, 蓄热接口), 中深层双源四工况热泵)",
            ),
            (
                "制热接口",
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                sum(
                    [
                        int(cond3 in ["output"]),
                        int(cond0 in ["output"]),
                        int(cond1 in ["output"]),
                        int(cond2 in ["output"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (制热接口, 蓄冷接口, 蓄热接口, 制冷接口), 中深层双源四工况热泵)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
                "制冷接口",
                "蓄冷接口",
                "制热接口",
                "蓄热接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, cond5, cond6, etype0, etype1, etype2, etype3, etype4, etype5, etype6: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [etype0 != "any", etype2 != "any", etype3 != "any", etype5 != "any"]
                ),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口, 制冷接口, 蓄冷接口, 制热接口, 蓄热接口), 中深层双源四工况热泵)",
            ),
            ("冷源接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(it != "any") for it in [etype0, etype1]]) in [0, 2],
                "#0 (conjugate, (冷源接口, 制冷接口), 中深层双源四工况热泵)",
            ),
        }.items()
    },
    "浅层双源三工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 浅层双源三工况热泵)",
            ),
            (
                "冷源接口",
                "电接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冰接口), 浅层双源三工况热泵)",
            ),
            (
                "制热接口",
                "热源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (制热接口, 热源接口, 电接口), 浅层双源三工况热泵)",
            ),
            (
                "制热接口",
                "制冷接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                sum(
                    [
                        int(cond1 in ["output"]),
                        int(cond0 in ["output"]),
                        int(cond2 in ["output"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (制热接口, 制冷接口, 制冰接口), 浅层双源三工况热泵)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
                "制冷接口",
                "制冰接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, cond5, etype0, etype1, etype2, etype3, etype4, etype5: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [
                        etype0 != "any",
                        etype1 != "any",
                        etype2 != "any",
                        etype3 != "any",
                        etype4 != "any",
                        etype5 != "any",
                    ]
                ),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口, 制冷接口, 制冰接口, 制热接口), 浅层双源三工况热泵)",
            ),
        }.items()
    },
    "中深层双源三工况热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 中深层双源三工况热泵)",
            ),
            (
                "冷源接口",
                "电接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冰接口), 中深层双源三工况热泵)",
            ),
            (
                "制热接口",
                "热源接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (制热接口, 热源接口, 电接口), 中深层双源三工况热泵)",
            ),
            (
                "制热接口",
                "制冷接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                sum(
                    [
                        int(cond1 in ["output"]),
                        int(cond0 in ["output"]),
                        int(cond2 in ["output"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (制热接口, 制冷接口, 制冰接口), 中深层双源三工况热泵)",
            ),
            (
                "电接口",
                "冷源接口",
                "热源接口",
                "制冷接口",
                "制冰接口",
                "制热接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, cond5, etype0, etype1, etype2, etype3, etype4, etype5: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [
                        etype0 != "any",
                        etype1 != "any",
                        etype2 != "any",
                        etype3 != "any",
                        etype4 != "any",
                        etype5 != "any",
                    ]
                ),
                "#0 (conjugate, (电接口, 冷源接口, 热源接口, 制冷接口, 制冰接口, 制热接口), 中深层双源三工况热泵)",
            ),
        }.items()
    },
    "水冷螺杆机": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 水冷螺杆机)",
            ),
            (
                "蓄冷接口",
                "电接口",
                "冷源接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond2 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (蓄冷接口, 电接口, 冷源接口), 水冷螺杆机)",
            ),
            ("蓄冷接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond1 in ["output"]), int(cond0 in ["output"])]) <= 1,
                "#0 (conjugate, (蓄冷接口, 制冷接口), 水冷螺杆机)",
            ),
            (
                "电接口",
                "冷源接口",
                "制冷接口",
                "蓄冷接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (电接口, 冷源接口, 制冷接口, 蓄冷接口), 水冷螺杆机)",
            ),
        }.items()
    },
    "双工况水冷螺杆机组": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "冷源接口",
                "电接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冷接口), 双工况水冷螺杆机组)",
            ),
            (
                "冷源接口",
                "电接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (冷源接口, 电接口, 制冰接口), 双工况水冷螺杆机组)",
            ),
            ("制冷接口", "制冰接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond0 in ["output"]), int(cond1 in ["output"])]) <= 1,
                "#0 (conjugate, (制冷接口, 制冰接口), 双工况水冷螺杆机组)",
            ),
            (
                "电接口",
                "冷源接口",
                "制冷接口",
                "制冰接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [etype0 != "any", etype1 != "any", etype2 != "any", etype3 != "any"]
                ),
                "#0 (conjugate, (电接口, 冷源接口, 制冷接口, 制冰接口), 双工况水冷螺杆机组)",
            ),
        }.items()
    },
    "吸收式燃气热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("制热接口", "燃料接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (制热接口, 燃料接口), 吸收式燃气热泵)",
            ),
            ("燃料接口", "制热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (燃料接口, 制热接口), 吸收式燃气热泵)",
            ),
        }.items()
    },
    "空气源热泵": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "制冷接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电接口, 制冷接口), 空气源热泵)",
            ),
            ("蓄冷接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (蓄冷接口, 电接口), 空气源热泵)",
            ),
            ("制热接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (制热接口, 电接口), 空气源热泵)",
            ),
            ("电接口", "蓄热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电接口, 蓄热接口), 空气源热泵)",
            ),
            (
                "制热接口",
                "蓄冷接口",
                "蓄热接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                sum(
                    [
                        int(cond3 in ["output"]),
                        int(cond0 in ["output"]),
                        int(cond1 in ["output"]),
                        int(cond2 in ["output"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (制热接口, 蓄冷接口, 蓄热接口, 制冷接口), 空气源热泵)",
            ),
            (
                "电接口",
                "制冷接口",
                "蓄冷接口",
                "制热接口",
                "蓄热接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, etype0, etype1, etype2, etype3, etype4: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype3 != "any"]),
                "#0 (conjugate, (电接口, 制冷接口, 蓄冷接口, 制热接口, 蓄热接口), 空气源热泵)",
            ),
        }.items()
    },
    "蒸汽溴化锂": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "蒸汽接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (蒸汽接口, 冷源接口, 制冷接口), 蒸汽溴化锂)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#1 (conjugate, (蒸汽接口, 冷源接口, 制冷接口), 蒸汽溴化锂)",
            )
        }.items()
    },
    "热水溴化锂": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "热水接口",
                "冷源接口",
                "制冷接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (热水接口, 冷源接口, 制冷接口), 热水溴化锂)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#1 (conjugate, (热水接口, 冷源接口, 制冷接口), 热水溴化锂)",
            )
        }.items()
    },
    "电热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("制热接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (制热接口, 电接口), 电热水锅炉)",
            ),
            ("电接口", "制热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电接口, 制热接口), 电热水锅炉)",
            ),
        }.items()
    },
    "电蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "电接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (蒸汽接口, 电接口), 电蒸汽锅炉)",
            ),
            ("电接口", "蒸汽接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电接口, 蒸汽接口), 电蒸汽锅炉)",
            ),
        }.items()
    },
    "天然气热水锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("制热接口", "燃料接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (制热接口, 燃料接口), 天然气热水锅炉)",
            ),
            ("燃料接口", "制热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (燃料接口, 制热接口), 天然气热水锅炉)",
            ),
        }.items()
    },
    "天然气蒸汽锅炉": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蒸汽接口", "燃料接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (蒸汽接口, 燃料接口), 天然气蒸汽锅炉)",
            ),
            ("燃料接口", "蒸汽接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (燃料接口, 蒸汽接口), 天然气蒸汽锅炉)",
            ),
        }.items()
    },
    "电解槽": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("电接口", "设备余热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电接口, 设备余热接口), 电解槽)",
            ),
            ("电接口", "制氢接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (电接口, 制氢接口), 电解槽)",
            ),
            (
                "电接口",
                "制氢接口",
                "设备余热接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (电接口, 制氢接口, 设备余热接口), 电解槽)",
            ),
        }.items()
    },
    "水蓄能": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蓄冷接口", "蓄热接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond1 not in ["idle"]), int(cond0 not in ["idle"])]) <= 1,
                "#0 (conjugate, (蓄冷接口, 蓄热接口), 水蓄能)",
            )
            and logFailedRule(
                sum([int(it != "any") for it in [etype0, etype1]]) >= 1,
                "#1 (conjugate, (蓄冷接口, 蓄热接口), 水蓄能)",
            ),
            ("蓄热接口", "蓄冷接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#0 (conjugate, (蓄热接口, 蓄冷接口), 水蓄能)",
            ),
        }.items()
    },
    "蓄冰槽": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("蓄冰接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (蓄冰接口), 蓄冰槽)",
            )
        }.items()
    },
    "储氢罐": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("储氢接口",): lambda cond0, etype0: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any"]),
                "#0 (conjugate, (储氢接口), 储氢罐)",
            )
        }.items()
    },
    "输水管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "输入接口",
                "电接口",
                "输出接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#0 (conjugate, (输入接口, 电接口, 输出接口), 输水管道)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#1 (conjugate, (输入接口, 电接口, 输出接口), 输水管道)",
            ),
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                sum([int(cond0 in ["input"]), int(cond1 in ["input"])]) <= 1,
                "#0 (conjugate, (输入接口, 输出接口), 输水管道)",
            )
            and logFailedRule(
                all(["冷" in it or it == "any" for it in [etype0, etype1]])
                or all(["热" in it or it == "any" for it in [etype0, etype1]]),
                "#1 (conjugate, (输入接口, 输出接口), 输水管道)",
            ),
            (
                "输入接口",
                "输出接口",
                "电接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (输入接口, 输出接口, 电接口), 输水管道)",
            ),
        }.items()
    },
    "蒸汽管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (输入接口, 输出接口), 蒸汽管道)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#1 (conjugate, (输入接口, 输出接口), 蒸汽管道)",
            )
            and logFailedRule(
                sum([int(cond0 in ["input"]), int(cond1 in ["input"])]) <= 1,
                "#2 (conjugate, (输入接口, 输出接口), 蒸汽管道)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#3 (conjugate, (输入接口, 输出接口), 蒸汽管道)",
            )
        }.items()
    },
    "复合输水管道": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "电接口",
                "冷输入接口",
                "冷输出接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond2 in ["any", "input"], cond0 in ["any", "input"]])
                if cond1 in ["output"]
                else True,
                "#0 (conjugate, (电接口, 冷输入接口, 冷输出接口), 复合输水管道)",
            )
            and logFailedRule(
                all([cond1 in ["any", "input"], cond0 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#1 (conjugate, (电接口, 冷输入接口, 冷输出接口), 复合输水管道)",
            ),
            (
                "热输出接口",
                "电接口",
                "热输入接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "input"], cond1 in ["any", "input"]])
                if cond2 in ["output"]
                else True,
                "#0 (conjugate, (热输出接口, 电接口, 热输入接口), 复合输水管道)",
            )
            and logFailedRule(
                all([cond2 in ["any", "input"], cond1 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#1 (conjugate, (热输出接口, 电接口, 热输入接口), 复合输水管道)",
            ),
            (
                "热输出接口",
                "冷输入接口",
                "热输入接口",
                "冷输出接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                sum(
                    [
                        int(cond1 in ["input"]),
                        int(cond2 in ["input"]),
                        int(cond3 in ["input"]),
                        int(cond0 in ["input"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (热输出接口, 冷输入接口, 热输入接口, 冷输出接口), 复合输水管道)",
            ),
            (
                "冷输入接口",
                "热输入接口",
                "冷输出接口",
                "热输出接口",
                "电接口",
            ): lambda cond0, cond1, cond2, cond3, cond4, etype0, etype1, etype2, etype3, etype4: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [
                        etype0 != "any",
                        etype1 != "any",
                        etype2 != "any",
                        etype3 != "any",
                        etype4 != "any",
                    ]
                ),
                "#0 (conjugate, (冷输入接口, 热输入接口, 冷输出接口, 热输出接口, 电接口), 复合输水管道)",
            ),
        }.items()
    },
    "水水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (输入接口, 输出接口), 水水换热器)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#1 (conjugate, (输入接口, 输出接口), 水水换热器)",
            )
            and logFailedRule(
                sum([int(cond0 in ["input"]), int(cond1 in ["input"])]) <= 1,
                "#2 (conjugate, (输入接口, 输出接口), 水水换热器)",
            )
            and logFailedRule(
                all(["冷" in it or it == "any" for it in [etype0, etype1]])
                or all(["热" in it or it == "any" for it in [etype0, etype1]]),
                "#3 (conjugate, (输入接口, 输出接口), 水水换热器)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#4 (conjugate, (输入接口, 输出接口), 水水换热器)",
            )
        }.items()
    },
    "复合水水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("冷输入接口", "冷输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#0 (conjugate, (冷输入接口, 冷输出接口), 复合水水换热器)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#1 (conjugate, (冷输入接口, 冷输出接口), 复合水水换热器)",
            ),
            ("热输出接口", "热输入接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (热输出接口, 热输入接口), 复合水水换热器)",
            )
            and logFailedRule(
                all([cond1 in ["any", "input"]]) if cond0 in ["output"] else True,
                "#1 (conjugate, (热输出接口, 热输入接口), 复合水水换热器)",
            ),
            (
                "热输出接口",
                "冷输入接口",
                "热输入接口",
                "冷输出接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                sum(
                    [
                        int(cond1 in ["input"]),
                        int(cond2 in ["input"]),
                        int(cond3 in ["input"]),
                        int(cond0 in ["input"]),
                    ]
                )
                <= 1,
                "#0 (conjugate, (热输出接口, 冷输入接口, 热输入接口, 冷输出接口), 复合水水换热器)",
            ),
            (
                "冷输入接口",
                "热输入接口",
                "冷输出接口",
                "热输出接口",
            ): lambda cond0, cond1, cond2, cond3, etype0, etype1, etype2, etype3: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all(
                    [etype0 != "any", etype1 != "any", etype2 != "any", etype3 != "any"]
                ),
                "#0 (conjugate, (冷输入接口, 热输入接口, 冷输出接口, 热输出接口), 复合水水换热器)",
            ),
        }.items()
    },
    "气水换热器": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#0 (conjugate, (输入接口, 输出接口), 气水换热器)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#1 (conjugate, (输入接口, 输出接口), 气水换热器)",
            )
        }.items()
    },
    "单向线": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            ("输入接口", "输出接口"): lambda cond0, cond1, etype0, etype1: logFailedRule(
                all([cond1 in ["any", "output"]]) if cond0 in ["input"] else True,
                "#0 (conjugate, (输入接口, 输出接口), 单向线)",
            )
            and logFailedRule(
                all([cond0 in ["any", "input"]]) if cond1 in ["output"] else True,
                "#1 (conjugate, (输入接口, 输出接口), 单向线)",
            )
            and logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any"]),
                "#2 (conjugate, (输入接口, 输出接口), 单向线)",
            )
        }.items()
    },
    "互斥元件": lambda port_kind_to_port_name: {
        tuple([port_kind_to_port_name[it] for it in k]): v
        for k, v in {
            (
                "互斥接口B",
                "互斥接口A",
                "外部接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                all([cond0 in ["any", "idle"], cond2 in ["any", "output"]])
                if cond1 in ["input"]
                else True,
                "#0 (conjugate, (互斥接口B, 互斥接口A, 外部接口), 互斥元件)",
            )
            and logFailedRule(
                all([cond0 in ["any", "idle"], cond2 in ["any", "input"]])
                if cond1 in ["output"]
                else True,
                "#1 (conjugate, (互斥接口B, 互斥接口A, 外部接口), 互斥元件)",
            )
            and logFailedRule(
                all([cond1 in ["any", "idle"], cond2 in ["any", "output"]])
                if cond0 in ["input"]
                else True,
                "#2 (conjugate, (互斥接口B, 互斥接口A, 外部接口), 互斥元件)",
            )
            and logFailedRule(
                all([cond1 in ["any", "idle"], cond2 in ["any", "input"]])
                if cond0 in ["output"]
                else True,
                "#3 (conjugate, (互斥接口B, 互斥接口A, 外部接口), 互斥元件)",
            )
            and logFailedRule(
                all([cond1 in ["any", "idle"], cond0 in ["any", "idle"]])
                if cond2 in ["idle"]
                else True,
                "#4 (conjugate, (互斥接口B, 互斥接口A, 外部接口), 互斥元件)",
            ),
            (
                "互斥接口A",
                "互斥接口B",
                "外部接口",
            ): lambda cond0, cond1, cond2, etype0, etype1, etype2: logFailedRule(
                True
                if ies_env.UNCHECK_CONNECTIVITY_IN_DYNAMIC_TYPE_VERIFICATION
                else all([etype0 != "any", etype1 != "any", etype2 != "any"]),
                "#0 (conjugate, (互斥接口A, 互斥接口B, 外部接口), 互斥元件)",
            ),
        }.items()
    },
}


def convert_topo_to_prolog_render_params_and_verification_params(topo):
    possibleEnergyTypes = set()
    possibleDeviceTypes = set()

    portNameToPortPossibleStates = {}  #
    deviceTypeToDeviceNames = {}  #
    deviceNameToPortNames = {}  #
    energyTypeToPortNames = {}  #
    adderNameToAdderPortNames = {}  #

    port_name_lookup_table = {}

    adders = topo.get_all_adders()
    adder_index_to_adder_name = {}

    port_verifiers = {}
    conjugate_port_verifiers = (
        {}
    )  # TODO: parse additional conjugate port verifiers from topo object.

    for devInfo in topo.get_all_devices():
        node_id = devInfo["id"]
        node_subtype = devInfo["subtype"]
        possibleDeviceTypes.add(node_subtype)
        devName = f"{node_subtype}_{node_id}"
        deviceNameToPortNames[devName] = []
        if node_subtype not in deviceTypeToDeviceNames.keys():
            deviceTypeToDeviceNames[node_subtype] = []
        deviceTypeToDeviceNames[node_subtype].append(devName)
        ports = devInfo["ports"]

        typeInfo = deviceTypeToTypeInfo[node_subtype]
        requiredPortFrontendNameToPortPossibleStates = typeInfo[
            "requiredPortFrontendNameToPortPossibleStates"
        ]
        requiredPortFrontendNameToEnergyTypes = typeInfo[
            "requiredPortFrontendNameToEnergyTypes"
        ]

        port_kind_to_port_name = {}

        for port_kind, port_info in ports.items():
            portPossibleStates = requiredPortFrontendNameToPortPossibleStates[port_kind]
            portPossibleEnergyTypes = requiredPortFrontendNameToEnergyTypes[port_kind]
            possibleEnergyTypes.update(portPossibleEnergyTypes)

            port_name = f"{devName}_{port_kind}"
            port_kind_to_port_name[port_kind] = port_name

            verifier = port_verifier_lookup_table.get(node_subtype, {}).get(
                port_kind, None
            )
            if verifier:
                port_verifiers[port_name] = verifier

            deviceNameToPortNames[devName].append(port_name)
            port_id = port_info["id"]
            port_name_lookup_table[port_id] = port_name
            portNameToPortPossibleStates[port_name] = portPossibleStates

            for energyType in portPossibleEnergyTypes:
                if energyType not in energyTypeToPortNames.keys():
                    energyTypeToPortNames[energyType] = []
                energyTypeToPortNames[energyType].append(port_name)

        conjugate_verifiers_constructor = (
            conjugate_port_verifier_constructor_lookup_table.get(
                node_subtype, lambda d: {}
            )
        )
        conjugate_verifiers = conjugate_verifiers_constructor(port_kind_to_port_name)
        conjugate_port_verifiers.update(conjugate_verifiers)

    for adder_index, adder_def in adders.items():
        index = str(adder_index).replace("-", "_")
        adder_name = f"adder{index}"
        adder_index_to_adder_name[adder_index] = adder_name
        port_name_list = []
        for _, port_index_list in adder_def.items():
            for port_index in port_index_list:
                port_name = port_name_lookup_table[port_index]
                port_name_list.append(port_name)
        adderNameToAdderPortNames[adder_name] = port_name_list

    render_params = dict(
        portNameToPortPossibleStates=portNameToPortPossibleStates,
        deviceTypes=list(possibleDeviceTypes),
        deviceTypeToDeviceNames=deviceTypeToDeviceNames,
        deviceNameToPortNames=deviceNameToPortNames,
        energyTypes=list(possibleEnergyTypes),
        energyTypeToPortNames=energyTypeToPortNames,
        adderNameToAdderPortNames=adderNameToAdderPortNames,
    )

    port_index_lookup_table = {v: k for k, v in port_name_lookup_table.items()}

    adder_name_to_adder_index = {v: k for k, v in adder_index_to_adder_name.items()}
    adder_index_to_port_name = {}

    for adderName, adderPortNames in adderNameToAdderPortNames.items():
        port_index_to_port_name = {
            port_index_lookup_table[portName]: portName for portName in adderPortNames
        }
        adder_index = adder_name_to_adder_index[adderName]
        adder_index_to_port_name[adder_index] = port_index_to_port_name

    verification_params = (
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
    )

    return render_params, verification_params


basepath = os.path.dirname(__file__)

template_path = "prolog_gen.pro.j2"

template_abs_path = os.path.join(basepath, template_path)

os.environ["NO_PYTHON_TYPECHECK"] = "True"
from jinja_utils import load_template_text

with open(template_abs_path, "r") as f:
    template_content = f.read()
    template_obj = load_template_text(template_content)


def render_prolog_code(render_params):
    prolog_code = template_obj.render(**render_params)
    logger_print("prolog code:", prolog_code)
    return prolog_code


def dynamic_verify_topo_object(topo):
    (
        render_params,
        verification_params,
    ) = convert_topo_to_prolog_render_params_and_verification_params(topo)

    (
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
    ) = verification_params
    adderNameToAdderPortNames = render_params["adderNameToAdderPortNames"]

    if ies_env.USE_PROLOG_CODE:
        prolog_script_content = render_prolog_code(render_params)

        (
            can_proceed,
            isomorphic_topo_status,
        ) = execute_prolog_script_and_check_if_can_proceed(
            prolog_script_content,
            adder_index_to_port_name,
            port_verifiers,
            conjugate_port_verifiers,
            adderNameToAdderPortNames,
        )
    else:
        (
            can_proceed,
            isomorphic_topo_status,
        ) = execute_python_code_and_check_if_can_proceed(
            render_params,
            adder_index_to_port_name,
            port_verifiers,
            conjugate_port_verifiers,
            adderNameToAdderPortNames,
        )

    return can_proceed, isomorphic_topo_status


##############################################

from error_utils import ErrorManager
from failsafe_utils import chdir_context

##############################################

from swiplserver import PrologMQI, PrologThread
from pydantic import BaseModel
from typing import List, Dict

# from HashableDict.HashableDict import HashDict
from frozendict import frozendict
import rich
import os
import tempfile
from config import ies_env

banner = lambda title: logger_print(title.center(60, "-"))
PROLOG_STACK_LIMIT = ies_env.PROLOG_STACK_LIMIT
PROLOG_SHARED_TABLE_LIMIT = ies_env.PROLOG_SHARED_TABLE_LIMIT
PROLOG_TABLE_SIZE_LIMIT = ies_env.PROLOG_TABLE_SIZE_LIMIT


def query_result_from_prolog(
    prolog_script_content: str, adder_index_to_port_name, adderNameToAdderPortNames
):
    banner("querying")
    topology_status_dict = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        with chdir_context(temp_dir):
            prolog_file_path = "prolog_script.pro"
            prolog_file_path_abs = os.path.join(prolog_file_path)
            prolog_path_args = []
            if PROLOG_STACK_LIMIT is not None:
                prolog_path_args.append(f"--stack-limit={PROLOG_STACK_LIMIT}G")
            if PROLOG_SHARED_TABLE_LIMIT is not None:
                prolog_path_args.append(
                    f"--shared-table-space={PROLOG_SHARED_TABLE_LIMIT}G"
                )
            if PROLOG_TABLE_SIZE_LIMIT is not None:
                prolog_path_args.append(f"--table-space={PROLOG_TABLE_SIZE_LIMIT}G")
            with open(prolog_file_path_abs, "w+") as f:
                f.write(prolog_script_content)
            with PrologMQI(prolog_path_args=prolog_path_args) as mqi:
                with mqi.create_thread() as prolog_thread:
                    topology_status_dict = query_prolog_in_context(
                        topology_status_dict,
                        prolog_file_path,
                        prolog_thread,
                        adder_index_to_port_name,
                        adderNameToAdderPortNames,
                    )
    return topology_status_dict


def construct_query_result_iterator(thread, query):
    thread.query_async(query, find_all=False)
    while True:
        it = thread.query_async_result()
        if it is not None:
            yield it
        else:
            break


import progressbar
import hashlib

import itertools


def get_all_combinations(
    portNameToPortPossibleStates, energyTypeToPortNames, adderNameToAdderPortNames
):
    port_name_to_possible_energy_types = {}

    for k, vlist in energyTypeToPortNames.items():
        for v in vlist:
            if v not in port_name_to_possible_energy_types.keys():
                port_name_to_possible_energy_types[v] = [k]
            port_name_to_possible_energy_types[v].append(k)

    adder_name_list = list(adderNameToAdderPortNames.keys())

    possible_simutaneous_adder_energy_types = set()

    adder_name_to_possible_adder_energy_types = {}

    for adder_name, _port_name_list in adderNameToAdderPortNames.items():
        paet = set()
        for pn in _port_name_list:
            ets = port_name_to_possible_energy_types[pn]
            paet.update(ets)
        adder_name_to_possible_adder_energy_types[adder_name] = paet

    possible_simutaneous_adder_energy_types = []

    possible_simutaneous_adder_energy_types = list(
        itertools.product(*adder_name_to_possible_adder_energy_types.values())
    )

    result = []

    # get `possible_adder_energy_types` from prolog?
    for simutaneous_adder_energy_types in possible_simutaneous_adder_energy_types:
        simutaneous_state = []
        # all idle, otherwise at least one input one output
        aet_to_ps_l = []
        for adder_index, aet in enumerate(simutaneous_adder_energy_types):
            sasp = []
            adder_name = adder_name_list[adder_index]
            _port_name_list = adderNameToAdderPortNames[adder_name]
            psl = []
            for pn in _port_name_list:
                ppet = port_name_to_possible_energy_types[pn]
                pps = portNameToPortPossibleStates[pn]
                if aet in ppet:
                    ps = pps
                else:
                    assert "idle" in pps
                    ps = ["idle"]
                psl.append(ps)
            for elem in itertools.product(*psl):
                if all([e == "idle" for e in elem]) or (
                    "input" in elem and "output" in elem
                ):
                    sasp.append([aet, elem])
            aet_to_ps_l.append(sasp)

        for elem in itertools.product(*aet_to_ps_l):
            simutaneous_state.append(elem)
        result.extend(simutaneous_state)
    return result


def query_result_from_python(
    render_params, adder_index_to_port_name, adderNameToAdderPortNames
):
    adder_name_list, adder_index_mapping = query_init(adder_index_to_port_name)

    STATUS_LIST = get_all_combinations(
        render_params["portNameToPortPossibleStates"],
        render_params["energyTypeToPortNames"],
        render_params["adderNameToAdderPortNames"],
    )

    logger_print("parsing result")
    topology_status_dict = parse_status_list(
        STATUS_LIST,
        adder_index_mapping,
        adder_index_to_port_name,
        adderNameToAdderPortNames,
    )

    logger_print("result parsed")
    return topology_status_dict


def parse_status_list(
    STATUS_LIST,
    adder_index_mapping,
    adder_index_to_port_name,
    adderNameToAdderPortNames,
):
    topology_status_dict = {}
    for simutaneous_status in progressbar.progressbar(STATUS_LIST):
        adder_status_dict = {}
        port_status_dict = {}
        for _index, adder_simutaneous_status in enumerate(simutaneous_status):
            adder_index = adder_index_mapping[_index]
            adder_name = "adder{}".format(str(adder_index).replace("-", "_"))
            adder_energy_type, adder_port_status = adder_simutaneous_status
            adder_status_dict[adder_index] = adder_energy_type
            port_index_to_port_name = adder_index_to_port_name[adder_index]
            for _port_index, port_status in enumerate(adder_port_status):
                port_name = adderNameToAdderPortNames[adder_name][_port_index]
                port_status_dict[port_name] = port_status
        key = frozendict(adder_status_dict)
        value = frozendict(port_status_dict)
        if key not in topology_status_dict.keys():
            topology_status_dict[key] = set()
        topology_status_dict[key].add(value)
    return topology_status_dict


def query_prolog_common(adder_name_list, prolog_file_path, prolog_thread):
    adder_names = ", ".join(adder_name_list)
    logger_print("adder_names: ", adder_names)
    prolog_thread.query(f'["{prolog_file_path}"].')
    logger_print("retrieving result")
    query = f"adder_port_status_list([{adder_names}], STATUS)"
    _iterator = construct_query_result_iterator(prolog_thread, query)

    STATUS_LIST = []

    hashset = set()

    for result in progressbar.progressbar(_iterator):
        STATUS = result[0]["STATUS"]
        status_hash = hashlib.md5(str(STATUS).encode()).hexdigest()
        if status_hash not in hashset:
            hashset.add(status_hash)
            STATUS_LIST.append(STATUS)
    return STATUS_LIST


def query_init(adder_index_to_port_name):
    adder_name_list = []
    adder_index_mapping = {}

    for i, k in enumerate(adder_index_to_port_name.keys()):
        adder_name_list.append("adder{}".format(str(k).replace("-", "_")))
        adder_index_mapping[i] = k
    return adder_name_list, adder_index_mapping


def query_prolog_in_context(
    topology_status_dict,
    prolog_file_path,
    prolog_thread,
    adder_index_to_port_name,
    adderNameToAdderPortNames,
):
    adder_name_list, adder_index_mapping = query_init(adder_index_to_port_name)

    STATUS_LIST = query_prolog_common(adder_name_list, prolog_file_path, prolog_thread)

    logger_print("parsing result")
    topology_status_dict = parse_status_list(
        STATUS_LIST,
        adder_index_mapping,
        adder_index_to_port_name,
        adderNameToAdderPortNames,
    )

    logger_print("result parsed")
    return topology_status_dict


def verify_topology_status_dict(
    topology_status_dict,
    port_verifiers,
    conjugate_port_verifiers,
    adder_index_to_port_name,
):
    banner("unverified topo status")
    logger_print(topology_status_dict)
    banner("verifying")

    verified_topology_status_dict = {}

    cached_conjugate_verifiers = {}
    cached_port_verifiers = {}

    for topo_status_index, (adder_status, topo_status) in enumerate(
        topology_status_dict.items()
    ):
        topo_status_frame_flatten = {}
        port_verified = {}
        conjugate_port_verified = {}

        port_name_to_energy_type = {
            v_v: adder_status[k]
            for k, v in adder_index_to_port_name.items()
            for v_k, v_v in v.items()
        }

        for topo_status_frame in topo_status:
            for topo_status_frame_index, (port_name, port_status) in enumerate(
                topo_status_frame.items()
            ):
                # breakpoint()
                if port_name not in topo_status_frame_flatten.keys():
                    topo_status_frame_flatten[port_name] = set()
                _conjugate_verified = True
                cached_quit = False
                with ErrorManager(suppress_error=True) as em:
                    for (
                        conjugate_ports,
                        conjugate_verifier,
                    ) in conjugate_port_verifiers.items():
                        # if not found, then skip this port or idle?
                        conds = [
                            topo_status_frame.get(port_name, UNKNOWN)
                            for port_name in conjugate_ports
                        ]
                        energytypes = [
                            port_name_to_energy_type.get(port_name, UNKNOWN)
                            for port_name in conjugate_ports
                        ]
                        cache_key = (
                            tuple([portNameTransformer(cp) for cp in conjugate_ports]),
                            tuple(conds),
                            tuple(energytypes),
                        )
                        cached = False
                        if cache_key in cached_conjugate_verifiers.keys():
                            cached = True
                            conjugate_verified = cached_conjugate_verifiers[cache_key]
                        else:
                            conjugate_verified = conjugate_verifier(
                                *conds, *energytypes
                            )
                            cached_conjugate_verifiers[cache_key] = conjugate_verified
                        # conjugate_verified = conjugate_verifier(*conds)
                        if not conjugate_verified:
                            if not cached:
                                em.append("-" * 60)
                                em.append(
                                    f"conjugate verification failed for conjugate ports '{conjugate_ports}' at topo status frame #{topo_status_frame_index} (calculated)"
                                )
                                em.append("conds: " + repr(conds))
                                em.append("energy types: " + repr(energytypes))
                            if not cached_quit:
                                cached_quit = True
                            if _conjugate_verified:
                                _conjugate_verified = False
                                break  # to save processing power
                if _conjugate_verified:
                    topo_status_frame_flatten[port_name].add(port_status)
                else:
                    if not cached_quit:
                        logger_print(
                            f"skipping topo status frame #{topo_status_frame_index} due to failed conjugate ports verification"
                        )
        for port_name, verifier in port_verifiers.items():
            conds = topo_status_frame_flatten.get(port_name, [UNKNOWN])
            cached = False
            cache_key = (portNameTransformer(port_name), tuple(conds))
            if cache_key in cached_port_verifiers.keys():
                verified = cached_port_verifiers[cache_key]
                cached = True
            else:
                verified = verifier(conds)
                cached_port_verifiers[cache_key] = verified
            port_verified[port_name] = verified
            if not verified:
                logger_print(
                    f"verifier failed for port '{port_name}', conds: {repr(conds)} (calculated)"
                )

        all_ports_verified = all(port_verified.values())
        all_conjugate_ports_verified = all(conjugate_port_verified.values())
        topo_verified = all_ports_verified and all_conjugate_ports_verified

        if not all_ports_verified:
            logger_print("not all port vaildations have passed")

        if not all_conjugate_ports_verified:
            logger_print("not all conjugate port vaildations have passed")

        if not topo_verified:
            logger_print(
                f"topo verification failed for topo status #{topo_status_index}"
            )
        else:
            if len(topo_status) > 0:
                verified_topology_status_dict[adder_status] = topo_status
            else:
                logger_print("skipping due to empty topo status")
        banner(f"processed topo status #{topo_status_index}")

    banner("verified topo status")
    # if you want verbosity...
    return verified_topology_status_dict


def isomorphicTopologyStatusCombinator(topology_status_dict: dict):
    topo_status_to_adder_status_dict: Dict[frozenset, set] = {}
    for adder_index_to_energy_type, topo_status in topology_status_dict.items():
        topo_status_frozen = frozenset(topo_status)
        if topo_status_frozen not in topo_status_to_adder_status_dict.keys():
            topo_status_to_adder_status_dict[topo_status_frozen] = set()
        topo_status_to_adder_status_dict[topo_status_frozen].add(
            adder_index_to_energy_type
        )
    return topo_status_to_adder_status_dict


def check_if_can_proceed(verified_topology_status_dict):
    isomorphic_topo_status = None
    possible_adder_energy_type_set_counts = len(verified_topology_status_dict)
    logger_print(
        "possible adder energy type set counts:", possible_adder_energy_type_set_counts
    )

    isomorphic_topo_status = isomorphicTopologyStatusCombinator(
        verified_topology_status_dict
    )

    banner("isomorphic topo status (converted)")
    for k, v in isomorphic_topo_status.items():
        logger_print("key:", *[f"\t{str(e_k)}" for e_k in k], "value:", f"\t{v}")
    isomorphic_topo_status_counts = len(isomorphic_topo_status.keys())
    logger_print("isomorphic topo status counts:", isomorphic_topo_status_counts)

    can_proceed = False
    if isomorphic_topo_status_counts == 0:
        logger_print("no adder energy type set")
    elif isomorphic_topo_status_counts > 1:
        logger_print("multiple adder energy type sets found")
    else:
        can_proceed = True
    if not can_proceed:
        logger_print("cannot proceed")
    else:
        logger_print("clear to proceed")
    return can_proceed, isomorphic_topo_status


def check_if_can_proceed_common(
    topology_status_dict,
    port_verifiers,
    conjugate_port_verifiers,
    adder_index_to_port_name,
):
    verified_topology_status_dict = verify_topology_status_dict(
        topology_status_dict,
        port_verifiers,
        conjugate_port_verifiers,
        adder_index_to_port_name,
    )
    can_proceed, isomorphic_topo_status = check_if_can_proceed(
        verified_topology_status_dict
    )
    return can_proceed, isomorphic_topo_status


def execute_python_code_and_check_if_can_proceed(
    render_params,
    adder_index_to_port_name,
    port_verifiers,
    conjugate_port_verifiers,
    adderNameToAdderPortNames,
):
    topology_status_dict = query_result_from_python(
        render_params, adder_index_to_port_name, adderNameToAdderPortNames
    )

    return check_if_can_proceed_common(
        topology_status_dict,
        port_verifiers,
        conjugate_port_verifiers,
        adder_index_to_port_name,
    )


def execute_prolog_script_and_check_if_can_proceed(
    prolog_script_content,
    adder_index_to_port_name,
    port_verifiers,
    conjugate_port_verifiers,
    adderNameToAdderPortNames,
):
    topology_status_dict = query_result_from_prolog(
        prolog_script_content, adder_index_to_port_name, adderNameToAdderPortNames
    )
    return check_if_can_proceed_common(
        topology_status_dict,
        port_verifiers,
        conjugate_port_verifiers,
        adder_index_to_port_name,
    )


def weak_type_check():
    ...
