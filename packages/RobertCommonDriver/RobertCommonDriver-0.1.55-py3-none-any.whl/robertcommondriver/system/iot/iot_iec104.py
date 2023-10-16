from scapy.fields import ByteEnumField, BitEnumField, BitField, ConditionalField, Field, PacketField, LEShortField, ShortField, XByteField, ByteField, PacketListField
from scapy.packet import Packet, Padding, NoPayload
from struct import unpack, pack
from typing import List, Dict, Any, Optional
from threading import Event

from .base import IOTBaseCommon, IOTDriver


'''
pip install scapy==2.4.5
'''

"""
ACPI
    68(1)
    长度(1)
    控制域(4)
        I帧
            发送序号， 接收序号
        S帧
            01 00 接收序号
        U帧
            0x 00 00 00
ASDU
    类型(1)
        监视方向
            1 单点遥信（带品质 不带时标）
            2 双点遥信
            13 段浮点遥测（带品质 不带时标）
        控制方向
            45 单点遥控
        监视方向系统类型
            70 初始化结束
        控制方向系统类型
            100 总召
            101 累积量召唤
            102 读命令
            103 时钟同步
    限定词(1)
        SQ = 0 地址连续 SQ=1地址不连续
    传送原因(2)
        PN
            6 激活
            7 激活确认
            8 停止激活
    地址(2)
    (信息体)(长度-10)
        连续信息传输型
            带绝对时标（遥测）
                地址编号(3字节) 信息体数据 品质描述词(1字节) 重复 信息体数据 品质描述词(1字节) 绝对时标(7字节)
            不带绝对时标（遥测）
                地址编号(3字节) 信息体数据 品质描述词(1字节) 重复 信息体数据 品质描述词(1字节)
            带绝对时标（遥信）
                地址编号(3字节) 信息体数据(1字节) 重复 信息体数据(1字节) 绝对时标(7字节)
            不带绝对时标（遥信）
                地址编号(3字节) 信息体数据(1字节) 重复 信息体数据(1字节)
        非连续信息传输型
            带绝对时标（遥测）
                地址编号(3字节) 信息体数据 品质描述词(1字节) 重复 地址编号(3字节) 信息体数据 品质描述词(1字节) 绝对时标(7字节)
            不带绝对时标（遥测）
                地址编号(3字节) 信息体数据 品质描述词(1字节) 重复 地址编号(3字节) 信息体数据 品质描述词(1字节)
            带绝对时标（遥信）
                地址编号(3字节) 信息体数据(1字节) 重复 地址编号(3字节) 信息体数据(1字节) 绝对时标(7字节)
            不带绝对时标（遥信）
                地址编号(3字节) 信息体数据(1字节) 重复 地址编号(3字节) 信息体数据(1字节)
                
        遥控和设定值
            单点遥控(1字节)   (S/E QU[6:2] RES SCS)
                S/E = 0 遥控执行命令；S/E=1 遥控选择命令；
                QU = 0 被控占内部确定遥控输出方式，不有控制站选择；
                    1 短脉冲方式输出
                    2 长脉冲方式输出
                    3 持续脉冲方式输出
                其他值没有定义
                RES ：保留位
                SCS ： 设置值； 0 = 控开 ；1 = 控合 
            双点遥控(1字节)   (S/E QU[6:2] DCS)
                S/E = 0 遥控执行命令；S/E=1 遥控选择命令；
                QU = 0 被控占内部确定遥控输出方式，不有控制站选择；
                    1 短脉冲方式输出
                    2 长脉冲方式输出
                    3 持续脉冲方式输出
                DCS； 0 无效控制
                    1 控分
                    2 控合
                    3 无效控制
            设定值QOS
            
    遥信：1H-4000H（512）
    遥测：4001H-5000H，首地址：16385（256）
    遥控：6001H-6100H，首地址：24577（128）
    设点：6201H-6400H
    电度：6401H-6600H
    
过程描述
    建立tcp连接；
    主站给从站发送启动帧；报文：68 04 07 00 00 00
    从站收到启动帧，给主站发送启动确认帧；报文：68 04 0B 00 00 00
    主站给从站发送总召唤；报文：68 0E 00 00 00 00 64 01 06 00 01 00 00 00 00 14
    从站收到主站的总召唤命令，给主站发送总召唤确认；
    报文：68 0E 00 00 02 00 64 01 07 00 01 00 00 00 00 14
    从站上传遥信，遥测，电度等I帧信息帧，发送完毕从站发送总召唤结束帧；
    主站收到从站发送的结束帧，会回复一个S帧的确认帧；
    进入下一个周期（其中如何数据有变化，从站需要主动上报）
"""


class IECDefine:

    # 显示类型
    ASDU_DISPLAY = 0    # 0 原值 1 英文 2 中文

    @staticmethod
    def convert_dispay(maps: dict, value: Any, type: int = 1):
        """转换显示"""
        if type == 1:
            if isinstance(maps, dict):
                values = maps.get(value, ['', ''])
                if isinstance(values, list):
                    if len(values) >= 2:
                        return values[0]
                else:
                    return values
        elif type == 2:
            if isinstance(maps, dict):
                values = maps.get(value, ['', ''])
                if isinstance(values, list):
                    if len(values) >= 2:
                        return values[1]
                else:
                    return values
        return value

    # 类型标识(1字节)
    ASDU_TYPE = {
        0x01:  'M_SP_NA_1',    #单点遥信(带品质描述 不带时标)
        0x03:  'M_DP_NA_1',    #双点遥信(带品质描述 不带时标)
        0x05:  'M_ST_NA_1',    #步位置信息(带品质描述 不带时标)
        0x07:  'M_BO_NA_1',    #32比特串(带品质描述 不带时标)
        0x09:  'M_ME_NA_1',    #规一化遥测值(带品质描述 不带时标)
        0x0B:  'M_ME_NB_1',    #标度化遥测值(带品质描述 不带时标)
        0x0D:  'M_ME_NC_1',    #短浮点遥测值(带品质描述 不带时标)
        0x0F:  'M_IT_NA_1',    #累积量(带品质描述 不带时标)
        0x14:  'M_PS_NA_1',    #成组单点遥信(只带变量标志)
        0x15:  'M_ME_ND_1',    #规一化遥测值(不带品质描述 不带时标)
        0x1E:  'M_SP_TB_1',    #单点遥信(带品质描述 带绝对时标)
        0x1F:  'M_DP_TB_1',    #双点遥信(带品质描述 带绝对时标)
        0x20:  'M_ST_TB_1',    #步位置信息(带品质描述 带绝对时标)
        0x21:  'M_BO_TB_1',    #32比特串(带品质描述 带绝对时标)
        0x22:  'M_ME_TD_1',    #规一化遥测值(带品质描述 带绝对时标)
        0x23:  'M_ME_TE_1',    #标度化遥测值(带品质描述 带绝对时标)
        0x24:  'M_ME_TF_1',    #短浮点遥测值(带品质描述 带绝对时标)
        0x25:  'M_IT_TB_1',    #累积量(带品质描述 带绝对时标)
        0x26:  'M_EP_TD_1',    #继电保护装置事件(带品质描述 带绝对时标)
        0x27:  'M_EP_TE_1',    #继电保护装置成组启动事件(带品质描述 带绝对时标)
        0x28:  'M_EP_TF_1',    #继电保护装置成组出口信息(带品质描述 带绝对时标)
        0x2D:  'C_SC_NA_1',    #单点遥控(一个报文只有一个遥控信息体 不带时标)
        0x2E:  'C_DC_NA_1',    #双点遥控(一个报文只有一个遥控信息体 不带时标)
        0x2F:  'C_RC_NA_1',    #升降遥控(一个报文只有一个遥控信息体 不带时标)
        0x30:  'C_SE_NA_1',    #规一化设定值(一个报文只有一个设定值 不带时标)
        0x31:  'C_SE_NB_1',    #标度化设定值(一个报文只有一个设定值 不带时标)
        0x32:  'C_SE_NC_1',    #短浮点设定值(一个报文只有一个设定值 不带时标)
        0x33:  'C_SE_ND_1',    #32比特串(一个报文只有一个设定值 不带时标)
        0x3A:  'C_SE_TA_1',    #单点遥控(一个报文只有一个设定值 带时标)
        0x3B:  'C_SE_TB_1',    #双点遥控(一个报文只有一个设定值 带时标)
        0x3C:  'C_SE_TC_1',    #升降遥控(一个报文只有一个设定值 带时标)
        0x3D:  'C_SE_TD_1',    #规一化设定值(一个报文只有一个设定值 带时标)
        0x3E:  'C_SE_TE_1',    #标度化设定值(一个报文只有一个设定值 带时标)
        0x3F:  'C_SE_TF_1',    #短浮点设定值(一个报文只有一个设定值 带时标)
        0x40:  'C_SE_TG_1',    #32比特串(一个报文只有一个设定值 带时标)
        0x46:  'M_EI_NA_1',    #初始化结束(从站发送，主站收到时候会做一次总召)
        0x64:  'C_IC_NA_1',    #总召
        0x65:  'C_CI_NA_1',    #累积量召唤
        0x66:  'C_RD_NA_1',    #读命令
        0x67:  'C_CS_NA_1',    #时钟同步命令
        0x69:  'C_RS_NA_1',    #复位进程命令
        0x6B:  'C_TS_NA_1',    #带时标的测试命令
        0x88:  'C_SE_NE_1',    #规一化设定值(一个报文可以包含多个设定值 不带时标)
    }

    # 帧类型
    APCI_TYPE = {
        0x00: 'I',
        0x01: 'S',
        0x03: 'U'
    }

    # U帧类型
    APCI_U_TYPE = {
        0x01: 'STARTDT act',    # U帧-激活传输启动
        0x02: 'STARTDT con',    # U帧-确认激活传输启动
        0x04: 'STOPDT act',     # U帧-停止传输
        0x08: 'STOPDT con',     # U帧-停止确认
        0x10: 'TESTFR act',     # U帧-测试询问帧
        0x20: 'TESTFR con',     # U帧-测试询确认
    }

    # 可变结构限定词(1字节)
    ASDU_SQ = {
        0X00: 0,
        0x80: 1  # 信息对象的地址连续 总召唤时，为了压缩信息传输时间SQ=
    }

    # 传送原因(2字节)
    ASDU_CAUSE = {
        0: 'not used',
        1: 'per/cyc',  # 周期 循环
        2: 'back',  # 背景扫描
        3: 'spont',  # 突发
        4: 'init',  # 初始化
        5: 'req',  # 请求或被请求
        6: 'act',  # 激活
        7: 'act config',  # 激活确认
        8: 'deact',  # 停止激活
        9: 'deact config',  # 停止激活确认
        10: 'act term',  # 激活终止
        11: 'retrem',  # 远方命令引起的返送信息
        12: 'retloc',  # 当地命令引起的返送信息
        13: 'file',
        20: 'inrogen',  # 响应站召唤
        21: 'inro1',  # 响应第1组召唤
        22: 'inro2',  # 响应第2组召唤
        23: 'inro3',
        24: 'inro4',
        25: 'inro5',
        26: 'inro6',
        27: 'inro7',
        28: 'inro8',
        29: 'inro9',
        30: 'inro10',
        31: 'inro11',
        32: 'inro12',
        33: 'inro13',
        34: 'inro14',
        35: 'inro15',
        36: 'inro16',
        37: 'reqcogen',  # 响应累积量站召唤
        38: 'reqco1',
        39: 'reqco2',
        40: 'reqco3',
        41: 'reqco4',
        44: 'unknown type identification',  # 未知的类型标识
        45: 'unknown cause of transmission',  # 未知的传送原因
        46: 'unknown common address of ASDU',  # 未知的应用服务数据单元公共地址
        47: 'unknown information object address'  # 未知的信息对象地址
    }

    # 传送原因 P/N
    ASDU_PN = {
        0x00: 'Positive confirm',
        0x40: 'Negative confirm'
    }

    # 溢出标识符
    ASDU_OV = {
        0X00: 'no overflow',    # 未溢出
        0x01: 'overflow'    # 溢出
    }

    # 二进制读数 计数器被调整
    ASDU_CA = {
        0X00: 'not adjusted',  # 未被调整
        0x01: 'adjusted'  # 被调整
    }

    # 封锁标识符
    ASDU_BL = {
        0X00: 'not blocked',    # 未被封锁
        0x10: 'blocked'     # 被封锁
    }

    # 取代标识符
    ASDU_SB = {
        0X00: 'not substituted',    # 未被取代
        0x20: 'substituted' # 被取代
    }

    # 刷新标识符
    ASDU_NT = {
        0X00: 'topical',    # 刷新成果
        0x40: 'not topical' # 刷新未成功
    }

    # 有效标志位
    ASDU_IV = {
        0X00: 'valid',      # 状态有效
        0x80: 'invalid'     # 状态无效
    }

    # 遥测品质描述词
    ASDU_QDS_FLAGS = ['OV', 'RES', 'RES', 'RES', 'BL', 'SB', 'NT', 'IV']

    # 双点信息品质描述词
    ASDU_DIQ_FLAGS = ['SPI', 'SPI', 'RES', 'RES', 'BL', 'SB', 'NT', 'IV']

    # 单点信息品质描述词
    ASDU_SIQ_FLAGS = ['SPI', 'RES', 'RES', 'RES', 'BL', 'SB', 'NT', 'IV']

    # 遥控命令方式
    ASDU_SEL_EXEC = {
        0x00: 'Execute',    # 遥控执行命令
        0x80: 'Select',
        0x01: 'Select',     # 遥控选择命令
    }

    ASDU_QL = {
        0x00: 'no use',
    }

    for i in range(1, 64):
        ASDU_QL[i] = f"preserve the accuracy of supporting equipment"    # 为配套设备保准保留

    for i in range(64, 128):
        ASDU_QL[i] = f"reserved for special access"    # 为特殊通途保留

    ASDU_BSID = {
        0x00: 'positive confirmation of selection, request, stop activation or deletion',  # 选择、请求、停止激活或删除的肯定确认
        0x01: 'negative confirmation of selection, request, stop activation or deletion',  # 选择、请求、停止激活或删除的否定确认
    }

    ASDU_STATUS = {
        0x00: 'no use',
    }

    for i in range(1, 16):
        ASDU_STATUS[i] = f"preserve the accuracy of supporting equipment"    # 为配套设备保准保留

    for i in range(16, 32):
        ASDU_STATUS[i] = f"reserved for special access"    # 为特殊通途保留

    ASDU_WORD = {
        0x00: 'no use', # 缺省
        0x01: 'select file',   # 选择文件
        0x02: 'request file',  # 请求文件
        0x03: 'stop activating files',  # 停止激活文件
        0x04: 'delete file',  # 删除文件
        0x05: 'select section',  # 选择节
        0x06: 'request section',  # 请求节
        0x07: 'stop activating sections',  # 停止激活节
    }

    for i in range(8, 11):
        ASDU_WORD[i] = f"standard determiner {i}"    # 标准限定词

    for i in range(11, 16):
        ASDU_WORD[i] = f"specific determiner {i}"    # 特定限定词

    ASDU_AFQ_WORD = {
        0x00: 'no use',  # 缺省
        0x01: 'positive recognition of file transfer',  # 文件传输的肯定认可
        0x02: 'negative recognition of file transfer',  # 文件传输的否定认可
        0x03: 'positive recognition of section transmission',  # 节传输的肯定认可
        0x04: 'negative recognition of section transmission',  # 节传输的否定认可
    }

    for i in range(4, 11):
        ASDU_AFQ_WORD[i] = f"standard determiner {i}"  # 标准限定词

    for i in range(11, 16):
        ASDU_AFQ_WORD[i] = f"specific determiner {i}"  # 特定限定词

    ASDU_ERR = {
        0x00: 'no use', # 缺省
        0x01: 'no requested storage space',   # 无请求的存储空间
        0x02: 'checksum error',  # 校验和错
        0x03: 'unexpected communication services',  # 非所期望的通信服务
        0x04: 'unexpected file name',  # 非所期望的文件名称
        0x05: 'unexpected section name',  # 非所期望的节名称
    }

    for i in range(6, 11):
        ASDU_ERR[i] = f"standard error {i}"    # 标准错误

    for i in range(11, 16):
        ASDU_ERR[i] = f"specific error {i}"    # 特定错误

    ASDU_LSQ = {
        0x00: 'no use',  # 缺省
        0x01: 'file transfer without stopping activation',  # 不带停止激活的文件传输
        0x02: 'file transfer with stop activation',  # 带停止激活的文件传输
        0x03: 'section transmission without stop activation',  # 不带停止激活的节传输
        0x04: 'ection transmission with stop activation',  # 带停止激活的节传输
    }

    for i in range(5, 128):
        ASDU_LSQ[i] = f"standard last paragraph determiner {i}"  # 标准最后节段限定词

    for i in range(128, 256):
        ASDU_LSQ[i] = f"specific last paragraph determiner {i}"  # 特定最后节段限定词

    # 遥控输出方式
    ASDU_QU = {
        0x00: 'no pulse defined',
        0x01: 'short pulse duration (circuit-breaker)',  # 短脉冲方式输出
        0x02: 'long pulse duration',  # 长脉冲方式输出
        0x03: 'persistent output',  # 持续脉冲方式输出
        0x04: 'Standard',
        0x05: 'Standard',
        0x06: 'Standard',
        0x07: 'Standard',
        0x08: 'Standard',
        0x09: 'reserved',
        0x0A: 'reserved',
        0x0B: 'reserved',
        0x0C: 'reserved',
        0x0D: 'reserved',
        0x0E: 'reserved',
        0x0F: 'reserved',
        0x10: 'Specific',
        0x11: 'Specific',
        0x12: 'Specific',
        0x13: 'Specific',
        0x14: 'Specific',
        0x15: 'Specific',
        0x16: 'Specific',
        0x17: 'Specific',
        0x18: 'Specific',
        0x19: 'Specific',
        0x1A: 'Specific',
        0x1B: 'Specific',
        0x1C: 'Specific',
        0x1D: 'Specific',
        0x1E: 'Specific',
        0x1F: 'Specific',
    }

    # 单点遥控设置值
    ASDU_SCS = {
        0x00: 'OFF',    # 控开
        0x01: 'ON'      # 控合
    }

    # 双点遥控设置值
    ASDU_DCS = {
        0x00: 'inactivity control',  # 无效控制
        0x01: 'OFF',  # 控分
        0x02: 'ON',  # 控合
        0x03: 'inactivity control',  # 无效控制
    }

    # 升降命令 RCS
    ASDU_RCS = {
        0x00: 'inactivity control',  # 不允许
        0x01: 'OFF',  # 降一步
        0x02: 'ON',  # 升一步
        0x03: 'inactivity control',  # 不允许
    }

    #
    ASDU_SU = {
        0X80: 'summer time',
        0x00: 'normal time'
    }

    # Day Of Week
    ASDU_DOW = {
        0x00: 'undefined',
        0x01: 'monday',
        0x02: 'tuesday',
        0x03: 'wednesday',
        0x04: 'thursday',
        0x05: 'friday',
        0x06: 'saturday',
        0x07: 'sunday'
    }

    # 过度
    ASDU_TRANSIENT = {
        0x00: 'not in transient',   # 设备未在瞬变状态
        0x80: 'in transient'   # 设备处于瞬变状态
    }

    ASDU_QOI = {
        0x00: 'no use',
        0x14: 'Station interrogation (global)',
        0x15: 'Interrogation of group 1',
        0x16: 'Interrogation of group 2',
        0x17: 'Interrogation of group 3',
        0x18: 'Interrogation of group 4',
        0x19: 'Interrogation of group 5',
        0x1A: 'Interrogation of group 6',
        0x1B: 'Interrogation of group 7',
        0x1C: 'Interrogation of group 8',
        0x1D: 'Interrogation of group 9',
        0x1E: 'Interrogation of group 10',
        0x1F: 'Interrogation of group 11',
        0x20: 'Interrogation of group 12',
        0x21: 'Interrogation of group 13',
        0x22: 'Interrogation of group 14',
        0x23: 'Interrogation of group 15',
        0x24: 'Interrogation of group 16'
    }

    for i in range(1, 20):
        ASDU_QOI[i] = f"reserved for supporting standards"    # 为配套标准保留

    # 单点遥信状态值
    ASDU_SPI = {
        0x00: 'OFF',     # 开
        0x01: 'ON'     # 合
    }

    # 双点遥信状态
    ASDU_DPI = {
        0x00: 'Indeterminate or Intermediate state',    # 不确定状态或中间装填
        0x01: 'Determined state OFF',   # 确定状态的开
        0x02: 'Determined state ON',    # 确定状态的合
        0x03: 'Indeterminate state'     # 不确定状态或中间装填
    }

    # 计数量 FRZ
    ASDU_FRZ = {
        0x00: 'request count quantity',  # 请求计数量
        0x01: 'freeze without reset',  # 冻结不带复位
        0x02: 'freeze band reset',  # 冻结带复位
        0x03: 'count reset'  # 计数量复位
    }

    # 计数量
    ASDU_RQT = {
        0x00: 'quantity not calculated using request',
        0x01: 'total request count',
        0x02: 'request count quantity group 1',
        0x03: 'request count quantity group 2',
        0x04: 'request count quantity group 3',
        0x05: 'request count quantity group 4',
    }

    for i in range(6, 32):
        ASDU_RQT[i] = f"reserved for supporting standards {i}"

    for i in range(32, 64):
        ASDU_RQT[i] = f"reserved for special purposes {i}"

    # GS
    ASDU_GS = {
        0x01: 'total startup',
        0x00: 'no total start',
    }

    # A相保护
    ASDU_SL_A = {
        0x01: 'A-phase protection activation',     # A相保护启动
        0x00: 'A-phase protection not activated',        # A相保护未启动
    }

    ASDU_SL_B = {
        0x01: 'B-phase protection activation',     # B相保护启动
        0x00: 'B-phase protection not activated',    # B相保护未启动
    }

    ASDU_SL_C = {
        0x01: 'C-phase protection activation',      # C相保护启动
        0x00: 'C-phase protection not activated',   # C相保护未启动
    }

    ASDU_SLE = {
        0x01: 'Ground current protection activation',   # 接地电流保护启动
        0x00: 'Ground current protection not activated',  # 接地电流保护未启动
    }

    ASDU_SRD = {
        0x01: 'reverse protection activation',     # 反向保护启动
        0x00: 'reverse protection not activated',    # 反向保护未启动
    }

    ASDU_GC = {
        0x01: 'general command output to output circuit',     # 总命令输出至输出电路
        0x00: 'no general command output to output circuit',    # 无总命令输出至输出电路
    }

    ASDU_GL_A = {
        0x01: 'command output to A-phase output circuit',    # 命令输出至A相输出电路
        0x00: 'no command output to A-phase output circuit',   # 无命令输出至A相输出电路
    }

    ASDU_GL_B = {
        0x01: 'command output to B-phase output circuit',    # 命令输出至B相输出电路
        0x00: 'no command output to B-phase output circuit',   # 无命令输出至B相输出电路
    }

    ASDU_GL_C = {
        0x01: 'command output to C-phase output circuit',    # 命令输出至C相输出电路
        0x00: 'no command output to C-phase output circuit',   # 无命令输出至C相输出电路
    }

    # 参数种类
    ASDU_KPA = {
        0x00: 'unused',     # 未用
        0x01: 'threshold',    # 门限值
        0x02: 'smoothing coefficient (filtering time constant)',   # 平滑系数（滤波时间常数）
        0x03: 'lower limit for transmitting measurement values',   # 传送测量值的下限
        0x04: 'upper limit for transmitting measurement values',   # 传送测量值的上限
    }

    for i in range(5, 32):
        ASDU_KPA[i] = f"standard measured value parameter determiner {i}"  # 标准测量值参数限定词

    for i in range(32, 64):
        ASDU_KPA[i] = f"specific measured value parameter determiner{i}"  # 特定测量值参数限定词

    # 当地参数改变
    ASDU_LPC = {
        0x01: 'change', # 改变
        0x00: 'unchanged',    # 未改变
    }

    # 参数在运行
    ASDU_POP = {
        0x01: 'not running',    # 未运行
        0x00: 'running',     # 运行
    }

    ASDU_QPA = {
        0x00: 'unused',     # 未用
        0x01: 'activate/stop the parameters loaded before activation (information object address=0)',   # 激活/停止激活之前装载的参数(信息对象地址=0)
        0x02: 'activate/deactivate the parameters of the addressed information object',  # 激活/停止激活所寻址信息对象的参数
        0x03: 'activating/deactivating the addressed information object for continuous cyclic or periodic transmission',  # 激活/停止激活所寻址的持续循环或周期传输的信息对象
    }

    for i in range(4, 128):
        ASDU_QPA[i] = f"standard parameter activation determiner {i}"   # 标准参数激活限定词

    for i in range(128, 256):
        ASDU_QPA[i] = f"specific parameter activation determiner{i}"   # 特定参数激活限定词

    ASDU_QRP = {
        0x00: 'not adopted',    # 未采用
        0x01: 'total reset of processes',   # 进程的总复位
        0x02: 'reset the time marked information waiting for processing in the event buffer',     # 复位事件缓冲区等待处理的带时标的信息
    }

    for i in range(3, 128):
        ASDU_QRP[i] = f"standard reset process command determiner {i}"     # 标准复位进程命令限定词

    for i in range(128, 256):
        ASDU_QRP[i] = f"specific reset process command determiner {i}"     # 特定复位进程命令限定词

    # 初始化原因
    ASDU_U17 = {
        0x00: 'Local power switch on',
        0x01: 'Local manual reset',
        0x02: 'Remote reset',
    }

    for i in range(3, 128):
        ASDU_U17[i] = 'Undefined'

    ASDU_BS1 = {
        0x00: 'Initialization with unchanged local parameters',
        0x80: 'Initialization after change of local parameters'
    }


class IECPacket:

    class Q(Packet):
        """品质描述词公有信息"""
        name = 'Q'
        fields_desc = [
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]
            return s

    class SIQ(Packet):
        """7.2.6.1 带品质描述词的单点信息"""
        name = 'SIQ'
        fields_desc = [
            ByteField('SPI', None),
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.SPI = IECDefine.ASDU_SPI[s[0] & 0b1]
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class DIQ(Packet):
        """7.2.6.2带品质描述词的双点信息"""
        name = 'QDS'

        fields_desc = [
            ByteField('DPI', False),
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.DPI = IECDefine.ASDU_DPI[s[0] & 0b11]
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]

            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QDS(Packet):
        """7.2.6.3 品质描述词"""
        name = 'QDS'
        fields_desc = [
            ByteField('OV', None),
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.OV = IECDefine.ASDU_OV[s[0] & 0b1]
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]

            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QDP(Packet):
        """7.2.6.4 继电保护设备事件的品质描述词"""
        name = 'QDP'
        fields_desc = [
            ByteField('EI', False),
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.EI = IECDefine.ASDU_IV[s[0] & 0b1]
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]

            return s[1:]

        def extract_padding(self, s):
            return None, s

    class VTI(Packet):
        """7.2.6.5 带瞬变状态指示的值"""
        name = 'VTI'
        fields_desc = [
            ByteField('Value', False),
            ByteField('Transient', None)
        ]

        def do_dissect(self, s):
            self.Value = s[0] & 0b1111111 # unpack('b', (s[0] & 0b1111111) << 1)[0] >> 1   # 取后七位  左移一位 以有符号单字节整型解析 右移一位
            self.Transient = IECDefine.ASDU_TRANSIENT[s[0] & 0b1]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class NVA(Packet):
        """7.2.6.6 规一化值"""
        name = 'NVA'
        fields_desc = [
            ShortField('NVA', None),
        ]

        def do_dissect(self, s):
            if s[0] & 0b10000000 == 0b10000000:
                # 标志位为1时
                if s[0] == 0b10000000 and s[1] == 0b0:
                    self.NVA = -1
                else:
                    self.NVA = unpack('>H', s[0:2])[0] / 32768
            else:
                # 标志位为0时
                self.NVA = unpack('>H', s[0:2])[0] / 32768
            return s[2:]

        def extract_padding(self, s):
            return None, s

    class SVA(Packet):
        """7.2.6.7 标度化值"""
        name = 'SVA'
        fields_desc = [
            ShortField('SVA', None),
        ]

        def do_dissect(self, s):
            self.SVA = unpack('>h', s[0:2])[0]
            return s[2:]

        def extract_padding(self, s):
            return None, s

    class BCR(Packet):
        """7.2.6.9 二进制计数器读数"""
        name = 'BCR'
        fields_desc = [
            ByteField('V', None),    # 计数读数
            ByteField('SQ', None),    # 顺序记号
            ByteField('CY', None),    #
            ByteField('CA', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            cp8 = s[4]
            self.V = unpack('<i', s[:4])[0]
            self.SQ = cp8 & 0b11111
            self.CY = IECDefine.ASDU_OV[cp8 & 0b100000]
            self.CA = IECDefine.ASDU_CA[cp8 & 0b1000000]
            self.IV = IECDefine.ASDU_IV[cp8 & 0b10000000]
            return s[5:]

        def extract_padding(self, s):
            return None, s

    class SEP(Packet):
        """7.2.6.10 继电保护设备事件的品质描述词"""
        name = 'SEP'
        fields_desc = [
            ByteField('ES', None),
            ByteField('EI', None),
            ByteField('BL', None),
            ByteField('SB', None),
            ByteField('NT', None),
            ByteField('IV', None)
        ]

        def do_dissect(self, s):
            self.EI = IECDefine.ASDU_IV[s[0] & 0b1]
            self.ES = IECDefine.ASDU_DPI[s[0] & 0b11]
            self.BL = IECDefine.ASDU_BL[s[0] & 0b10000]
            self.SB = IECDefine.ASDU_SB[s[0] & 0b100000]
            self.NT = IECDefine.ASDU_NT[s[0] & 0b1000000]
            self.IV = IECDefine.ASDU_IV[s[0] & 0b10000000]

            return s[1:]

        def extract_padding(self, s):
            return None, s

    class SPE(Packet):
        """7.2.6.11 继电保护设备启动事件"""
        name = 'SPE'
        fields_desc = [
            ByteField('GS', None),
            ByteField('SL1', None),
            ByteField('SL2', None),
            ByteField('SL3', None),
            ByteField('SLE', None),
            ByteField('SRD', None)
        ]

        def do_dissect(self, s):
            self.GS = IECDefine.ASDU_GS[s[0] & 0b1]
            self.SL1 = IECDefine.ASDU_SL_A[s[0] & 0b10]
            self.SL2 = IECDefine.ASDU_SL_B[s[0] & 0b100]
            self.SL3 = IECDefine.ASDU_SL_C[s[0] & 0b1000]
            self.SLE = IECDefine.ASDU_SLE[s[0] & 0b10000]
            self.SRD = IECDefine.ASDU_SRD[s[0] & 0b100000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class OCI(Packet):
        """7.2.6.12 继电保护设备输出电路信息"""
        name = 'OCI'
        fields_desc = [
            ByteField('GC', None),
            ByteField('CL1', None),
            ByteField('CL2', None),
            ByteField('CL3', None)
        ]

        def do_dissect(self, s):
            self.GC = IECDefine.ASDU_GC[s[0] & 0b1]
            self.CL1 = IECDefine.ASDU_GL_A[s[0] & 0b10]
            self.CL2 = IECDefine.ASDU_GL_B[s[0] & 0b100]
            self.CL3 = IECDefine.ASDU_GL_C[s[0] & 0b1000]

            return s[1:]

        def extract_padding(self, s):
            return None, s

    class BSI(Packet):
        """7.2.6.13 二进制状态信息"""
        name = 'BSI'
        fields_desc = [
            ByteField('LSS', None),     # 当地显示子系统
            ByteField('RAM', None),  # 变位遥信使遥控 升降 设定命令取消
            ByteField('UPS', None),  # UPS状态
            ByteField('AGC', None),  # 自动发电控制
            ByteField('TRRL', None),  # 遥控转当地
            ByteField('U', None),  # 无人值班
            ByteField('SR', None),  # 系统重新启动
            ByteField('CS', None),  # 冷启动
            ByteField('SS', None),  # 系统自检
            ByteField('PF', None),     # 电源故障
            ByteField('STI', None),     # 短时间干扰
            ByteField('PSUF', None),  # 电源单元有故障
            ByteField('Value', None),
        ]

        def do_dissect(self, s):
            self.Value = ''.join(format(bt, '08b') for bt in s[0:4])
            self.RAM = self.BSI[0]  # 1
            self.LSS = self.BSI[6]  # 7
            self.UPS = self.BSI[16]   # 17
            self.TRRL = self.BSI[18]  # 19
            self.U = self.BSI[19]  # 20
            self.AGC = self.BSI[20]   # 21
            self.SR = self.BSI[24]  # 25
            self.CS = self.BSI[25] # 26
            self.SS = self.BSI[26]  # 27
            self.PF = self.BSI[29]  # 30
            self.STI = self.BSI[30]  # 31
            self.PSUF = self.BSI[31]  # 32
            return s[4:]

        def extract_padding(self, s):
            return None, s

    class FBP(Packet):
        """7.2.6.14 固定测试字，两个八位位组"""
        name = 'FBP'
        fields_desc = [
            ShortField('FBP', None),
        ]

        def do_dissect(self, s):
            self.FBP = unpack('>h', s[0:2])[0]
            return s[2:]

        def extract_padding(self, s):
            return None, s

    class SCO(Packet):
        """7.2.6.15 单命令"""
        name = 'SCO'

        fields_desc = [
            ByteField('SE', None),
            ByteField('QU', None),
            ByteField('SCS', None),
        ]

        def do_dissect(self, s):
            self.QU = IECDefine.ASDU_QU[(s[0] & 0b01111100) >> 2]
            self.SE = IECDefine.ASDU_SEL_EXEC[s[0] & 0b10000000]
            self.SCS = IECDefine.ASDU_SCS[s[0] & 0b1]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class DCO(Packet):
        """7.2.6.16 双命令"""
        name = 'DCO'
        fields_desc = [
            ByteField('SE', None),
            ByteField('QU', None),
            ByteField('DCS', None),
        ]

        def do_dissect(self, s):
            self.QU = IECDefine.ASDU_QU[(s[0] & 0b01111100) >> 2]
            self.SE = IECDefine.ASDU_SEL_EXEC[s[0] & 0b10000000]
            self.DCS = IECDefine.ASDU_DCS[s[0] & 0b11]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class RCO(Packet):
        """7.2.6.17 步调节命令"""
        name = 'RCO'
        fields_desc = [
            ByteField('SE', None),
            ByteField('QU', None),
            ByteField('RCS', None),
        ]

        def do_dissect(self, s):
            self.QU = IECDefine.ASDU_QU[(s[0] & 0b01111100) >> 2]
            self.SE = IECDefine.ASDU_SEL_EXEC[s[0] & 0b10000000]
            self.RCS = IECDefine.ASDU_RCS[s[0] & 0b11],  # TODO
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class CP56Time(Packet):
        """7.2.6.18 七个八位位组二进制时间 该时间为增量时间信息，其增量的参考日期协商确定"""
        name = 'CP56Time'

        fields_desc = [
            ByteField('S', None),
            ByteField('Min', None),
            ByteField('IV', None),
            ByteField('Hour', None),
            ByteField('SU', None),
            ByteField('Day', None),
            ByteField('WeekDay', None),
            ByteField('Month', None),
            ByteField('Year', None),
        ]

        def do_dissect(self, s):
            self.S = unpack('<H', s[0:2])[0] / 1000  # 单位：秒(s)
            self.Min = int(s[2] & 0b111111)
            self.IV = IECDefine.ASDU_IV[s[2] & 0b10000000]
            self.Hour = int(s[3] & 0b11111)
            self.SU = IECDefine.ASDU_SU[s[3] & 0b10000000]
            self.Day = int(s[4] & 0b11111)
            self.WeekDay = IECDefine.ASDU_DOW[s[4] & 0b11100000]
            self.Month = int(s[5] & 0b1111)
            self.Year = int(s[6] & 0b1111111)
            return s[7:]

        def extract_padding(self, s):
            return None, s

    class CP24Time(Packet):
        """7.2.6.19 解析 三个八位位组二进制时间 该时间为增量时间信息，其增量的参考日期协商确定"""
        name = 'CP24Time'
        fields_desc = [
            ByteField('S', None),
            ByteField('Min', None),
            ByteField('IV', None),
        ]

        def do_dissect(self, s):
            self.S = unpack('<H', s[0:2])[0] / 1000  # 单位：秒(s)
            self.Min = int(s[2] & 0b111111)
            self.IV = IECDefine.ASDU_IV[s[2] & 0b10000000]
            return s[3:]

        def extract_padding(self, s):
            return None, s

    class CP16Time(Packet):
        """7.2.6.20 二个八位位组二进制时间 该时间为增量时间信息，其增量的参考日期协商确定"""
        name = 'CP16Time'
        fields_desc = [
            ByteField('S', None),
        ]

        def do_dissect(self, s):
            self.S = unpack('<H', s[0:2])[0] / 1000  # 单位：秒(s)
            return s[2:]

        def extract_padding(self, s):
            return None, s

    class COI(Packet):
        """7.2.6.21 初始化原因"""
        name = 'COI'
        fields_desc = [
            ByteField('U17', None),
            ByteField('BS1', None),
        ]

        def do_dissect(self, s):
            self.U17 = IECDefine.ASDU_U17[s[0] & 0b1111111]
            self.BS1 = IECDefine.ASDU_BS1[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QOI(Packet):
        """7.2.6.22 召唤限定词"""
        name = 'QOI'
        fields_desc = [
            ByteField('QOI', None),
        ]

        def do_dissect(self, s):
            self.QOI = IECDefine.ASDU_QOI.get(s[0])
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QCC(Packet):
        """7.2.6.23 计数量召唤命令限定词"""
        name = 'QCC'
        fields_desc = [
            ByteField('RQT', None),
            ByteField('FRZ', None),
        ]

        def do_dissect(self, s):
            self.FRZ = IECDefine.ASDU_FRZ[(s[0] & 0b11000000) >> 6]
            self.RQT = IECDefine.ASDU_RQT[s[0] & 0b111111]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QPM(Packet):
        """7.2.6.24 测量值参数限定词"""
        name = 'QPM'
        fields_desc = [
            ByteField('KPA', None),
            ByteField('LPC', None),
            ByteField('POP', None),
        ]

        def do_dissect(self, s):
            self.KPA = IECDefine.ASDU_KPA[s[0] & 0b111111]
            self.LPC = IECDefine.ASDU_LPC[s[0] & 0b1000000]
            self.POP = IECDefine.ASDU_POP[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QPA(Packet):
        """7.2.6.25 参数激活限定词"""
        name = 'QPA'
        fields_desc = [
            ByteField('QPA', None)
        ]

        def do_dissect(self, s):
            self.QPA = IECDefine.ASDU_QPA[s[0]]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QOC(Packet):
        """7.2.6.26 命令限定词"""
        name = 'QOC'
        fields_desc = [
            ByteField('QU', None),
            ByteField('SE', None)
        ]

        def do_dissect(self, s):
            self.QU = IECDefine.ASDU_QU[(s[0] & 0b01111100) >> 2]
            self.SE = IECDefine.ASDU_SEL_EXEC[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QRP(Packet):
        """7.2.6.27 复位进程命令限定词"""
        name = 'QRP'

        fields_desc = [
            ByteField('QRP', None),
        ]

        def do_dissect(self, s):
            self.QRP = IECDefine.ASDU_QRP[s[0]]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class FRQ(Packet):
        """7.2.6.28 文件准备就绪限定词"""
        name = 'FRQ'
        fields_desc = [
            ByteField('U17', None),
            ByteField('BSID', None),
        ]

        def do_dissect(self, s):
            self.U17 = IECDefine.ASDU_QL[s[0] & 0b1111111]
            self.BSID = IECDefine.ASDU_BSID[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class SRQ(Packet):
        """7.2.6.29 节准备就绪限定词"""
        name = 'SRQ'
        fields_desc = [
            ByteField('U17', None),
            ByteField('BS1', None),
        ]

        def do_dissect(self, s):
            self.U17 = IECDefine.ASDU_QL[s[0] & 0b1111111]
            self.BS1 = 'not ready' if s[0] & 0b10000000 else 'ready'
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class SCQ(Packet):
        """7.2.6.30 选择和召唤限定词"""
        name = 'SCQ'
        fields_desc = [
            ByteField('Word', None),
            ByteField('Err', None),
        ]

        def do_dissect(self, s):
            self.Word = IECDefine.ASDU_WORD[s[0] & 0b1111]
            self.Err = IECDefine.ASDU_ERR[(s[0] & 0b11110000) >> 4]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class LSQ(Packet):
        """7.2.6.31 最后的节和段的限定词"""
        name = 'LSQ'
        fields_desc = [
            ByteField('LSQ', None),
        ]

        def do_dissect(self, s):
            self.LSQ = IECDefine.ASDU_LSQ[s[0]]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class AFQ(Packet):
        """7.2.6.32 文件认可或节认可限定词"""
        name = 'AFQ'
        fields_desc = [
            ByteField('Word', None),
            ByteField('Err', None),
        ]

        def do_dissect(self, s):
            self.Word = IECDefine.ASDU_AFQ_WORD[s[0] & 0b1111]
            self.Err = IECDefine.ASDU_ERR[(s[0] & 0b11110000) >> 4]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class NOF(Packet):
        """7.2.6.33 文件名称"""
        name = 'NOF'
        fields_desc = [
            ByteField('NAME', None),
        ]

        def do_dissect(self, s):
            self.NAME = s if s[0] else 'no use'
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class NOS(Packet):
        """7.2.6.34 节名称"""
        name = 'NOS'
        fields_desc = [
            ByteField('NOS', None),
        ]

        def do_dissect(self, s):
            self.NOS = s[0] if s[0] else '缺省'
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class LOF(Packet):
        """7.2.6.35 文件或节的长度"""
        name = 'LOF'
        fields_desc = [
            ShortField('LOF', None),
        ]

        def do_dissect(self, s):
            self.LOF = unpack('<I', s[0:1])[0]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class LOS(Packet):
        """7.2.6.36 段的长度"""
        name = 'LOS'
        fields_desc = [
            ShortField('LOS', None),
        ]

        def do_dissect(self, s):
            self.LOS = s[0]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class CHS(Packet):
        """7.2.6.37 校验和"""
        name = 'CHS'
        fields_desc = [
            ShortField('CHS', None),
        ]

        def do_dissect(self, s):
            self.CHS = s[0]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class SOF(Packet):
        """7.2.6.38 文件状态"""
        name = 'SOF'
        fields_desc = [
            ByteField('STATUS', None),
            ByteField('LFD', None),
            ByteField('FOR', None),
            ByteField('FA', None),
        ]

        def do_dissect(self, s):
            self.STATUS = IECDefine.ASDU_STATUS[s[0] & 0b11111]
            self.LFD = 'final catalog file' if s[0] & 0b100000 else 'there are also directory files behind it'
            self.FOR = 'define subdirectory names' if s[0] & 0b1000000 else 'define file name'
            self.FA = 'file transfer activated' if s[0] & 0b10000000 else 'file waiting for transfer'
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class QOS(Packet):
        """7.2.6.39 设定命令限定词"""
        name = 'QOS'
        fields_desc = [
            ByteField('QL', False),
            ByteField('SE', None)
        ]

        def do_dissect(self, s):
            self.QL = IECDefine.ASDU_QL[s[0] & 0b1111111]
            self.SE = IECDefine.ASDU_SEL_EXEC[s[0] & 0b10000000]
            return s[1:]

        def extract_padding(self, s):
            return None, s

    class SCD(Packet):
        """7.2.6.40 状态和状态变位检出"""
        name = 'SCD'
        fields_desc = [
            ByteField('ST', None),
            ByteField('CD', None)
        ]

        def do_dissect(self, s):
            self.ST = bin(s[1]).strip('0b') + bin(s[0]).strip('0b')    # 字节1-2是连续的16位遥信状态
            self.CD = bin(s[3]).strip('0b') + bin(s[2]).strip('0b')    # 字节3-4是对应的变位标志，1表示变位，0表示未变位
            return s[4:]

        def extract_padding(self, s):
            return None, s

    class LEFloatField(Field):
        def __init__(self, name, default):
            Field.__init__(self, name, default, '<f')

    class LEIntField(Field):
        def __init__(self, name, default):
            Field.__init__(self, name, default, '<i')

    class SignedShortField(Field):
        def __init__(self, name, default):
            Field.__init__(self, name, default, "<h")

    class IOAID(Field):

        def __init__(self, name, default):
            Field.__init__(self, name, default, '<I')

        def addfield(self, pkt, s, val):
            if val is None:
                return s
            return s + pack('BBB', int(val & 0xff), int((val & 0xff00) / 0x0100), int((val & 0xff0000) / 0x010000))
            #return s + pack('BB', int(val & 0xff), int((val & 0xff00) / 0x0100))  # NOTE: For malformed packets

        def getfield(self, pkt, s):
            return s[3:], self.m2i(pkt, unpack(self.fmt, s[:3] + b'\x00')[0])
            #return s[2:], self.m2i(pkt, unpack(self.fmt, s[:2] + b'\x00\x00')[0])


class IECData:

    class IOA1(Packet):
        """7.3.1.1 M_SP_NA_1 单点遥信(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SIQ', None, IECPacket.SIQ)
        ]

    class IOA2(Packet):
        """7.3.1.2 M_SP_TA_1 带时标的单点信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SIQ', None, IECPacket.SIQ),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA3(Packet):
        """7.3.1.3 M_DP_NA_1 双点遥信(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DIQ', None, IECPacket.DIQ)
        ]

    class IOA4(Packet):
        """7.3.1.4 M_DP_TA_1 带时标的双点信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DIQ', None, IECPacket.DIQ),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA5(Packet):
        """7.3.1.5 M_ST_NA_1 步位置信息(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('VTI', None, IECPacket.VTI),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA6(Packet):
        """7.3.1.6 M_ST_TA_1 带时标的步位置信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('VTI', None, IECPacket.VTI),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA7(Packet):
        """7.3.1.7 M_BO_NA_1 32比特串(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BSI', None, IECPacket.BSI),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA8(Packet):
        """7.3.1.8 M_BO_TA_1 带时标的32比特串"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BSI', None, IECPacket.BSI),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA9(Packet):
        """ 7.3.1.9 M_ME_NA_1 规一化遥测值(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA10(Packet):
        """ 7.3.1.10 M_ME_TA_1 规一化遥测值(带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA11(Packet):
        """7.3.1.11 M_ME_NB_1 测量值，标度化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SVA', None, IECPacket.SVA),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA12(Packet):
        """7.3.1.12 M_ME_TB_1 测量值，带时标的标度化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SVA', None, IECPacket.SVA),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA13(Packet):
        """7.3.1.13 M_ME_NC_1 短浮点遥测值(带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA14(Packet):
        """7.3.1.14 M_ME_TC_1 短浮点遥测值(带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA15(Packet):
        """7.3.1.15 M_IT_NA_1 累计量"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BCR', None, IECPacket.BCR)
        ]

    class IOA16(Packet):
        """7.3.1.16 M_IT_TA_1 带时标的累计量"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BCR', None, IECPacket.BCR),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA17(Packet):
        """7.3.1.17 M_EP_TA_1 带时标的继电保护设备事件"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SEP', None, IECPacket.SEP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA18(Packet):
        """7.3.1.18 M_EP_TB_1 带时标的继电保护设备成组启动事件"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SPE', None, IECPacket.SPE),
            PacketField('QDP', None, IECPacket.QDP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA19(Packet):
        """7.3.1.19 M_EP_TC_1 带时标的继电保护设备成组输出电路信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('OCI', None, IECPacket.OCI),
            PacketField('QDP', None, IECPacket.QDP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP24Time', None, IECPacket.CP24Time)
        ]

    class IOA20(Packet):
        """7.3.1.20 M_PS_NA_1 带变位检出的成组单点信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SCD', None, IECPacket.SCD),
            PacketField('QDS', None, IECPacket.QDS)
        ]

    class IOA21(Packet):
        """ 7.3.1.21 M_ME_ND_1 规一化遥测值(不带品质描述 不带时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA)
        ]

    class IOA22(Packet):
        """ 7.3.1.22 M_SP_TB_1 带时标CP56Time2a的单点信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SIQ', None, IECPacket.SIQ),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA23(Packet):
        """ 7.3.1.23 M_DP_TB_1 带时标CP56Time2a的双点信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DIQ', None, IECPacket.DIQ),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA24(Packet):
        """ 7.3.1.24 M_ST_TB_1 带时标的步位置信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('VTI', None, IECPacket.VTI),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA25(Packet):
        """ 7.3.1.25 M_BO_TB_1 带时标CP56Time2a的32比特串"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BSI', None, IECPacket.BSI),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA26(Packet):
        """ 7.3.1.26 M_ME_TD_1 测量值，带时标CP56Time2a的规一化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA30(Packet):
        """7.3.1.30 M_SP_TB_1 单点遥信(带品质描述 带绝对时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SIQ', None, IECPacket.SIQ),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA31(Packet):
        """M_DP_TB_1 双点遥信(带品质描述 带绝对时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DIQ', None, IECPacket.DIQ),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA35(Packet):
        """ 7.3.1.27 M_ME_TE_1 测量值，带时标CP56Time2a的标度化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SVA', None, IECPacket.SVA),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA36(Packet):
        """ 7.3.1.28 M_ME_TF_1 测量值，带时标CP56Time2a的短浮点数"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),
            PacketField('QDS', None, IECPacket.QDS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA37(Packet):
        """ 7.3.1.29 M_IT_TB_1 带时标CP56Time2a的累计量"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('BCR', None, IECPacket.BCR),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA38(Packet):
        """7.3.1.30 M_EP_TD_1 带时标CP56Time2a的继电保护设备事件"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SEP', None, IECPacket.SEP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP56Time', None, IECPacket.CP56Time),
        ]

    class IOA39(Packet):
        """7.3.1.31 M_EP_TE_1 带时标CP56Time2a的继电保护设备成组启动事件"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SEP', None, IECPacket.SEP),
            PacketField('QDP', None, IECPacket.QDP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP56Time', None, IECPacket.CP56Time),
        ]

    class IOA40(Packet):
        """# 7.3.1.32 M_EP_TF_1 带时标CP56Time2a的继电保护设备成组输出电路信息"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('OCI', None, IECPacket.OCI),
            PacketField('QDP', None, IECPacket.QDP),
            PacketField('CP16Time', None, IECPacket.CP16Time),
            PacketField('CP56Time', None, IECPacket.CP56Time),
        ]

    class IOA42(Packet):
        """M_EP_TD_1 继电保护装置事件(带品质描述 带绝对时标)"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('CP16Time', None, IECPacket.CP16Time),  # CP16Time
            PacketField('CP56Time', None, IECPacket.CP56Time),
        ]

    class IOA45(Packet):
        """7.3.2.1 C_SC_NA_1 单命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SCO', None, IECPacket.SCO)
        ]

    class IOA46(Packet):
        """7.3.2.2 C_DC_NA_1 双命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DCO', None, IECPacket.DCO)
        ]

    class IOA47(Packet):
        """7.3.2.3 C_RC_NA_1 步调节命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('RCO', None, IECPacket.RCO)
        ]

    class IOA48(Packet):
        """7.3.2.4 C_SE_NA_1 设定命令，规一化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA),
            PacketField('QOS', None, IECPacket.QOS)
        ]

    class IOA49(Packet):
        """7.3.2.5 C_SE_NB_1 设定命令，标度化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SVA', None, IECPacket.SVA),    # StrField("Value", '', fmt="H", remain=0)
            PacketField('QOS', None, IECPacket.QOS)
        ]

    class IOA50(Packet):
        """ 7.3.2.6C_SE_NC_1 设定命令，短浮点数"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),  # StrField("Value", '', fmt="f", remain=0)
            PacketField('QOS', None, IECPacket.QOS)
        ]

    class IOA51(Packet):
        """C_BO_NA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEIntField('Value', None) # StrField("Value", '', fmt="I", remain=0)
        ]

    class IOA58(Packet):
        """C_SC_TA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SCO', None, IECPacket.SCO),    # XByteField("SCO", 0x80),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA59(Packet):
        """C_DC_TA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('DCO', None, IECPacket.DCO),    # XByteField("DCO", 0x80),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA60(Packet):
        """C_RC_TA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('RCO', None, IECPacket.RCO),    # XByteField("RCO", 0x80),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA61(Packet):
        """C_SE_TA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEIntField('Value', None),    # StrField("Value", '', fmt="H", remain=0),
            PacketField('QOS', None, IECPacket.QOS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA62(Packet):
        """C_SE_TB_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEIntField('Value', None),    # StrField("Value", '', fmt="H", remain=0),
            PacketField('QOS', None, IECPacket.QOS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA63(Packet):
        """C_SE_TC_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),  # StrField("Value", '', fmt="f", remain=0),
            PacketField('QOS', None, IECPacket.QOS),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA64(Packet):
        """C_BO_TA_1"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEIntField('Value', None),    # StrField("Value", '', fmt="I", remain=0)
            PacketField('CP56Time', None, IECPacket.CP56Time)   # PacketField("CP56Time", CP56Time, Packet)]
        ]

    class IOA70(Packet):
        """ 7.3.3 M_EI_NA_1 初始化结束"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('COI', None, IECPacket.COI),
        ]

    class IOA100(Packet):
        """7.3.4.1 C_IC_NA_1 召唤命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('QOI', None, IECPacket.QOI)   #PacketField('QOI', None, IECPacket.QOI)
        ]

    class IOA101(Packet):
        """7.3.4.2 C_CI_NA_1 计数量召唤命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('QCC', None, IECPacket.QCC)
        ]

    class IOA102(Packet):
        """7.3.4.3 C_RD_NA_1 读命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
        ]

    class IOA103(Packet):
        """7.3.4.4 C_CS_NA_1 时钟同步命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    class IOA104(Packet):
        """7.3.4.5 C_TS_NA_1 测试命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('FBP', None, IECPacket.FBP)
        ]

    class IOA105(Packet):
        """7.3.4.6 C_RP_NA_1 复位进程命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('QRP', None, IECPacket.QRP)
        ]

    class IOA106(Packet):
        """7.3.4.7 C_CD_NA_1 延时获得命令"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('CP16Time', None, IECPacket.CP16Time)
        ]

    class IOA110(Packet):
        """7.3.5.1 P_ME_NA_1 测量值参数，规一化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NVA', None, IECPacket.NVA),
            PacketField('QPM', None, IECPacket.QPM)
        ]

    class IOA111(Packet):
        """7.3.5.2 P_ME_NB_1 测试值参数，标度化值"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('SVA', None, IECPacket.SVA),
            PacketField('QPM', None, IECPacket.QPM)
        ]

    class IOA112(Packet):
        """7.3.5.3 P_ME_NC_1 测量值参数，短浮点数"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            IECPacket.LEFloatField('Value', None),
            PacketField('QPM', None, IECPacket.QPM)
        ]

    class IOA113(Packet):
        """7.3.5.4 P_AC_NA_1 参数激活"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('QPA', None, IECPacket.QPA)
        ]

    class IOA120(Packet):
        """7.3.6.1 F_FR_NA_1 文件准备就绪"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('LOF', None, IECPacket.LOF),
            PacketField('FRQ', None, IECPacket.FRQ)
        ]

    class IOA121(Packet):
        """7.3.6.2 F_SR_NA_1 节准备就绪"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('NOS', None, IECPacket.NOS),
            PacketField('LOF', None, IECPacket.LOF),
            PacketField('SRQ', None, IECPacket.SRQ)
        ]

    class IOA122(Packet):
        """7.3.6.3 F_SC_NA_1 召唤目录，选择文件，召唤文件，召唤节"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('NOS', None, IECPacket.NOS),
            PacketField('SCQ', None, IECPacket.SCQ),
        ]

    class IOA123(Packet):
        """7.3.6.4 F_LS_NA_1 最后的节，最后的段"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('NOS', None, IECPacket.NOS),
            PacketField('LSQ', None, IECPacket.LSQ),
            PacketField('CHS', None, IECPacket.CHS),
        ]

    class IOA124(Packet):
        """7.3.6.5 F_AF_NA_1 认可文件，认可节"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('NOS', None, IECPacket.NOS),
            PacketField('AFQ', None, IECPacket.AFQ),
        ]

    class IOA125(Packet):
        """7.3.6.6 F_SG_NA_1 段"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('NOS', None, IECPacket.NOS),
            PacketField('LOS', None, IECPacket.LOS),
        ]

    class IOA126(Packet):
        """7.3.6.7 F_DR_TA_1 目录"""
        name = 'IOA'
        fields_desc = [
            IECPacket.IOAID('IOA', None),
            PacketField('NOF', None, IECPacket.NOF),
            PacketField('LOF', None, IECPacket.LOF),
            PacketField('SOF', None, IECPacket.SOF),
            PacketField('CP56Time', None, IECPacket.CP56Time)
        ]

    IOAS = {
        1: IOA1,    # 单点遥信(带品质描述 不带时标)
        2: IOA2,
        3: IOA3,    # 双点遥信(带品质描述 不带时标)
        4: IOA4,
        5: IOA5,    # 步位置信息(带品质描述 不带时标)
        7: IOA7,    # 32比特串(带品质描述 不带时标)
        9: IOA9,    # 规一化遥测值(带品质描述 不带时标)
        10: IOA10,
        11: IOA11,  # 标度化值(带品质描述 不带时标)
        12: IOA12,
        13: IOA13,  # 短浮点遥测值(带品质描述 不带时标)
        14: IOA14,
        15: IOA15,  # 累积量(带品质描述 不带时标)
        16: IOA16,
        20: IOA20,
        21: IOA21,
        30: IOA30,  # 单点遥信(带品质描述 带绝对时标)
        31: IOA31,  # 双点遥信(带品质描述 带绝对时标)
        36: IOA36,  # 短浮点遥测值(带品质描述 带绝对时标)
        37: IOA37,   # 累积量(带品质描述 带绝对时标)
        45: IOA45,  # 单点遥控(一个报文只有一个遥控信息体 不带时标)
        50: IOA50,   # 短浮点设定值(一个报文只有一个设定值 不带时标)
        70: IOA70,   # 初始化结束(从站发送，主站收到时候会做一次总召)
        100: IOA100,    # 总召
        101: IOA101,  # 电能脉冲召唤命令
        103: IOA103,     # 时钟同步命令
    }

    IOALEN = {
        1: 4,   # 单点遥信(带品质描述 不带时标) 地址3字节+数据1字节
        2: 7,   # 带3个字节短时标的单点遥信 地址3字节+数据1字节+时标3字节
        3: 4,   # 双点遥信(带品质描述 不带时标) 地址3字节+数据1字节
        4: 7,   # 带3个字节短时标的双点遥信(带品质描述 带时标) 地址3字节+数据1字节+时标3字节
        5: 5,
        6: 8,
        7: 8,
        8: 11,
        9: 6,     # 规一化遥测值(带品质描述 不带时标)  地址3字节+信息体长度3字节
        10: 9,      # 带3个字节时标且具有品质描述的测量值， 地址3字节+遥测值占6个字节
        11: 6,      # 不带时标的标度化值 地址3字节+遥测值占3个字节
        12: 9,   # 带3个字节时标标度化值， 地址3字节+遥测值占6个字节
        13: 8,  # 短浮点遥测值(带品质描述 不带时标) 地址3字节+遥测值占5个字节
        14: 11,     # 带3个字节时标短浮点遥测值(带品质描述 带时标) 地址3字节+遥测值占8个字节
        15: 8,      # 电能脉冲计数量 地址3字节+电能量5个字节
        16: 11,     # 电能脉冲计数量 地址3字节+电能量5个字节 + 时标3字节
        17: 9,
        18: 10,
        19: 10,
        20: 8,  # 具有状态变为检测的成组单点遥信，每个字节包括8个遥信
        21: 5,  # 带3个字节时标且具有品质描述的短浮点遥测值(带品质描述 不带时标) 地址3字节+遥测值占2个字节
        22: 11,
        23: 11,
        24: 12,
        25: 15,
        26: 13,
        30: 11,     # 单点遥信(带品质描述 带绝对时标)  地址3字节+数据1字节 + 时标7字节
        31: 11,     # 双点遥信(带品质描述 带绝对时标)  地址3字节+数据1字节 + 时标7字节
        35: 13,
        36: 15,
        37: 15,     # 电能脉冲计数量 地址3字节+电能量5个字节 + 时标7字节
        38: 13,
        39: 14,
        40: 14,
        45: 4,
        46: 4,
        47: 4,
        48: 6,
        49: 6,
        50: 8,
        51: 7,
        70: 4,
        100: 4,
        101: 4,
        103: 10,
        104: 5,
        105: 4,
        106: 5,
        110: 6,
        111: 6,
        112:  8,
        113: 4,
        121: 7,
        122: 6,
        123: 7,
        124: 6,
        126: 13
    }


class IOTIEC104(IOTDriver):

    class ASDU(Packet):
        name = 'ASDU'

        fields_desc = [
            ByteEnumField('Type', None, IECDefine.ASDU_TYPE),
            ByteEnumField('SQ', None, IECDefine.ASDU_SQ),
            ByteField('Num', 0),
            ByteEnumField('Cause', None, IECDefine.ASDU_CAUSE),
            ByteEnumField('PN', 0x00, IECDefine.ASDU_PN),
            ByteField('Test', None),
            ByteField('OA', None),
            LEShortField('Addr', None),
            PacketListField('IOA', None)
        ]

        def do_dissect(self, s):
            self.Type = s[0] & 0xff   # 类型(1)
            self.SQ = s[1] & 0x80 == 0x80   # 限定词(1)
            self.Num = s[1] & 0x7f  # 数量
            self.Cause = s[2] & 0x3F    # 原因
            self.PN = s[2] & 0x40   # 第6位为P/N = 0 肯定 ； P/N = 1 否定 （正常为P/N = 0；P/N = 1说明该报文无效
            self.Test = s[2] & 0x80 # 第7为为测试 T = 0 未试验 ； T = 1 试验 （一般 T= 0）
            self.OA = s[3]          # 源发地址：用来记录来时哪个主站的响应数据，一般写 0；
            self.Addr = unpack('<H', s[4:6])[0] # 公共地址

            flag = True
            IOAS = list()
            remain = s[6:]

            idx = 6
            offset = 0
            if self.Type not in IECData.IOAS.keys():
                raise Exception(f"unsupport type({self.Type}")
            else:
                ioa_type = IECData.IOAS.get(self.Type)
                ioa_length = IECData.IOALEN.get(self.Type)
                if self.SQ:
                    for i in range(1, self.Num + 1):
                        if flag:
                            if len(remain[:ioa_length]) >= ioa_length:
                                IOAS.append(ioa_type(remain[:ioa_length]))
                                offset = IOAS[0].IOA
                                remain = remain[ioa_length:]
                                idx = idx + ioa_length
                                ioa_length = ioa_length - 3
                        else:
                            if len(remain[:ioa_length]) >= ioa_length:
                                _offset = pack("<H", (i - 1) + offset) + b'\x00'  # See 7.2.2.1 of IEC 60870-5-101
                                IOAS.append(ioa_type(_offset + remain[:ioa_length]))
                                remain = remain[ioa_length:]
                                idx = idx + ioa_length
                        flag = False
                else:
                    for i in range(1, self.Num + 1):
                        if len(remain[:ioa_length]) >= ioa_length:
                            IOAS.append(ioa_type(remain[: ioa_length]))
                            remain = remain[ioa_length:]
                            idx = idx + ioa_length
            self.IOA = IOAS
            return s[idx:]

        def do_build(self):
            s = bytearray()
            s.append(self.Type)
            s.append(self.SQ | self.Num)
            s.append(self.Test | self.PN | self.Cause)
            s.append(self.OA)
            s.append(int(self.Addr) & 0xff)
            s.append(int(self.Addr) >> 8)
            s = bytes(s)
            if self.IOA is not None:
                for i in self.IOA:
                    s += i.build()

            return s

        def info(self, pkt: Packet = None):
            pkt = self if pkt is None else pkt
            values = {}
            for key in pkt.fields.keys():
                if isinstance(pkt.fields[key], list):
                    for filed in pkt.fields[key]:
                        if isinstance(filed, Packet):
                            if filed.name not in values.keys():
                                values[filed.name] = []
                            values[filed.name].append(self.info(filed))
                elif isinstance(pkt.fields[key], Packet):
                    values[pkt.fields[key].name] = self.info(pkt.fields[key])
                else:
                    values[key] = pkt.fields[key]
            return values

    class APCI(Packet):
        name = 'ACPI'

        fields_desc = [
            XByteField('START', 0x68),      # 68H
            ByteField('ApduLen', 4),        # 长度
            ByteEnumField('Type', 0x00, IECDefine.APCI_TYPE),   # 帧类型
            ConditionalField(XByteField('UType', None), lambda pkt: pkt.Type == 0x03),  # U帧类型
            ConditionalField(ShortField('Tx', 0x00), lambda pkt: pkt.Type == 0x00),
            ConditionalField(ShortField('Rx', 0x00), lambda pkt: pkt.Type < 3),
        ]

        def do_dissect(self, s):
            self.START = s[0]       # 68H
            self.ApduLen = s[1]     # 长度
            self.Type = s[2] & 0x03 if bool(s[2] & 0x01) else 0x00
            if self.Type == 3:      # U帧
                self.UType = (s[2] & 0xfc) >> 2
            else:
                if self.Type == 0:  # I帧
                    self.Tx = (s[3] << 7) | (s[2] >> 1)
                self.Rx = (s[5] << 7) | (s[4] >> 1)
            return s[6:]

        def dissect(self, s):
            s = self.pre_dissect(s)
            s = self.do_dissect(s)
            s = self.post_dissect(s)
            payl, pad = self.extract_padding(s)
            self.do_dissect_payload(payl)
            if pad:
                self.add_payload(IOTIEC104.APDU(pad))

        def do_build(self):
            s = list(range(6))
            s[0] = 0x68
            s[1] = self.ApduLen
            if self.Type == 0x03:
                s[2] = ((self.UType << 2) & 0xfc) | self.Type
                s[3] = 0
                s[4] = 0
                s[5] = 0
            else:
                if self.Type == 0x00:
                    s[2] = ((self.Tx << 1) & 0x00fe) | self.Type
                    s[3] = ((self.Tx << 1) & 0xff00) >> 8
                else:
                    s[2] = self.Type
                    s[3] = 0
                s[4] = (self.Rx << 1) & 0x00fe
                s[5] = ((self.Rx << 1) & 0xff00) >> 8
            s = bytes(s)
            if self.haslayer('ASDU'):
                s += self.payload.build()
            return s

        def extract_padding(self, s):
            if self.Type == 0x00 and self.ApduLen > 4:
                return s[:self.ApduLen - 4], s[self.ApduLen - 4:]
            return None, s

        def do_dissect_payload(self, s):
            if s is not None:
                p = IOTIEC104.ASDU(s, _internal=1, _underlayer=self)
                self.add_payload(p)
        def info(self):
            values = {}
            for key in self.fields.keys():
                values[key] = self.fields[key]
            return values

    class APDU(Packet):
        name = 'APDU'

        def dissect(self, s):
            s = self.pre_dissect(s)
            s = self.do_dissect(s)
            s = self.post_dissect(s)
            payl, pad = self.extract_padding(s)
            self.do_dissect_payload(payl)
            if pad:
                if pad[0] in [0x68]:
                    self.add_payload(IOTIEC104.APDU(pad, _internal=1, _underlayer=self))
                else:
                    self.add_payload(Padding(pad))

        def do_dissect(self, s):
            apci = IOTIEC104.APCI(s, _internal=1, _underlayer=self)
            self.add_payload(apci)

        def info(self):
            values = {}
            if not isinstance(self.payload, NoPayload):
                values[self.payload.name] = self.payload.info()
                if not isinstance(self.payload.payload, NoPayload):
                    values[self.payload.payload.name] = self.payload.payload.info()
            return values

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.reinit()

    def reinit(self):
        self.client = None
        self.is_connected = False
        self.ole_zongzhao = IOTBaseCommon.get_datetime()    # 总召时间
        self.ole_dianneng = IOTBaseCommon.get_datetime()    # 电能召唤时间
        self.ole_recv = IOTBaseCommon.get_datetime()  # 收到回复数据时间

        self.event_zongzhao = None   # 总召事件激活
        self.event_dianneng = None  # 电能
        self.values = {}
        self.send_count = 0
        self.recv_count = 0
        self.recv_i_total = 0     # I帧接收

    def exit(self):
        self._release_client()

    @classmethod
    def template(cls, mode: int, type: str, lan: str) -> List[Dict[str, Any]]:
        templates = []
        if type == 'point':
            templates.extend([
                {'required': True, 'name': '是否可写' if lan == 'ch' else 'writable'.upper(), 'code': 'point_writable', 'type': 'bool', 'default': 'TRUE', 'enum': [], 'tip': ''},
                {'required': True, 'name': '物理点名' if lan == 'ch' else 'name'.upper(), 'code': 'point_name', 'type': 'string', 'default': 'Chiller_1_CHW_ENT', 'enum': [], 'tip': ''},
                {'required': True, 'name': '点地址' if lan == 'ch' else 'Address', 'code': 'point_address', 'type': 'int', 'default': 16385, 'enum': [], 'tip': ''},
                {'required': True, 'name': '点类型' if lan == 'ch' else 'Type'.upper(), 'code': 'point_type', 'type': 'int', 'default': 13, 'enum': [], 'tip': ''},
                {'required': False, 'name': '点描述' if lan == 'ch' else 'description'.upper(), 'code': 'point_description', 'type': 'string', 'default': 'Chiller_1_CHW_ENT', 'enum': [], 'tip': ''},
                {'required': False, 'name': '逻辑点名' if lan == 'ch' else 'name alias'.upper(), 'code': 'point_name_alias', 'type': 'string', 'default': 'Chiller_1_CHW_ENT1', 'enum': [], 'tip': ''},
                {'required': True, 'name': '是否启用' if lan == 'ch' else 'enable'.upper(), 'code': 'point_enabled', 'type': 'bool', 'default': 'TRUE', 'enum': [], 'tip': ''},
                {'required': True, 'name': '倍率' if lan == 'ch' else 'scale'.upper(), 'code': 'point_scale', 'type': 'string', 'default': '1', 'enum': [], 'tip': ''}
            ])
        elif type == 'config':
            templates.extend([
                {'required': True, 'name': '地址' if lan == 'ch' else 'Host', 'code': 'host', 'type': 'string', 'default': '192.168.1.1', 'enum': [], 'tip': ''},
                {'required': True, 'name': '端口' if lan == 'ch' else 'Port', 'code': 'port', 'type': 'int', 'default': 2404, 'enum': [], 'tip': ''},
                {'required': True, 'name': '超时(s)' if lan == 'ch' else 'Timeout(s)', 'code': 'timeout', 'type': 'float', 'default': 10, 'enum': [], 'tip': ''},
                {'required': False, 'name': '总召(s)' if lan == 'ch' else 'ZongZhao Interval(s)', 'code': 'zongzhao_interval', 'type': 'int', 'default': 900, 'enum': [], 'tip': ''},
                {'required': False, 'name': '总召超时(s)' if lan == 'ch' else 'ZongZhao Timeout(s)', 'code': 'zongzhao_timeout', 'type': 'int', 'default': 30, 'enum': [], 'tip': ''},
                {'required': False, 'name': '电能召唤(s)' if lan == 'ch' else 'DianNeng Interval(s)', 'code': 'dianneng_interval', 'type': 'int', 'default': 60, 'enum': [], 'tip': ''},
                {'required': False, 'name': '电能召唤超时(s)' if lan == 'ch' else 'DianNeng Timeout(s)', 'code': 'dianneng_timeout', 'type': 'int', 'default': 30, 'enum': [], 'tip': ''},
                {'required': False, 'name': 'S帧' if lan == 'ch' else 'S Interval', 'code': 's_interval', 'type': 'int', 'default': 0, 'enum': [], 'tip': ''},
                {'required': False, 'name': '超时U帧测试(s)' if lan == 'ch' else 'U Test Timeout(s)', 'code': 'u_test_timeout', 'type': 'int', 'default': 15, 'enum': [], 'tip': ''},    # 超时发送U帧
            ])

        return templates

    def read(self, **kwargs):
        self.update_info(used=IOTBaseCommon.get_datetime_str())

        names = kwargs.get('names', list(self.points.keys()))
        self.update_results(names, True, None)
        read_items = []
        for name in names:
            point = self.points.get(name)
            if point:
                type = point.get('point_type')  # 单点遥信
                address = point.get('point_address')    # 点地址
                if type is not None and address is not None:
                    read_items.append(f"{type}_{address}")

        self._read(list(set(read_items)))

        for name in names:
            point = self.points.get(name)
            if point:
                type = point.get('point_type')  # 单点遥信
                address = point.get('point_address')  # 点地址
                if type is not None and address is not None:
                    value = self._get_value(name, f"{self.configs.get('host')}:{self.configs.get('port')}", address, type)
                    if value is not None:
                        self.update_results(name, True, value)
            else:
                self.update_results(name, False, 'UnExist')
        return self.get_results(**kwargs)

    def write(self, **kwargs):
        self.update_info(used=IOTBaseCommon.get_datetime_str())
        results = {}
        values = kwargs.get('values', {})
        for name, value in values.items():
            point = self.points.get(name)
            result = [False, 'Unknown']
            if point:
                type = point.get('point_type')  # 单点遥信
                address = point.get('point_address')  # 点地址
                if type is not None and address is not None:
                    self._write(type, address, value)
                    result = self.get_device_property(f"{self.configs.get('host')}:{self.configs.get('port')}", f"{type}_{address}", [self.get_write_quality, self.get_write_result])
                else:
                    result = [False, 'Invalid Params']
            else:
                result = [False, 'Point UnExist']
            results[name] = result
            if result[0] is not True:
                self.logging(content=f"write value({name}) fail({result[1]})", level='ERROR', source=name, pos=self.stack_pos)
        return results

    def ping(self, **kwargs) -> bool:
        self.update_info(used=IOTBaseCommon.get_datetime_str())
        return self.is_connected

    def _read(self, read_items: list):
        try:
            if len(read_items) > 0 and self._get_client():
                pass
        except Exception as e:
            for read_item in read_items:
                self.update_device(f"{self.configs.get('host')}:{self.configs.get('port')}", read_item, **self.gen_read_write_result(False, e.__str__()))

    def _write(self, type: int, address: int, value):
        raise NotImplementedError()

    def _release_client(self):
        self.is_connected = False
        try:
            if self.client:
                self.client.exit()
        except Exception as e:
            pass
        finally:
            self.reinit()

    def _get_client(self):
        try:
            if self.client is not None and (self.is_connected is False or self.client.check_invalid() is False):
                self._release_client()

            if self.client is None:
                self.clear_device(f"{self.configs.get('host')}:{self.configs.get('port')}")
                client = IOTBaseCommon.IECSocketClient(self.configs.get('host'), self.configs.get('port'), self.configs.get('timeout', 4), callbacks={'handle_data': self.handle_data, 'handle_connect': self.handle_connect, 'handle_close': self.handle_close, 'handle_error': self.handle_error})
                self.client = client
            return self.client
        except Exception as e:
            raise Exception(f"connect fail({e.__str__()})")

    def handle_connect(self, client):
        start_frame = (IOTIEC104.APDU() / IOTIEC104.APCI(ApduLen=4, Type=0x03, UType=0x01)).build()
        self.logging(content=f"iec104({client}) send U: ({self.format_bytes(start_frame)})", pos=self.stack_pos)

        # 连接成功 U帧启动报文
        self.is_connected = True
        client.send(start_frame)

        # 启动总召轮询和U帧测试
        IOTBaseCommon.function_thread(self.send_zongzhao_thread, True, f"iecclient({self.configs.get('host')}:{self.configs.get('port')}) zongzhao").start()
        IOTBaseCommon.function_thread(self.send_u_test_thread, True, f"iecclient({self.configs.get('host')}:{self.configs.get('port')}) u-test").start()

    # 关闭事件
    def handle_close(self, client, reason: str):
        self.is_connected = False
        self.logging(content=f"iec104({client}) close({reason})", pos=self.stack_pos)

    def handle_error(self, client, e: Exception):
        self.is_connected = False
        self.logging(content=f"iec104({client}) error({e.__str__()})", level='ERROR', pos=self.stack_pos)

    def handle_data(self, client, datas: bytes):
        try:
            if len(datas) > 0 and client is not None:
                self.ole_recv = IOTBaseCommon.get_datetime()

                info = IOTIEC104.APDU(datas).info()
                acpi = info.get('ACPI', {})
                asdu = info.get('ASDU', {})
                type = acpi.get('Type')
                if type == 0:  # I帧
                    self.recv_count = info.get('ACPI', {}).get('Rx', self.recv_count) + 1
                    self.recv_i_total = self.recv_i_total + 1

                    type_id = asdu.get('Type')
                    cause_id = asdu.get('Cause')
                    self.logging(content=f"iec104({client}) recv I {self._get_frame_name(type_id, cause_id)}: [{self.format_bytes(datas)}]", pos=self.stack_pos)

                    s_interval = self.configs.get('s_interval', 0)
                    if s_interval > 0 and self.recv_i_total % s_interval == 0:
                        self._send_s_frame(client)

                    if type_id == 100:  # 总召
                        if cause_id == 7:   # 总召确认
                            pass
                        elif cause_id == 10:   # 总召结束
                            if self.event_zongzhao:
                                self.event_zongzhao.set()
                    elif type_id in [1, 30]:  # 单点遥信(带品质描述 不带时标) 单点遥信(带品质描述 带绝对时标)
                        for ioa in asdu.get('IOA', []):
                            if 'SIQ' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('SIQ').get('SPI'))
                    elif type_id in [3, 31]:  # 双点遥信(带品质描述 不带时标) 双点遥信(带品质描述 带绝对时标)
                        for ioa in asdu.get('IOA', []):
                            if 'DIQ' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('DIQ').get('DPI'))
                    elif type_id == 5:  # 步位置信息(带品质描述 不带时标)
                        for ioa in asdu.get('IOA', []):
                            if 'VTI' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('VTI').get('Value'))
                    elif type_id == 7:  # 32比特串(带品质描述 不带时标)
                        pass
                    elif type_id == 9:  # 规一化遥测值(带品质描述 不带时标)
                        for ioa in asdu.get('IOA', []):
                            if 'DIQ' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('DIQ').get('DPI'))
                    elif type_id == 11:  # 标度化值
                        for ioa in asdu.get('IOA', []):
                            if 'SVA' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('SVA'))
                    elif type_id in [13, 36]:     # 短浮点遥测值(带品质描述 不带时标) 短浮点遥测值(带品质描述 带绝对时标)
                        for ioa in asdu.get('IOA', []):
                            if 'Value' in ioa.keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('Value'))
                    elif type_id in [15, 37]:  # 累积量(带品质描述 不带时标)
                        for ioa in asdu.get('IOA', []):
                            if 'V' in ioa.get('BCR', {}).keys():
                                self._update_value(type_id, ioa.get('IOA'), ioa.get('BCR', {}).get('V'))
                    elif type_id == 45:     # 单点遥控(一个报文只有一个遥控信息体 不带时标)
                        pass
                    elif type_id == 50:     # 短浮点设定值(一个报文只有一个设定值 不带时标)
                        pass
                    elif type_id == 101:    # 电能脉冲召唤命令
                        if cause_id == 7:   # 电能确认
                            pass
                        elif cause_id == 10:   # 电能结束
                            if self.event_dianneng is not None:
                                self.event_dianneng.set()
                    elif type_id == 103:    # 时钟同步
                        pass
                elif type == 1:  # S帧
                    self.logging(content=f"iec104({client}) recv S: [{self.format_bytes(datas)}]", pos=self.stack_pos)
                elif type == 3:
                    self.logging(content=f"iec104({client}) recv U: [{self.format_bytes(datas)}]", pos=self.stack_pos)
                    if info.get('ACPI', {}).get('UType') == 0x02:  # U帧激活确认 发送总召命令
                        self._send_zongzhao(client)
                    elif info.get('ACPI', {}).get('UType') == 0x08:     # U帧结束确认
                        self.is_connected = False
                    elif info.get('ACPI', {}).get('UType') == 0x10:     # U帧测试确认
                        self._send_u_test_frame(client, 0x20)
                    elif info.get('ACPI', {}).get('UType') == 0x20:     # U帧测试确认
                        pass
        except Exception as e:
            self.logging(content=f"handle data fail({e.__str__()})({self.format_bytes(datas)})", level='ERROR', pos=self.stack_pos)

    def _update_value(self, type_id: int, address: int, value):
        self.update_device(f"{self.configs.get('host')}:{self.configs.get('port')}", f"{type_id}_{address}", **self.gen_read_write_result(True, value))

    def _get_value(self, name: str, device_address: str, address: str, type: int):
        try:
            [result, value] = self.get_device_property(device_address, f"{type}_{address}", [self.get_read_quality, self.get_read_result])
            if result is True:
                if value is not None:
                    return value
                else:
                    raise Exception(f"value is none")
            else:
                raise Exception(str(value))
        except Exception as e:
            self.update_results(name, False, e.__str__())
        return None

    def _send_frame(self, client, type_id: int, cause_id: int, datas: bytes):
        if client is not None:
            self.logging(content=f"iec104 send {self._get_frame_name(type_id, cause_id)}: [{self.format_bytes(datas)}]", pos=self.stack_pos)
            client.send(datas)
        
            if len(datas) > 6:
                self.send_count = self.send_count + 1

    def _get_frame_name(self, type_id: int, cause_id: int) -> str:
        return f"{IECDefine.ASDU_TYPE.get(type_id)} {IECDefine.ASDU_CAUSE.get(cause_id)}"

    # 发送总召命令
    def _send_zongzhao(self, client):
        if client is not None:
            pkt = IOTIEC104.APDU()
            pkt /= IOTIEC104.APCI(ApduLen=14, Type=0x00, Tx=self.send_count, Rx=self.recv_count)
            pkt /= IOTIEC104.ASDU(Type=100, SQ=0, Cause=6, Num=1, Test=0, OA=0, Addr=1, IOA=[IECData.IOAS[100](IOA=0, QOI=0x14)])

            self.event_zongzhao = Event()
            self._send_frame(client, 100, 6, pkt.build())
            self.ole_zongzhao = IOTBaseCommon.get_datetime()

    # 发送电能脉冲召唤命令
    def _send_dianneng(self, client):
        if client is not None:
            pkt = IOTIEC104.APDU()
            pkt /= IOTIEC104.APCI(ApduLen=14, Type=0x00, Tx=self.send_count, Rx=self.recv_count)
            pkt /= IOTIEC104.ASDU(Type=101, SQ=0, Cause=6, Num=1, Test=0, OA=0, Addr=1, IOA=[IECData.IOAS[101](IOA=0, QCC=IECPacket.QCC(RQT=0, FRZ=0))])

            self.event_dianneng = Event()
            self._send_frame(client, 101, 6, pkt.build())
            self.ole_dianneng = IOTBaseCommon.get_datetime()

    def _send_u_test_frame(self, client, utype: int = 0x10):
        """发送U帧测试帧"""
        if client is not None:
            start_frame = (IOTIEC104.APDU() / IOTIEC104.APCI(ApduLen=4, Type=0x03, UType=utype)).build()
            self.logging(content=f"iec104({client}) send U ({self.format_bytes(start_frame)})", pos=self.stack_pos)
            client.send(start_frame)
            self.ole_recv = IOTBaseCommon.get_datetime()

    def _send_s_frame(self, client):
        """发送S帧"""
        if client is not None:
            start_frame = (IOTIEC104.APDU() / IOTIEC104.APCI(ApduLen=4, Type=0x01, Rx=self.recv_count)).build()
            self.logging(content=f"iec104({client}) send S ({self.format_bytes(start_frame)})", pos=self.stack_pos)
            client.send(start_frame)

    def send_zongzhao_thread(self):
        """总召轮询"""
        while self.is_connected:
            self.delay(1)

            # 等待电能结束事件
            dianneng_timeout = self.configs.get('dianneng_timeout', 30)
            if isinstance(dianneng_timeout, int) and self.event_dianneng is not None and self.event_dianneng.is_set() is False and (IOTBaseCommon.get_datetime() - self.ole_dianneng).total_seconds() <= dianneng_timeout:  # 尚未收到电能结束命令
                continue

            # 先发总召
            zongzhao_interval = self.configs.get('zongzhao_interval', 0)
            if isinstance(zongzhao_interval, int) and zongzhao_interval > 0:
                if (IOTBaseCommon.get_datetime() - self.ole_zongzhao).total_seconds() >= zongzhao_interval:
                    try:
                        self._send_zongzhao(self.client)
                    except:
                        pass

            # 等待总召结束事件
            zongzhao_timeout = self.configs.get('zongzhao_timeout', 30)
            if isinstance(zongzhao_timeout, int) and self.event_zongzhao is not None and self.event_zongzhao.is_set() is False and (IOTBaseCommon.get_datetime() - self.ole_zongzhao).total_seconds() <= zongzhao_timeout:    # 尚未收到总召结束命令
                continue

            # 发送电能脉冲召唤命令
            dianneng_interval = self.configs.get('dianneng_interval', 0)
            if isinstance(dianneng_interval, int) and dianneng_interval > 0:
                if (IOTBaseCommon.get_datetime() - self.ole_dianneng).total_seconds() >= dianneng_interval:
                    try:
                        self._send_dianneng(self.client)
                    except:
                        pass

    def send_u_test_thread(self):
        """发送U帧测试帧 超过一定时间没有下发报文或者装置没有上送任何报文"""
        u_test_timeout = self.configs.get('u_test_timeout', 10)
        if u_test_timeout > 0:
            while self.is_connected:
                self.delay(1)
                if (IOTBaseCommon.get_datetime() - self.ole_recv).total_seconds() >= u_test_timeout:
                    try:
                        self._send_u_test_frame(self.client)
                    except:
                        pass

    def format_bytes(self, data: bytes) -> str:
        if isinstance(data, bytes):
            return ' '.join(["%02X" % x for x in data]).strip()
        return ''